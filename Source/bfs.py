import time
from support import *
from node import Node
from game import Sokoban
from queue import Queue

def BFS(Sokoban: Sokoban):
    start_time = time.time()
    startNode = Node(Sokoban, None, [], 0)

    explored_set = set()
    explored_set.add(startNode.key)  # Sử dụng key thay vì lưu toàn bộ đối tượng Node
    frontier = Queue()
    frontier.put(startNode)

    node_count = 1 

    while not frontier.empty():
        expand_node = frontier.get()

        valid_actions_list = expand_node.state.get_next_actions()
        for action in valid_actions_list:
            action_type = action[0]  
            action_seq = action[1]      
            new_state, actions, weight = expand_node.state.move(action_type, action_seq)
            new_node = Node(new_state, expand_node, actions, weight)

            # Kiểm tra nếu trạng thái mới đã được duyệt
            if new_node.key in explored_set:
                continue

            node_count += 1  # Increment state count
            
            # Kiểm tra điều kiện thắng
            if new_node.state.check_win():
                print("Win\n")
                return (new_node.get_line(), len(explored_set), new_node)
            
            explored_set.add(new_node.key)  # Thêm key của trạng thái mới vào explored_set
            frontier.put(new_node)

            # Kiểm tra giới hạn thời gian
            end_time = time.time()
            if end_time - start_time > TIME_OUT:
                return []

    print("Not Found\n")
    return []
