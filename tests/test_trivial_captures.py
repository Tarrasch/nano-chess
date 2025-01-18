import main
import search
from position import Position

def search_best_move_helper(fen: str, depth: int) -> str:
    color = fen.split()[1]
    return main.search_with_depth(Position.from_fen(fen), depth=depth, color=color)

class SimpleObs(object):
    def __init__(self, fen):
        self.board = fen


def test_capture_queen():
    assert main.chess_bot(SimpleObs("6k1/8/6K1/8/8/3q4/8/3R4 w - - 0 1")) == 'd1d3'
    assert main.chess_bot(SimpleObs("6K1/8/6k1/8/8/3Q4/8/3r4 b - - 0 1")) == 'd1d3'

def test_takes_free_pawn():
    assert search_best_move_helper("r5k1/1p3p1p/6p1/8/8/6P1/5P1P/1R4K1 w - - 0 1", depth=2) == 'b1b7'

def test_does_not_sacrifice_rook():
    assert main.chess_bot(SimpleObs("1r4k1/1p3p1p/6p1/8/8/6P1/5P1P/1R4K1 w - - 0 1")) != 'b1b7'

def test_does_not_sacrifice_rook_multiple_depths():
    assert search_best_move_helper("1r4k1/1p3p1p/6p1/8/8/6P1/5P1P/1R4K1 w - - 0 1", depth=2) != 'b1b7'
    assert search_best_move_helper("1r4k1/1p3p1p/6p1/8/8/6P1/5P1P/1R4K1 w - - 0 1", depth=2) != 'b1b7'
    assert search_best_move_helper("1r4k1/1p3p1p/6p1/8/8/6P1/5P1P/1R4K1 w - - 0 1", depth=3) != 'b1b7'
