import main


class SimpleObs(object):
    def __init__(self, fen):
        self.board = fen


def test_mates_in_one_white_to_move():
    assert main.chess_bot(SimpleObs("6k1/8/6K1/8/8/8/8/3R4 w - - 0 1")) == "d1d8"
