import dataclasses
import time
from position import Position, Move
from typing import Iterable, Optional

WINNING_SCORE = 150000


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
    position: Position, suggested_time_for_move: float
) -> SearchResult:
    start = time.time()
    for search_result in search_indefinetly(position=position):
        if time.time() - start > suggested_time_for_move * 0.05:
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

    return best_move.to_uci()  # type: ignore


def quiescence_search(
    position: Position, alpha: int, beta: int, last_captured_square: int
) -> int:
    # From https://www.chessprogramming.org/Quiescence_Search :)
    stand_pat = position.evaluation
    best_score = stand_pat
    if stand_pat >= beta:
        return stand_pat
    if alpha < stand_pat:
        alpha = stand_pat
    for move in position.gen_moves():
        if move.j != last_captured_square:
            continue
        new_position = position.move(move)
        child_score = -quiescence_search(
            new_position, -beta, -alpha, 119-last_captured_square
        )

        if child_score > best_score:
            best_score = child_score
        alpha = max(alpha, child_score)
        if alpha >= beta:
            break
    return best_score


def negamax(
    position: Position,
    depth: int,
    alpha: int,
    beta: int,
    last_captured_square: Optional[int] = None,
) -> SearchResult:
    if position.king_is_captured:
        return SearchResult.from_terminal_node(score=position.evaluation)
    if depth <= 0:
        if last_captured_square:
            return SearchResult.from_terminal_node(
                score=quiescence_search(
                    position, alpha, beta, last_captured_square=last_captured_square
                )
            )
        else:
            return SearchResult.from_terminal_node(score=position.evaluation)

    final_search_result = SearchResult(
        depth=depth, score=-1000000, nodes_visited=0, move=None
    )
    for move in position.gen_moves():
        is_capture = position.board[move.j].islower()
        new_position = position.move(move)
        last_captured_square = 119-move.j if is_capture else None
        child_search_result = negamax(
            new_position,
            depth - 1,
            -beta,
            -alpha,
            last_captured_square=last_captured_square,
        )
        final_search_result.nodes_visited += child_search_result.nodes_visited

        score = -child_search_result.score
        if score > final_search_result.score:
            final_search_result.score = score
            final_search_result.move = move
        alpha = max(alpha, score)
        if alpha >= beta:
            break
    return final_search_result
