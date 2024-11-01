import heapq
import time
from .node import Node
from .support import *
from .game import Sokoban

def heuristic(state):
	total_distance = 0
	for stone in state.stone_map:
		min_distance = min(
			abs(stone[0] - sx) + abs(stone[1] - sy)
			for sx, sy in state.check_point_list
		)
		total_distance += min_distance
	return total_distance

def AStar(Sokoban : Sokoban):
	start_time = time.time()
	initial_memory = get_memory_usage()

	startNode = Node(Sokoban, None, [], 0)
	explored_set = set()
	frontier = []
	initial_f = startNode.total_weight + heuristic(startNode.state)
	heapq.heappush(frontier, (initial_f, 0, startNode))
	counter = 1

	while frontier:
		_, _, current_node = heapq.heappop(frontier)

		if current_node.state.check_win():
			end_time = time.time()
			final_memory = get_memory_usage()
			return (len(explored_set), current_node, end_time - start_time, final_memory - initial_memory)

		if current_node in explored_set:  # Kiểm tra toàn bộ node
			continue

		explored_set.add(current_node)

		valid_actions_list = current_node.state.get_next_actions()
		for action in valid_actions_list:
			action_type = action[0]
			action_seq = action[1]
			new_state, actions, weight = current_node.state.move(action_type, action_seq)
			new_node = Node(new_state, current_node, actions, weight)

			if new_node not in explored_set:
				f = new_node.total_weight + heuristic(new_node.state)
				heapq.heappush(frontier, (f, counter, new_node))
				counter += 1

		end_time = time.time()
		if end_time - start_time > TIME_OUT:
			return []

	print("Not Found\n")
	return []
