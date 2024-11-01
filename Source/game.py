from copy import deepcopy

class Sokoban:

    PLAYER_SYMBOL = '@'  # Symbol for the player
    OBSTACLES = ['#', '*', '$']  # Symbols for obstacles
    WALLS = '#'
    STONE_SYMBOL = '$'  # Symbol for a stone
    SWITCH_SYMBOL = '.'  # Symbol for a switch
    SWITCHED_STONE_SYMBOL = '*' # Symbol for a stone placed on a switch
    EMPTY_SYMBOL = ' ' #Symbol for a empty placed on a switch
    SWITCHED_PLAYER_SYMBOL = '+'# Symbol for a player placed on a switch
    def __init__(self, board, check_point_list, stone_map):
        self.board = board
        self.check_point_list = check_point_list
        self.stone_map = stone_map
        self.playerPos = self.find_position_player()
        self.heuristic = ... 


    def find_position_player(self):
        '''return position of player in board'''
        for x in range(len(self.board)):
            for y in range(len(self.board[0])):
                if self.board[x][y] == self.PLAYER_SYMBOL or\
                    self.board[x][y] == self.SWITCHED_PLAYER_SYMBOL:
                    return (x,y)
        return (-1,-1)  # error board

    def check_win(self):
        for p in self.check_point_list:
            if self.board[p[0]][p[1]] != self.SWITCHED_STONE_SYMBOL:
                return False
        return True

    def is_board_can_not_win(self):
        '''Return True if at least one box is stuck in a corner of walls, meaning the game can't be won.'''
        for stone_pos in self.stone_map:  # Iterate through each stone position
            x, y = stone_pos
            if self.board[x][y] != self.SWITCHED_STONE_SYMBOL and self.is_stone_in_corner(stone_pos):  # Check if the stone is in a corner
                return True
        return False

    def is_stone_in_corner(self, stone_pos):
        x, y = stone_pos  # Unpack the stone position

        # Ensure we don't go out of bounds of the board
        if x < 0 or x >= len(self.board) or y < 0 or y >= len(self.board[0]):
            return False

        # Check for walls on the left and right of the stone position
        left_wall = (y > 0 and self.board[x][y - 1] == self.WALLS)
        right_wall = (y < len(self.board[0]) - 1 and self.board[x][y + 1] == self.WALLS)
        
        # Check for walls above and below the stone position
        top_wall = (x > 0 and self.board[x - 1][y] in self.WALLS)
        bottom_wall = (x < len(self.board) - 1 and self.board[x + 1][y] == self.WALLS)

        # A stone is in a corner if two adjacent sides are walls
        if (left_wall and bottom_wall) or (left_wall and top_wall) or \
        (right_wall and bottom_wall) or (right_wall and top_wall):
            return True

        return False
    
    def is_stuck_all_stones(self):
        for stone_pos in self.stone_map:  
            x, y = stone_pos  # Unpack the stone position

            # Ensure we don't go out of bounds of the board
            if x < 0 or x >= len(self.board) or y < 0 or y >= len(self.board[0]):
                return False

            # Check for walls on the left and right of the stone position
            left_wall = (y > 0 and self.board[x][y - 1] in self.OBSTACLES)
            right_wall = (y < len(self.board[0]) - 1 and self.board[x][y + 1] in self.OBSTACLES)
            
            # Check for walls above and below the stone position
            top_wall = (x > 0 and self.board[x - 1][y] in self.OBSTACLES)
            bottom_wall = (x < len(self.board) - 1 and self.board[x + 1][y] in self.OBSTACLES)

            # A stone is in a corner if two adjacent sides are walls
            if not((left_wall and bottom_wall) or (left_wall and top_wall) or \
            (right_wall and bottom_wall) or (right_wall and top_wall)):
                return False
        return True

    def is_stone_on_check_point(self, stone_pos):
        return stone_pos in self.check_point_list

    def is_free_pos(self, positions):
        """Check if all specified positions are free (not a wall '#' or stone '$', '*') and within board limits."""
        for x, y in positions:
            # Check if the position is within the bounds of the board
            if x < 0 or x >= len(self.board) or y < 0 or y >= len(self.board[0]):
                return False  # Position is out of bounds
            # Check if the position is free
            if self.board[x][y] in self.OBSTACLES:
                return False  # Position is blocked by wall or stone
        return True  # All positions are free

    ''' GET THE NEXT POSSIBLE MOVE '''
    def get_push_actions_above_stone(self, x, y):
        categorized_actions = {
            'push-above-stone': []  # Actions that involve pushing above stone
        }

        if x - 1 >= 0 and (self.board[x - 1][y] == self.STONE_SYMBOL or 
                           self.board[x - 1][y] == self.SWITCHED_STONE_SYMBOL):
            # Push stone up
            if x - 2 >= 0 and self.board[x - 2][y] not in self.OBSTACLES:
                categorized_actions['push-above-stone'].append(['U'])

            # Push stone left
            if self.is_free_pos([(x, y + 1), (x - 1, y + 1), (x - 1, y - 1)]):
                categorized_actions['push-above-stone'].append(['r', 'u', 'L'])

            # Push stone right
            if self.is_free_pos([(x, y - 1), (x - 1, y - 1), (x - 1, y + 1)]):
                categorized_actions['push-above-stone'].append(['l', 'u', 'R'])

            # Push stone down from right
            if self.is_free_pos([(x, y + 1), (x - 1, y + 1), (x - 2, y + 1), (x - 2, y)]):
                categorized_actions['push-above-stone'].append(['r', 'u', 'u', 'l', 'D'])

            # Push stone down from left
            elif self.is_free_pos([(x, y - 1), (x - 1, y - 1), (x - 2, y - 1), (x - 2, y)]):
                categorized_actions['push-above-stone'].append(['l', 'u', 'u', 'r', 'D'])

        return categorized_actions

    def get_push_actions_below_stone(self, x, y):
        categorized_actions = {
            'push-below-stone': []  # Actions that involve pushing below stone
        }

        if x + 1 < len(self.board) and (self.board[x + 1][y] == self.STONE_SYMBOL 
                                        or self.board[x + 1][y] == self.SWITCHED_STONE_SYMBOL):
            # Push stone down
            if x + 2 < len(self.board) and self.board[x + 2][y] not in self.OBSTACLES:
                categorized_actions['push-below-stone'].append(['D'])

            # Push stone left
            if self.is_free_pos([(x, y + 1), (x + 1, y + 1), (x + 1, y - 1)]):
                categorized_actions['push-below-stone'].append(['r', 'd', 'L'])

            # Push stone right
            if self.is_free_pos([(x, y - 1), (x + 1, y - 1), (x + 1, y + 1)]):
                categorized_actions['push-below-stone'].append(['l', 'd', 'R'])

            # Push stone up from right
            if self.is_free_pos([(x, y + 1), (x + 1, y + 1), (x + 2, y + 1), (x + 2, y)]):
                categorized_actions['push-below-stone'].append(['r', 'd', 'd', 'l', 'U'])

            # Push stone up from left
            elif self.is_free_pos([(x, y - 1), (x + 1, y - 1), (x + 2, y - 1), (x + 2, y)]):
                categorized_actions['push-below-stone'].append(['l', 'd', 'd', 'r', 'U'])

        return categorized_actions

    def get_push_actions_left_stone(self, x, y):
        categorized_actions = {
            'push-left-stone': []  # Actions that involve pushing left stone
        }

        if y - 1 >= 0 and (self.board[x][y - 1] == self.STONE_SYMBOL or
                                    self.board[x][y - 1] == self.SWITCHED_STONE_SYMBOL):
            # Push stone left
            if y - 2 >= 0 and self.board[x][y - 2] not in self.OBSTACLES:
                categorized_actions['push-left-stone'].append(['L'])

            # Push stone up
            if self.is_free_pos([(x + 1, y), (x + 1, y - 1), (x - 1, y - 1)]):
                categorized_actions['push-left-stone'].append(['d', 'l', 'U'])

            # Push stone down
            if self.is_free_pos([(x - 1, y), (x - 1, y - 1), (x + 1, y - 1)]):
                categorized_actions['push-left-stone'].append(['u', 'l', 'D'])

            # Push stone right from up
            if self.is_free_pos([(x - 1, y), (x - 1, y - 1), (x - 1, y - 2), (x, y - 2)]):
                categorized_actions['push-left-stone'].append(['u', 'l', 'l', 'd', 'R'])

            # Push stone right from down
            elif self.is_free_pos([(x + 1, y), (x + 1, y - 1), (x + 1, y - 2), (x, y - 2)]):
                categorized_actions['push-left-stone'].append(['d', 'l', 'l', 'u', 'R'])

        return categorized_actions

    def get_push_actions_right_stone(self, x, y):
        categorized_actions = {
            'push-right-stone': [] # Actions that involve pushing right stone
        }

        if y + 1 < len(self.board[0]) and (self.board[x][y + 1] == self.STONE_SYMBOL
                                           or self.board[x][y+1] == self.SWITCHED_STONE_SYMBOL):
            # Push stone right
            if y + 2 < len(self.board[0]) and self.board[x][y + 2] not in self.OBSTACLES:
                categorized_actions['push-right-stone'].append(['R'])

            # Push stone up
            if self.is_free_pos([(x + 1, y), (x + 1, y + 1), (x - 1, y + 1)]):
                categorized_actions['push-right-stone'].append(['d', 'r', 'U'])

            # Push stone down
            if self.is_free_pos([(x - 1, y), (x - 1, y + 1), (x + 1, y + 1)]):
                categorized_actions['push-right-stone'].append(['u', 'r', 'D'])

            # Push stone left from up
            if self.is_free_pos([(x - 1, y), (x - 1, y + 1), (x - 1, y + 2), (x, y + 2)]):
                categorized_actions['push-right-stone'].append(['u', 'r', 'r', 'd', 'L'])

            # Push stone left from down
            elif self.is_free_pos([(x + 1, y), (x + 1, y + 1), (x + 1, y + 2), (x, y + 2)]):
                categorized_actions['push-right-stone'].append(['d', 'r', 'r', 'u', 'L'])

        return categorized_actions

    def get_next_actions(self):

        if(self.is_board_can_not_win() or self.is_stuck_all_stones()):
            return []
        
        '''Return list of positions that player can move to from current position'''
        x, y = self.playerPos
        actions_with_push = []

        # Retrieve push actions from all directions and extend the actions_with_push list if not empty
        push_above_actions = self.get_push_actions_above_stone(x, y)
        if push_above_actions['push-above-stone']:
            actions_with_push.extend([('push-above-stone', action) for action in push_above_actions['push-above-stone']])

        push_below_actions = self.get_push_actions_below_stone(x, y)
        if push_below_actions['push-below-stone']:
            actions_with_push.extend([('push-below-stone', action) for action in push_below_actions['push-below-stone']])

        push_left_actions = self.get_push_actions_left_stone(x, y)
        if push_left_actions['push-left-stone']:
            actions_with_push.extend([('push-left-stone', action) for action in push_left_actions['push-left-stone']])

        push_right_actions = self.get_push_actions_right_stone(x, y)
        if push_right_actions['push-right-stone']:
            actions_with_push.extend([('push-right-stone', action) for action in push_right_actions['push-right-stone']])


        frees = []  # Initialize a list for free moves
        for dx, dy, action in [(-1, 0, 'u'), (1, 0, 'd'), (0, -1, 'l'), (0, 1, 'r')]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < len(self.board) and 0 <= new_y < len(self.board[0]) and self.board[new_x][new_y] in [self.SWITCH_SYMBOL, self.EMPTY_SYMBOL]:
                frees.append(('free', action))  # Add the action directly to the list

        return actions_with_push + frees     

    ''' MOVE THE BOARD IN CERTAIN DIRECTIONS '''
    def push_above_stone(self, new_board, new_stone_map, action_sequence: list):

        cur_stone_pos = (self.playerPos[0] - 1, self.playerPos[1])
        last_action = action_sequence[-1] 

        if last_action == 'U':
            x = self.playerPos[0] - 2
            y = self.playerPos[1] 
        elif last_action == 'D':
            x = self.playerPos[0]
            y = self.playerPos[1] 
        elif last_action == 'R':
            x = self.playerPos[0] - 1
            y = self.playerPos[1] + 1
        elif last_action == 'L':
            x = self.playerPos[0] - 1
            y = self.playerPos[1] - 1

        if(self.is_stone_on_check_point([x, y])):
            new_board[x][y] = self.SWITCHED_STONE_SYMBOL
        else: new_board[x][y] = self.STONE_SYMBOL

        new_stone_map[(x, y)] = new_stone_map.pop(cur_stone_pos)
        new_board[cur_stone_pos[0]][cur_stone_pos[1]] = self.PLAYER_SYMBOL
        return new_stone_map.get((x, y))

    def push_right_stone(self, new_board, new_stone_map, action_sequence: list):

        cur_stone_pos = (self.playerPos[0], self.playerPos[1] + 1)
        last_action = action_sequence[-1]
        if last_action == 'U':
            x = self.playerPos[0] - 1
            y = self.playerPos[1] + 1
        elif last_action == 'D':
            x = self.playerPos[0] + 1 
            y = self.playerPos[1] + 1
        elif last_action == 'R':
            x = self.playerPos[0]
            y = self.playerPos[1] + 2
        elif last_action == 'L':
            x = self.playerPos[0]
            y = self.playerPos[1]

        if(self.is_stone_on_check_point([x, y])):
            new_board[x][y] = self.SWITCHED_STONE_SYMBOL
        else: new_board[x][y] = self.STONE_SYMBOL

        new_stone_map[(x, y)] = new_stone_map.pop(cur_stone_pos)
        new_board[cur_stone_pos[0]][cur_stone_pos[1]] = self.PLAYER_SYMBOL
        return new_stone_map.get((x, y))

    def push_below_stone(self, new_board, new_stone_map, action_sequence: list):

        cur_stone_pos = (self.playerPos[0] + 1, self.playerPos[1])

        last_action = action_sequence[-1]
        if last_action == 'U':
            x = self.playerPos[0] 
            y = self.playerPos[1]
        elif last_action == 'D':
            x = self.playerPos[0] + 2
            y = self.playerPos[1]
        elif last_action == 'R':
            x = self.playerPos[0] + 1
            y = self.playerPos[1] + 1
        elif last_action == 'L':
            x = self.playerPos[0] + 1
            y = self.playerPos[1] - 1

        if(self.is_stone_on_check_point([x, y])):
            new_board[x][y] = self.SWITCHED_STONE_SYMBOL
        else: new_board[x][y] = self.STONE_SYMBOL

        new_stone_map[(x, y)] = new_stone_map.pop(cur_stone_pos)
        new_board[cur_stone_pos[0]][cur_stone_pos[1]] = self.PLAYER_SYMBOL
        return new_stone_map.get((x, y))

    def push_left_stone(self, new_board, new_stone_map, action_sequence: list):
        cur_stone_pos = (self.playerPos[0], self.playerPos[1] - 1)
        last_action = action_sequence[-1]
        if last_action == 'U':
            x = self.playerPos[0] - 1
            y = self.playerPos[1] - 1
        elif last_action == 'D':
            x = self.playerPos[0] + 1
            y = self.playerPos[1] - 1
        elif last_action == 'R':
            x = self.playerPos[0]
            y = self.playerPos[1]
        elif last_action == 'L':
            x = self.playerPos[0]
            y = self.playerPos[1] - 2

        if(self.is_stone_on_check_point([x, y])):
            new_board[x][y] = self.SWITCHED_STONE_SYMBOL
        else: new_board[x][y] = self.STONE_SYMBOL

        new_stone_map[(x, y)] = new_stone_map.pop(cur_stone_pos)
        new_board[cur_stone_pos[0]][cur_stone_pos[1]] = self.PLAYER_SYMBOL
        return new_stone_map.get((x, y))

    def move_free(self, new_board, action):

        x, y = self.playerPos
        
        if action == 'u':
            new_x, new_y = x - 1, y
        elif action == 'd':
            new_x, new_y = x + 1, y
        elif action == 'l':
            new_x, new_y = x, y - 1
        elif action == 'r':
            new_x, new_y = x, y + 1

        new_board[new_x][new_y] = self.PLAYER_SYMBOL

    def move(self, action_type: str, actions):

        new_board = [row[:] for row in self.board]
        new_stone_map = deepcopy(self.stone_map)
        weight = 0

        new_board[self.playerPos[0]][self.playerPos[1]] = self.EMPTY_SYMBOL
        if action_type == 'push-above-stone':
            weight = self.push_above_stone(new_board, new_stone_map, actions)
        elif action_type == 'push-below-stone':
            weight = self.push_below_stone(new_board, new_stone_map, actions)
        elif action_type == 'push-left-stone':
            weight = self.push_left_stone(new_board, new_stone_map, actions)
        elif action_type == 'push-right-stone':
            weight = self.push_right_stone(new_board, new_stone_map, actions)
        elif action_type == 'free':
            self.move_free(new_board, actions)
        
        for p in self.check_point_list:
            if new_board[p[0]][p[1]] == self.EMPTY_SYMBOL:
                new_board[p[0]][p[1]] = self.SWITCH_SYMBOL

        return Sokoban(new_board, self.check_point_list, new_stone_map), actions, weight