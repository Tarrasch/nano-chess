# See https://stackoverflow.com/a/24391977
import pstats
p = pstats.Stats('profile')
p.strip_dirs()
p.sort_stats('tottime')
p.print_stats(30)
