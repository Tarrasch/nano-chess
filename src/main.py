from position import Position
from search import search_with_depth


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
    # TODO Change to search_with_time_constraints.
    return search_with_depth(position, depth=3, color=color)
