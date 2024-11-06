import time
from .support import *
from .node import Node
from .game import Sokoban
from queue import *


def BFS(Sokoban: Sokoban):
	start_time = time.time()
	initial_memory = process_memory()


	startNode = Node(Sokoban, None, [], 0)

	explored_set = set()
	explored_set.add(startNode)
	frontier = Queue()
	frontier.put(startNode)

	
	while frontier.empty() is False:

		expand_node = frontier.get()

		valid_actions_list = expand_node.state.get_next_actions()
		for action in valid_actions_list:
			action_type = action[0]  
			action_seq = action[1]      
			new_state, actions, weight = expand_node.state.move(action_type, action_seq)
			new_node = Node(new_state, expand_node, actions, weight)
			
			if new_node in explored_set:
				continue
			if(new_node.state.is_least_one_box_in_corner() or new_node.state.is_stuck_all_stones()):
				explored_set.add(new_node)
				continue
			if new_node.state.check_win():
				final_memory = process_memory()
				end_time = time.time()		 
				
				return (len(explored_set), new_node, end_time - start_time, final_memory - initial_memory)
			
			explored_set.add(new_node)
			frontier.put(new_node)
			
			end_time = time.time()

			if end_time - start_time > TIME_OUT:
				return []
	return []
