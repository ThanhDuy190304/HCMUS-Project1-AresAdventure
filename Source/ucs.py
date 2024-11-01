import heapq
import time
from node import Node
from support import *
from game import Sokoban
from queue import *

def UCS(Sokoban):
    start_time = time.time()
    startNode = Node(Sokoban, None, [], 0)

    explored_set = set()
    frontier = []
    heapq.heappush(frontier, (startNode.total_weight, 0, startNode))
    counter = 1

    while frontier:
        _, _, current_node = heapq.heappop(frontier)

        if current_node.state.check_win():
            print("Win\n")
            return (current_node.get_line(), len(explored_set), current_node)

        if current_node.key in explored_set:
            continue

        explored_set.add(current_node.key)

        valid_actions_list = current_node.state.get_next_actions()
        for action in valid_actions_list:
            action_type = action[0]
            action_seq = action[1]
            new_state, actions, weight = current_node.state.move(action_type, action_seq)
            new_node = Node(new_state, current_node, actions, weight)

            if new_node.key not in explored_set:
                heapq.heappush(frontier, (new_node.total_weight, counter, new_node))
                counter += 1

        end_time = time.time()
        if end_time - start_time > TIME_OUT:
            return []

    print("Not Found\n")
    return []
