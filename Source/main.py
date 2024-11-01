import time
import bfs 
from support import *



def main():

    
    grid, stones, stone_weights, switches, player_position = read_maze_file('input_01.txt')
    check_points = find_list_check_point(grid)
    boxes_data = find_boxes_position(grid, stone_weights)
    print(grid)
    print("Danh sách các điểm cần đặt đá (check_points):")
    print(check_points)

    print("\nThông tin về các viên đá (boxes_data):")
    print(boxes_data)

    print("Vị trí của nhân vật:", player_position)


    game = Sokoban(grid, check_points, boxes_data)
    
    # Bắt đầu đo thời gian
    start_time = time.time()

    # Bắt đầu đo bộ nhớ
    initial_memory = get_memory_usage()

    result = bfs.BFS(game)  # Lưu kết quả trả về từ BFS

    # Kết thúc đo thời gian
    end_time = time.time()
    
    # Đo bộ nhớ sau khi thực thi
    final_memory = get_memory_usage()

    # In ra thông tin trả về
    if result:
        final_state_path, num_checked_states, final_node = result
        print("Final State Path:")
        for board_state in final_state_path:
            for row in board_state:
                print(' '.join(row))
            print()  # Dòng trống giữa các trạng thái
        
        print("Number of Checked States:", num_checked_states)
        print("Player Info:")
        print("  Step Count:", len(final_node.actions))
        print("  Steps:", final_node.actions)
        print("  Total Weight:", final_node.total_weight)
    else:
        print("No solution found.")
    
    # In ra thời gian thực thi và bộ nhớ sử dụng
    print(f"Execution Time: {end_time - start_time:.4f} seconds")
    print(f"Memory Usage: {final_memory - initial_memory} KB")

if __name__ == "__main__":
    main()