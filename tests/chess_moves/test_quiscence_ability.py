import search
from position import Position


def search_best_move_helper(fen: str, depth: int = 3) -> str:
    color = fen.split()[1]
    return search.search_with_depth(Position.from_fen(fen), depth=depth, color=color)


# "rnbqkbnr/ppp3pp/8/3p1p2/3P4/8/PPPNQPPP/R1B1KBNR b KQkq - 1 5"


def test_does_not_do_random_knight_sacrifice():
    # Happened for me in game https://lichess.org/aW8CJaWR/black#14
    assert search_best_move_helper(
        "rn1qk1nr/pp3ppp/2pbp1b1/3pN3/3P2P1/2N4B/PPP1PP1P/R1BQ1RK1 w kq - 2 8",
        depth=3,
    ) not in [
        "c3d5",
        "e5g6",  # This move is often acceptable, but let's ensure it's not having the idea of just taking it later.
    ]