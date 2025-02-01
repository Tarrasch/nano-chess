from manual_eval import piece_values, piece_square_tables
from itertools import count
import dataclasses
from typing import List, Optional
import math
import neural_network_eval

# Code taken from Sunfish.

###############################################################################
# Global constants
###############################################################################

# Our board is represented as a 120 character string. The padding allows for
# fast detection of moves that don't stay within the board.
A1, H1, A8, H8 = 91, 98, 21, 28
initial = (
    "         \n"  #   0 -  9
    "         \n"  #  10 - 19
    " rnbqkbnr\n"  #  20 - 29
    " pppppppp\n"  #  30 - 39
    " ........\n"  #  40 - 49
    " ........\n"  #  50 - 59
    " ........\n"  #  60 - 69
    " ........\n"  #  70 - 79
    " PPPPPPPP\n"  #  80 - 89
    " RNBQKBNR\n"  #  90 - 99
    "         \n"  # 100 -109
    "         \n"  # 110 -119
)

# Lists of possible moves for each piece type.
N, E, S, W = -10, 1, 10, -1
directions = {
    "P": (N, N + N, N + W, N + E),
    "N": (
        N + N + E,
        E + N + E,
        E + S + E,
        S + S + E,
        S + S + W,
        W + S + W,
        W + N + W,
        N + N + W,
    ),
    "B": (N + E, S + E, S + W, N + W),
    "R": (N, E, S, W),
    "Q": (N, E, S, W, N + E, S + E, S + W, N + W),
    "K": (N, E, S, W, N + E, S + E, S + W, N + W),
}

# Mate value must be greater than 8*queen + 2*(rook+knight+bishop)
# King value is set to twice this value such that if the opponent is
# 8 queens up, but we got the king, we still exceed MATE_VALUE.
# When a MATE is detected, we'll set the score to MATE_UPPER - plies to get there
# E.g. Mate in 3 will be MATE_UPPER - 6
MATE_LOWER = piece_values["K"] - 10 * piece_values["Q"]
MATE_UPPER = piece_values["K"] + 10 * piece_values["Q"]


###############################################################################
# Chess logic
###############################################################################


