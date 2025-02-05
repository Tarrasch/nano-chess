import search
from position import Position


def search_best_move_helper(fen: str, depth: int) -> str:
    return search.search_with_depth(Position.from_fen(fen), depth=depth)


def test_does_not_sacrifice_king():
    # https://lichess.org/editor/rn2k2r/ppp1ppbp/6p1/8/Q2P4/4PP1P/Pq3P2/R4K1R_b_kq_-_2_15?color=white
    fen = "rn2k2r/ppp1ppbp/6p1/8/Q2P4/4PP1P/Pq3P2/R4K1R b kq - 2 15"
    ok_moves = ["b8c6", "b7b5", "c7c6", "e8d8", "e8f8"]
    assert search_best_move_helper(fen, depth=2) in ok_moves
    assert search_best_move_helper(fen, depth=3) in ok_moves
