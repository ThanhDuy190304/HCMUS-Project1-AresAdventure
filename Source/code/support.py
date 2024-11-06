import os
import psutil
TIME_OUT = 1800

# inner psutil function
def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss

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
                if char == '$':
                    stones.append((row, col))
                elif char == '.':
                    switches.append((row, col))
                elif char == '*':
                    stones.append((row, col))
                    switches.append((row, col))
                elif char == '+':
                    player_position = (row, col)
                    switches.append((row, col))
                elif char == '@':
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


