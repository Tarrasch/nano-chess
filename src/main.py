from Chessnut import Game
from piece_square_tables import piece_square_tables

WINNING_SCORE = 20000


def evaluate_position(game, remaining_depth):
    """
    Evaluate score relative to the side that's moving.
    """
    if game.status == Game.CHECKMATE:
        return -WINNING_SCORE-remaining_depth
    elif game.status == Game.STALEMATE:
        return 0
    piece_values = {"P": 100, "N": 320, "B": 330, "R": 500, "Q": 900, "K": 0}
    whites_score = 0

    for i in range(64):
        piece = game.board.get_piece(i)
        if piece != " ":
            piece_color = 1 if piece.isupper() else -1
            piece_type = piece.upper()

            # Material score
            whites_score += piece_color * piece_values[piece_type]

            # Positional score
            if piece_color == 1:  # White piece
                whites_score += piece_square_tables[piece_type][i]
            else:  # Black piece
                whites_score -= piece_square_tables[piece_type][63 - i]

    return whites_score * (1 if game.state.player == "w" else -1)


def negamax(game: Game, depth: int, alpha: int, beta: int) -> tuple[int, str]:
    if (depth <= 0) or game.status in (Game.CHECKMATE, Game.STALEMATE):
        return evaluate_position(game, remaining_depth=depth), 'undefined'

    best_score = -1000000
    best_move = "undefined"
    for move in game.get_moves():
        new_game = Game(game.get_fen())
        new_game.apply_move(move)
        score = -negamax(new_game, depth - 1, -beta, -alpha)[0]
        if score > best_score:
            best_score = score
            best_move = move
        alpha = max(alpha, score)
        if alpha >= beta:
            break
    return best_score, best_move


def search_best_move(game: Game, depth: int) -> str:
    """
    Selects the best move from the given game state using negamax search.

    Args:
        game: The current game state.
        depth: The maximum search depth.

    Returns:
        The best move found by negamax search.
    """
    _, best_move = negamax(game, depth, -WINNING_SCORE-100, WINNING_SCORE+100)

    return best_move


def chess_bot(obs):
    """
    Simple chess bot that prioritizes checkmates, then captures, queen promotions, then randomly moves.

    Args:
        obs: An object with a 'board' attribute representing the current board state as a FEN string.

    Returns:
        A string representing the chosen move in UCI notation (e.g., "e2e4")
    """
    game = Game(obs.board)
    return search_best_move(game, depth=3)
