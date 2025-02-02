import search
from position import Position


def search_best_move_helper(fen: str, depth: int = 3) -> str:
    color = fen.split()[1]
    return search.search_with_depth(Position.from_fen(fen), depth=depth, color=color)


def test_does_not_sacrifice_king():
    # https://lichess.org/editor/rn2k2r/ppp1ppbp/6p1/8/Q2P4/4PP1P/Pq3P2/R4K1R_b_kq_-_2_15?color=white
    fen = "r6r/p1pk2bp/4p1p1/1p6/4n1q1/8/7K/8 b - - 1 38"
    ok_moves = ["g7e5", "g7d4", "g4g3"]
    # assert search_best_move_helper(fen, depth=3) in ok_moves
    assert search_best_move_helper(fen, depth=5) in ok_moves
