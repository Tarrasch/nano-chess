import search
from position import Position


def search_best_move_helper(fen: str, depth: int = 3) -> str:
    return search.search_with_depth(Position.from_fen(fen), depth=depth)


def test_mates_in_one_white_to_move():
    assert search_best_move_helper("6k1/8/6K1/8/8/8/8/3R4 w - - 0 1") == "d1d8"


def test_mates_in_one_black_to_move():
    assert search_best_move_helper("6K1/8/6k1/8/8/8/8/3r4 b - - 0 1") == "d1d8"


def test_en_passant_mate_white():
    assert search_best_move_helper("6kr/2K2R2/5R2/6Pp/6R1/8/8/8 w - h6 0 1") == "g5h6"


def test_en_passant_mate_black():
    assert search_best_move_helper("6KR/2k2r2/5r2/8/6pP/8/8/6r1 b - h3 0 1") == "g4h3"
