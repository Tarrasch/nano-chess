from position import Position
from search import search_with_time_constraints


def chess_bot(obs):
    """
    Simple chess bot that prioritizes checkmates, then captures, queen promotions, then randomly moves.

    Args:
        obs: An object with a 'board' attribute representing the current board state as a FEN string.

    Returns:
        A string representing the chosen move in UCI notation (e.g., "e2e4")
    """
    position = Position.from_fen(obs.board)
    # TODO: Change back time to 0.1
    search_result = search_with_time_constraints(position, suggested_time_for_move=10)
    best_move = search_result.move
    if position.is_flipped_perspective:
        best_move = best_move.rotate()  # type: ignore

    return best_move.to_uci()  # type: ignore
