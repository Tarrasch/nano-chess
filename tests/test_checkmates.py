import main


class SimpleObs(object):
    def __init__(self, fen):
        self.board = fen


def test_mates_in_one_white_to_move():
    assert main.chess_bot(SimpleObs("6k1/8/6K1/8/8/8/8/3R4 w - - 0 1")) == "d1d8"


def test_mates_in_one_black_to_move():
    assert main.chess_bot(SimpleObs("6K1/8/6k1/8/8/8/8/3r4 b - - 0 1")) == "d1d8"


def test_en_passant_mate_white():
    assert main.chess_bot(SimpleObs("6kr/2K2R2/5R2/6Pp/6R1/8/8/8 w - h6 0 1")) == "g5h6"


def test_en_passant_mate_black():
    assert main.chess_bot(SimpleObs("6KR/2k2r2/5r2/8/6pP/8/8/6r1 b - h3 0 1")) == "g4h3"
