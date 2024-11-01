from game import Sokoban

class Node:
	def __init__(self, state:Sokoban, parent: 'Node', actions, weight):
		self.state = state
		self.parent = parent
		self.actions = self.add_action(parent.actions if parent else [], actions)
		self.total_weight = (parent.total_weight if parent else 0) + weight
		self.key = self.generate_key()  # Tạo thuộc tính `key` cho node
	''' Hàm tạo khóa duy nhất cho mỗi node dựa trên trạng thái board '''
	def generate_key(self):
		return str(self.state.board)  # Biểu diễn board dưới dạng chuỗi để tạo khóa duy nhất
    

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
	   
