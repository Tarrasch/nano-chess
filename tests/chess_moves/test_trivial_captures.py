import search
from position import Position


def search_best_move_helper(fen: str, depth: int = 3) -> str:
    color = fen.split()[1]
    return search.search_with_depth(Position.from_fen(fen), depth=depth, color=color)


class SimpleObs(object):
    def __init__(self, fen):
        self.board = fen


def test_capture_queen():
    assert search_best_move_helper("6k1/8/6K1/8/8/3q4/8/3R4 w - - 0 1") == "d1d3"
    assert search_best_move_helper("6K1/8/6k1/8/8/3Q4/8/3r4 b - - 0 1") == "d1d3"


def test_takes_free_pawn():
    assert (
        search_best_move_helper("r5k1/1p3p1p/6p1/8/8/6P1/5P1P/1R4K1 w - - 0 1", depth=2)
        == "b1b7"
    )


def test_does_not_sacrifice_rook():
    assert (
        search_best_move_helper("1r4k1/1p3p1p/6p1/8/8/6P1/5P1P/1R4K1 w - - 0 1")
        != "b1b7"
    )


def test_does_not_sacrifice_rook_multiple_depths():
    assert (
        search_best_move_helper(
            "1r4k1/1p3p1p/6p1/8/8/6P1/5P1P/1R4K1 w - - 0 1", depth=2
        )
        != "b1b7"
    )
    assert (
        search_best_move_helper(
            "1r4k1/1p3p1p/6p1/8/8/6P1/5P1P/1R4K1 w - - 0 1", depth=3
        )
        != "b1b7"
    )


def test_does_not_blunder_queen():
    # https://lichess.org/UUYDLpDv/white#9 (first time I played agianst the "NNUE")
    for depth in range(2, 5):
        assert search_best_move_helper(
            "r1b1kbnr/pppp1ppp/n7/4N3/1q1PP3/2P5/PP3PPP/RNBQKB1R b KQkq - 0 5",
            depth=depth,
        ) in ["b4a5", "b4b6", "b4d6", "b4e7"]
