from .game import Sokoban
from .support import *

class Node:
	def __init__(self, state:Sokoban, parent: 'Node', actions, weight):
		self.state = state
		self.parent = parent
		self.actions = self.add_action(parent.actions if parent else [], actions)
		self.total_weight = (parent.total_weight if parent else 0) + weight
		
	def __hash__(self):
		# Use player's position and the sorted stone positions for a unique hash
		return hash((tuple(sorted(self.state.stone_map.items())), self.state.playerPos))

	def __eq__(self, other):
		if self.state.stone_map != other.state.stone_map:
			return False	
		
		if self.state.playerPos == other.state.playerPos:
			return True
		
		for stone_position in self.state.stone_map.keys():
			if is_adjacent(self.state.playerPos, stone_position) and\
				is_adjacent(other.state.playerPos, stone_position):
				return True

		return False
	
	''' RECURSIVE FUNCTION TO BACKTRACK TO THE FIRST IF THE CURRENT STATE IS GOAL '''
	def get_line(self):
		if self.parent is None:
			return [self.state.board]
		return (self.parent).get_line() + [self.state.board]
	def add_action(self, cur_action, next_action):
		# Initialize a copy of current actions list
		actions = list(cur_action)
		
		# Check if next_action is a list, and extend or append accordingly
		if isinstance(next_action, list):
			actions.extend(next_action)
		else:
			actions.append(next_action)
		
		return actions