import os
TIME_OUT = 1800

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


