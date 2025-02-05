import search
from position import Position


def search_best_move_helper(fen: str, depth: int = 3) -> str:
    return search.search_with_depth(Position.from_fen(fen), depth=depth)


def test_does_not_move_into_pawn_capture():
    # from_kaggle_validator: https://www.kaggleusercontent.com/episodes/66611496.json
    for depth in range(2, 4):
        assert search_best_move_helper(
            "r1b1r1k1/1ppp1p2/4pR2/p5p1/4P3/P1K1P1P1/1P4PP/1R6 w - - 2 25",
            depth=depth,
        ) not in ["c3b4"]