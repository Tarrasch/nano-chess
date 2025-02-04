from manual_eval import piece_square_tables
from position import A1, H1, A8, H8
from position import AbstractPosition, Move


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
