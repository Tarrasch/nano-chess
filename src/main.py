from position import Position, Move
from typing import Optional

WINNING_SCORE = 150000
AT_LEAST_A_KING_UP_SCORE = 150000


def negamax(
    position: Position, depth: int, alpha: int, beta: int
) -> tuple[int, Optional[Move]]:
    if abs(position.score) > AT_LEAST_A_KING_UP_SCORE:
        return position.score, None

    if depth <= 0:
        return position.score, None

    best_score = -1000000
    best_move = None
    for move in position.gen_moves():
        new_position = position.move(move)
        score = -negamax(new_position, depth - 1, -beta, -alpha)[0]
        if score > best_score:
            best_score = score
            best_move = move
        alpha = max(alpha, score)
        if alpha >= beta:
            break
    return best_score, best_move


def search_best_move(position: Position, depth: int, color: str) -> str:
    """
    Selects the best move from the given game state using negamax search.

    Args:
        position: The current game state.
        depth: The maximum search depth.

    Returns:
        The best move found by negamax search.
    """
    position_score, best_move = negamax(
        position, depth, -WINNING_SCORE - 100, WINNING_SCORE + 100
    )
    if color == "b":
        position_score = -position_score
        best_move = best_move.rotate()  # type: ignore
    print("position_score = ", position_score)

    return best_move.to_uci()  # type: ignore


def chess_bot(obs):
    """
    Simple chess bot that prioritizes checkmates, then captures, queen promotions, then randomly moves.

    Args:
        obs: An object with a 'board' attribute representing the current board state as a FEN string.

    Returns:
        A string representing the chosen move in UCI notation (e.g., "e2e4")
    """
    position = Position.from_fen(obs.board)
    color = obs.board.split()[1]
    print(position.board)
    return search_best_move(position, depth=3, color=color)
