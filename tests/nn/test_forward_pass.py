from position import InefficientNeuralNetworkEvalPosition as nn_pos_class
from position import one_hot_encode_board
import numpy as np


def test_one_hot_encode_board():
    # https://lichess.org/editor/6K1/8/6k1/8/8/8/8/8_w_-_-_0_1?color=white
    pos = nn_pos_class.from_fen("6K1/8/6k1/8/8/8/8/8 w - - 0 1")
    answer = sum([[0] * 64 * 5, [0] * 62, [1, 0], [0] * 64 * 5, [0] * 46, [1], [0] * 17], start=[])
    assert np.array_equal(one_hot_encode_board(pos.board), answer)


def test_reasonable_score_starting_position():
    pos = nn_pos_class.new_startpos()
    assert -100 < pos.evaluation and pos.evaluation < 100

def test_reasonable_score_white_queen_up():
    # https://lichess.org/editor/4k3/p2p4/1bp1pp2/1p6/8/6N1/QPPPPPP1/4K3_w_-_-_0_1?color=white
    pos = nn_pos_class.from_fen("4k3/p2p4/1bp1pp2/1p6/8/6N1/QPPPPPP1/4K3 w - - 0 1")
    assert pos.evaluation > 300
    assert pos.evaluation < 3000 # It should not exaggerate the value of the queen!

def test_reasonable_score_white_queen_up_2():
    # https://lichess.org/UUYDLpDv/white#9 (first time I played agianst the "NNUE")
    pos = nn_pos_class.from_fen("r1b1kbnr/ppp2ppp/n2p4/4N3/1P1PP3/8/PP3PPP/RNBQKB1R b KQkq - 0 6")
    # It's bad for the player to move.
    assert pos.evaluation < -300
    assert pos.evaluation > -3000 # It should not exaggerate the value of the queen!
    

def test_reasonable_score_black_rook_up():
    # https://lichess.org/editor/r3k3/p2p4/1bp1pp2/1p6/8/6N1/1PPPPPP1/4K3_w_-_-_0_1?color=white
    pos = nn_pos_class.from_fen("r3k3/p2p4/1bp1pp2/1p6/8/6N1/1PPPPPP1/4K3 w - - 0 1")
    assert pos.evaluation < -200
    assert pos.evaluation > -2000 # It should not exaggerate the value of the rook!
    
def test_reasonable_score_black_rook_up_black_to_move():
    # https://lichess.org/editor/r3k3/p2p4/1bp1pp2/1p6/8/6N1/1PPPPPP1/4K3_w_-_-_0_1?color=white
    pos = nn_pos_class.from_fen("r3k3/p2p4/1bp1pp2/1p6/8/6N1/1PPPPPP1/4K3 b - - 0 1")
    # We add a minus sign because the evaluation is from the perspective of the white player
    assert -pos.evaluation < -200
    assert -pos.evaluation > -2000 # It should not exaggerate the value of the rook!
    
