import dataclasses
import time
from position import Position, Move
from typing import Iterable

WINNING_SCORE = 150000
HAS_CERTAINLY_CAPTURED_KING_SCORE = 150000


@dataclasses.dataclass()
class SearchResult:
    depth: int  # Maximum number of plies left for this node.
    score: int  # Score from perspective of player to move.
    nodes_visited: int  # The number of time we evaluated
    move: Move  # Best move generated at this depth

    @staticmethod
    def from_terminal_node(score: int) -> "SearchResult":
        return SearchResult(depth=None, score=score, nodes_visited=1, move=None)


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
        yield negamax(position, depth, -WINNING_SCORE - 100, WINNING_SCORE + 100)


def search_with_depth(position: Position, depth: int, color: str) -> str:
    """
    Selects the best move from the given game state using negamax search.

    Only for internal use.

    Args:
        position: The current game state.
        depth: The maximum search depth.

    Returns:
        The best move found by negamax search.
    """
    search_result = negamax(position, depth, -WINNING_SCORE - 100, WINNING_SCORE + 100)
    best_move = search_result.move
    if position.is_flipped_perspective:
        best_move = best_move.rotate()  # type: ignore
    # print("position_score = ", position_score)

    return best_move.to_uci()  # type: ignore


def negamax(position: Position, depth: int, alpha: int, beta: int) -> SearchResult:
    king_is_captured = abs(position.score) > HAS_CERTAINLY_CAPTURED_KING_SCORE
    if king_is_captured or depth <= 0:
        return SearchResult.from_terminal_node(score=position.score)

    final_search_result = SearchResult(
        depth=depth, score=-1000000, nodes_visited=0, move=None
    )
    for move in position.gen_moves():
        new_position = position.move(move)
        child_search_result = negamax(new_position, depth - 1, -beta, -alpha)
        final_search_result.nodes_visited += child_search_result.nodes_visited

        score = -child_search_result.score
        if score > final_search_result.score:
            final_search_result.score = score
            final_search_result.move = move
        alpha = max(alpha, score)
        if alpha >= beta:
            break
    return final_search_result
