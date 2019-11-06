import sys
sys.path.append('search_algorithms/')
from functions import *
import BFS
# import functions


if __name__ == '__main__':
    import_map_image()
    cut()
    create_map()
    save_map()

    # Run BFS
    BFS.run_bfs()

    # Auto-keyboard typing to solve the puzzle
    import write
