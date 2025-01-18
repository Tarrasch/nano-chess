from position import Position, Move


def test_initial_position():
    pos = Position.new_startpos()

    assert pos.board.count("P") == 8
    assert pos.board.count("p") == 8


def test_white_up_by_pawn_after_latvian_gambit():
    pos = Position.new_startpos()
    pos = pos.move(Move.from_uci("e2e4"))
    pos = pos.move(Move.from_uci("f7f5").rotate())
    pos = pos.move(Move.from_uci("e4f5"))
    pos = pos.rotate()

    assert pos.board.count("P") == 8
    assert pos.board.count("p") == 7