@dataclasses.dataclass(frozen=True)
class Move:
    i: int
    j: int
    prom: str  # piece being promoted to

    @staticmethod
    def from_uci(move_in_uci: str):
        """
        Converts a UCI string to a Move object.

        The output is not adjusted/rotated yet for the black player.
        """

        def parse(c):
            fil, rank = ord(c[0]) - ord("a"), int(c[1]) - 1
            return A1 + fil - 10 * rank

        i, j, prom = (
            parse(move_in_uci[:2]),
            parse(move_in_uci[2:4]),
            move_in_uci[4:].upper(),
        )
        return Move(i, j, prom)

    def to_uci(self):
        # Convert the 120-board index to file and rank
        def index_to_uci(index):
            file = chr((index % 10) + ord("a") - 1)
            rank = str(8 - (index // 10 - 2))
            return file + rank

        from_square = index_to_uci(self.i)
        to_square = index_to_uci(self.j)
        promotion = self.prom.lower() if self.prom else ""

        return f"{from_square}{to_square}{promotion}"

    def rotate(self) -> "Move":
        return Move(119 - self.i, 119 - self.j, self.prom)


@dataclasses.dataclass()
class AbstractPosition:
    board: str  # a 120 char representation of the boardwc
    score: object  # int or neural network intermediate input
    white_castling_rights: tuple[bool, bool]
    black_castling_rights: tuple[bool, bool]
    enpassant_square: Optional[int]
    # King passant is the square the king just "jumped over" immedietly after castling.
    king_passant_square: int
    is_flipped_perspective: bool  # True when black is to move.
    king_is_captured: bool

    @classmethod
    def new_startpos(cls) -> "AbstractPosition":
        return cls.from_fen(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        )

    @classmethod
    def from_fen(cls, fen: str) -> "AbstractPosition":
        # MOSTLY AI GENERATED CODE.
        parts = fen.split()

        board = ["."] * 120
        # Fill spaces and newlines
        for i in range(120):
            if 21 <= i <= 98 and i % 10 != 0 and i % 10 != 9:
                # We're inside the board
                pass
            else:
                board[i] = "\n" if i % 10 == 9 else " "

        # Parse board position
        fen_board = parts[0]
        row, col = 0, 0
        for char in fen_board:
            if char == "/":
                row += 1
                col = 0
            elif char.isdigit():
                col += int(char)
            else:
                board[21 + row * 10 + col] = char
                col += 1

        board = "".join(board)

        # Parse castling rights
        white_castling = ("K" in parts[2], "Q" in parts[2])
        black_castling = ("k" in parts[2], "q" in parts[2])

        # Parse en passant square
        ep_square = None
        if parts[3] != "-":
            file, rank = parts[3]
            ep_square = 21 + (8 - int(rank)) * 10 + (ord(file) - ord("a"))

        position = cls(
            board=board,
            score=cls.get_score_from_board(board),
            white_castling_rights=white_castling,
            black_castling_rights=black_castling,
            enpassant_square=ep_square,
            king_passant_square=-100,
            is_flipped_perspective=False,
            king_is_captured=False,
        )
        return position if parts[1] == "w" else position.rotate()

    @property
    def evaluation(self) -> int:
        if self.king_is_captured:
            return -200000
        return self.score

    def gen_moves(self):
        # For each of our pieces, iterate through each possible 'ray' of moves,
        # as defined in the 'directions' map. The rays are broken e.g. by
        # captures or immediately in case of pieces such as knights.
        for i, p in enumerate(self.board):
            if not p.isupper():
                continue
            for d in directions[p]:
                for j in count(i + d, d):
                    q = self.board[j]
                    # Stay inside the board, and off friendly pieces
                    if q.isspace() or q.isupper():
                        break
                    # Pawn move, double move and capture
                    if p == "P":
                        if d in (N, N + N) and q != ".":
                            break
                        if d == N + N and (i < A1 + N or self.board[i + N] != "."):
                            break
                        if (
                            d in (N + W, N + E)
                            and q == "."
                            and j
                            not in (
                                self.enpassant_square,
                                self.king_passant_square,
                                self.king_passant_square - 1,
                                self.king_passant_square + 1,
                            )
                            # and j != self.ep and abs(j - self.kp) >= 2
                        ):
                            break
                        # If we move to the last row, we can be anything
                        if A8 <= j <= H8:
                            for prom in "NBRQ":
                                yield Move(i, j, prom)
                            break
                    # Move it
                    yield Move(i, j, "")
                    # Stop crawlers from sliding, and sliding after captures
                    if p in "PNK" or q.islower():
                        break
                    # Castling, by sliding the rook next to the king
                    if (
                        i == A1
                        and self.board[j + E] == "K"
                        and self.white_castling_rights[0]
                    ):
                        yield Move(j + E, j + W, "")
                    if (
                        i == H1
                        and self.board[j + W] == "K"
                        and self.white_castling_rights[1]
                    ):
                        yield Move(j + W, j + E, "")

    def rotate(self, nullmove=False):
        """Rotates the board, preserving enpassant, unless nullmove"""
        return type(self)(
            self.board[::-1].swapcase(),
            -self.score,
            self.black_castling_rights,
            self.white_castling_rights,
            119 - self.enpassant_square
            if self.enpassant_square and not nullmove
            else 0,
            119 - self.king_passant_square
            if self.king_passant_square and not nullmove
            else 0,
            not self.is_flipped_perspective,
            self.king_is_captured,
        )

    def move(self, move: Move):
        i, j, prom = dataclasses.astuple(move)
        p = self.board[i]

        def put(board, i, p):
            return board[:i] + p + board[i + 1 :]

        # Copy variables and reset ep and kp
        board = self.board
        wc, bc, ep, kp = self.white_castling_rights, self.black_castling_rights, 0, 0
        king_is_captured = self.check_captured_king(move)
        new_score = self.get_new_score(move)
        # Actual move
        board = put(board, j, board[i])
        board = put(board, i, ".")
        # Castling rights, we move the rook or capture the opponent's
        if i == A1:
            wc = (False, wc[1])
        if i == H1:
            wc = (wc[0], False)
        if j == A8:
            bc = (bc[0], False)
        if j == H8:
            bc = (False, bc[1])
        # Castling
        if p == "K":
            wc = (False, False)
            if abs(j - i) == 2:
                kp = (i + j) // 2
                board = put(board, A1 if j < i else H1, ".")
                board = put(board, kp, "R")
        # Pawn promotion, double move and en passant capture
        if p == "P":
            if A8 <= j <= H8:
                board = put(board, j, prom)
            if j - i == 2 * N:
                ep = i + N
            if j == self.enpassant_square:
                board = put(board, j + S, ".")
        # We rotate the returned position, so it's ready for the next player
        return type(self)(
            board,
            new_score,
            wc,
            bc,
            ep,
            kp,
            is_flipped_perspective=self.is_flipped_perspective,
            king_is_captured=king_is_captured,
        ).rotate()

    def check_captured_king(self, move: Move) -> bool:
        q = self.board[move.j]
        return q == "k" or abs(move.j - self.king_passant_square) < 2


class ManualEvalPosition(AbstractPosition):
    @classmethod
    def get_score_from_board(cls, board: str) -> int:
        score = sum(
            piece_square_tables[c][i] for i, c in enumerate(board) if c.isupper()
        )
        score -= sum(
            piece_square_tables[c.upper()][119 - i]
            for i, c in enumerate(board)
            if c.islower()
        )
        return score

    def get_new_score(self, move: Move) -> int:
        i, j, prom = move.i, move.j, move.prom
        p, q = self.board[i], self.board[j]
        # Actual move
        score_delta = piece_square_tables[p][j] - piece_square_tables[p][i]
        # Capture
        if q.islower():
            score_delta += piece_square_tables[q.upper()][119 - j]
        # Opponent's illegal castling detection
        if abs(j - self.king_passant_square) < 2:
            score_delta += piece_square_tables["K"][119 - j]
        # Castling (if we did it)
        if p == "K" and abs(i - j) == 2:
            score_delta += piece_square_tables["R"][(i + j) // 2]
            score_delta -= piece_square_tables["R"][A1 if j < i else H1]
        # Special pawn stuff
        if p == "P":
            if A8 <= j <= H8:
                score_delta += (
                    piece_square_tables[prom][j] - piece_square_tables["P"][j]
                )
            if j == self.enpassant_square:
                score_delta += piece_square_tables["P"][119 - (j + S)]
        return self.score + score_delta


def tanh(x):
    return math.tanh(x)

def forward_pass(
    one_hot_encoded_board: List[int],
    network_0_weights: List[List[float]],
    network_2_weights: List[List[float]],
    network_4_weights: List[List[float]],
    network_6_weights: List[float],
) -> float:
    # Layer 0
    layer_0_output = [sum(w * x for w, x in zip(weights, one_hot_encoded_board)) for weights in network_0_weights]
    layer_1_output = [tanh(x) for x in layer_0_output]

    # Layer 2
    layer_2_output = [sum(w * x for w, x in zip(weights, layer_1_output)) for weights in network_2_weights]
    layer_3_output = [tanh(x) for x in layer_2_output]

    # Layer 4
    layer_4_output = [sum(w * x for w, x in zip(weights, layer_3_output)) for weights in network_4_weights]
    layer_5_output = [tanh(x) for x in layer_4_output]

    # Layer 6
    final_output = sum(w * x for w, x in zip(network_6_weights, layer_5_output))
    return final_output


class NeuralNetworkEvalPosition(AbstractPosition):
    @staticmethod
    def one_hot_encode_board(board: str) -> List[int]:
        result = [0] * 768
        for board_offset in range(64):
            fil = board_offset % 8
            rank = board_offset // 8
            i = A1 + fil - 10 * rank
            c = board[i]
            piece_index = "PNBRQKpnbrqk".find(c)
            if piece_index >= 0:
                result[64 * piece_index + board_offset] = 1
        return result

    @classmethod
    def get_score_from_board(cls, board: str) -> List[float]:
        # Let's start without "efficiently updateable".
        return 12345  # Dummy

    def get_new_score(self, move: Move) -> int:
        # Let's start without "efficiently updateable".
        return 12345  # Dummy
    
    @property
    def evaluation(self) -> float:
        if self.king_is_captured:
            return -200000
        return forward_pass(
            self.one_hot_encode_board(self.board),
            neural_network_eval.network_0_weights,
            neural_network_eval.network_2_weights,
            neural_network_eval.network_4_weights,
            neural_network_eval.network_6_weights,
        )


Position = NeuralNetworkEvalPosition
