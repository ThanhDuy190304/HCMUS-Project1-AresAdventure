
from code.support import *
from code.game import Sokoban
import code.bfs as bfs
import code.astar as astar
import code.ucs as ucs
import code.dfs as dfs


def main():
    
    grid, stones, stone_weights, switches, player_position = read_maze_file('input/input_10.txt')
    check_points = find_list_check_point(grid)
    boxes_data = find_boxes_position(grid, stone_weights)

    game = Sokoban(grid, check_points, boxes_data)
    
    #result = bfs.BFS(game)
    # result = dfs.DFS(game)
    result = astar.AStar(game)
    # result = ucs.UCS(game)
    
    if result:
        num_checked_states, final_node, exe_time, exe_memory = result
        print("Number of Checked States:", num_checked_states)
        print("Player Info:")
        print("  Step Count:", len(final_node.actions))
        print("  Steps:", final_node.actions)
        print("  Total Weight:", final_node.total_weight)
        print(f"Execution Time: {exe_time:.4f} seconds")
        print(f"Memory Usage: {exe_memory} KB")
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()