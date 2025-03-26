from position import Position
import search

pos = Position.from_fen('rn2kb1r/ppp1qppp/3p1nb1/6B1/3NP3/2N2P2/PPP1B1PP/R2QK2R w KQkq - 3 9')

print(search.search_with_depth(pos, depth=4))