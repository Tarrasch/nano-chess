import dataclasses
import time
from position import Position, Move
from typing import Optional, Iterable

WINNING_SCORE = 150000
AT_LEAST_A_KING_UP_SCORE = 150000


@dataclasses.dataclass()
class SearchResult:
    depth: int  # Number of plies searched
    score: int  # Score from perspective of player to move.
    move: Move  # Best move generated at this depth


def search_with_time_constraints(
    position: Position, remaining_time_in_seconds: float
) -> SearchResult:
    # TODO Change to better types than floats marked as "_in_seconds"!
    start = time.time()
    think_time_in_seconds = min(
        remaining_time_in_seconds / 40, remaining_time_in_seconds / 2 - 1
    )
    for search_result in search_indefinetly(position=position):
        if time.time() - start > think_time_in_seconds * 0.8:
            return search_result


def search_indefinetly(position: Position) -> Iterable[SearchResult]:
    for depth in range(1, 1000):
        score, move = negamax(
            position, depth, -WINNING_SCORE - 100, WINNING_SCORE + 100
        )
        yield SearchResult(depth=depth, score=score, move=move)


def search_with_depth(position: Position, depth: int, color: str) -> str:
    """
    Selects the best move from the given game state using negamax search.

    Args:
        position: The current game state.
        depth: The maximum search depth.

    Returns:
        The best move found by negamax search.
    """
    _, best_move = negamax(position, depth, -WINNING_SCORE - 100, WINNING_SCORE + 100)
    if position.is_flipped_perspective:
        best_move = best_move.rotate()  # type: ignore
    # print("position_score = ", position_score)

    return best_move.to_uci()  # type: ignore


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
