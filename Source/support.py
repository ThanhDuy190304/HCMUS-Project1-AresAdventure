from game import Sokoban
from node import Node
import os

TIME_OUT = 1800


''' CHECK WHETHER THE BOARD ALREADY EXISTED IN THE TRAVERSED LIST'''
def is_node_exist(node: Node, explored_set: set[Node]) -> bool:
    '''Return True if the board already exists in the list of states, with the player adjacent to a stone in the same configuration.'''
    
    def is_adjacent(pos1, pos2):
        '''Check if pos1 is adjacent to pos2 (up, down, left, right).'''
        return (
            (pos1[0] == pos2[0] + 1 and pos1[1] == pos2[1]) or  # Below
            (pos1[0] == pos2[0] - 1 and pos1[1] == pos2[1]) or  # Above
            (pos1[0] == pos2[0] and pos1[1] == pos2[1] + 1) or  # Right
            (pos1[0] == pos2[0] and pos1[1] == pos2[1] - 1)     # Left
        )
    
    player_position = node.state.playerPos
    stone_map = node.state.stone_map
    
    for existing_node in explored_set :
        if stone_map == existing_node.state.stone_map:
            other_player_position = existing_node.state.playerPos
            if(player_position == other_player_position): return True
            # Check if the player's position in both states is adjacent to any stone
            for stone_position in stone_map.keys():
                if is_adjacent(player_position, stone_position) and is_adjacent(other_player_position, stone_position):
                    return True
                    
    return False

def get_memory_usage():
    process = os.popen('wmic process where "ProcessId={}" get WorkingSetSize'.format(os.getpid()))
    memory = process.read().strip().split('\n')
    
    for line in memory:
        if line.strip().isdigit():
            return int(line.strip()) // 1024  
    return 0

def read_maze_file(file_path):
    with open(file_path, 'r') as file:
        stone_weights = list(map(int, file.readline().strip().split()))
        
        grid = []
        stones = []
        switches = []
        player_position = None
        
        for row, line in enumerate(file):
            grid_row = list(line.strip())
            grid.append(grid_row)
            for col, char in enumerate(grid_row):
                if char == '$':  # Viên đá không trên công tắc
                    stones.append((row, col))
                elif char == '.':  # Công tắc không có đá
                    switches.append((row, col))
                elif char == '*':  # Viên đá trên công tắc
                    stones.append((row, col))
                    switches.append((row, col))
                elif char == '+':  # Ares trên công tắc
                    player_position = (row, col)
                    switches.append((row, col))
                elif char == '@':  # Ares không trên công tắc
                    player_position = (row, col)
                    
    return grid, stones, stone_weights, switches, player_position

def find_list_check_point(grid):
    check_points = []
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == '.' or grid[row][col] == '*' or grid[row][col] == '+':
                check_points.append([row, col])
    return check_points

def find_boxes_position(grid, stone_weights):
    boxes = {}
    stone_index = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if (grid[row][col] == '$' or grid[row][col] == '*') and stone_index < len(stone_weights):
                boxes[(row, col)] = stone_weights[stone_index]
                stone_index += 1
    return boxes

def print_board(board, file):
	for row in board:
		file.write(' '.join(row) + '\n')
	file.write('\n')  # Add a blank line for better separation between prints
