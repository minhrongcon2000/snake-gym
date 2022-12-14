from collections import deque
import numpy as np
import random


class SnakeMove:
    LEFT = np.array([[0, -1]], dtype=int)
    RIGHT = np.array([[0, 1]], dtype=int)
    UP = np.array([[-1, 0]], dtype=int)
    DOWN = np.array([[1, 0]], dtype=int)
    
    
class SnakeComponent:
    SNAKE = 1
    FOOD = 2


class SnakeController:
    def __init__(self, n_rows, n_cols, random_state=None, debug=False):
        np.random.seed(random_state)
        self.debug = debug
        self.board_state = np.zeros((n_rows, n_cols), dtype=int)
        self.directions = np.array([SnakeMove.LEFT, SnakeMove.RIGHT, SnakeMove.UP, SnakeMove.DOWN])
        self.n_rows = n_rows
        self.n_cols = n_cols
        
        self.reset()
        
    def reset(self):
        self.board_state = np.zeros((self.n_rows, self.n_cols), dtype=int)
        
        # snake logic
        self.board_state[self.n_rows // 2 - 1, self.n_cols // 2 - 1] = SnakeComponent.SNAKE
        self.board_state[self.n_rows // 2 - 1, self.n_cols // 2 - 2] = SnakeComponent.SNAKE
        self.snake = np.array([(self.n_rows // 2 - 1, self.n_cols // 2 - 1), (self.n_rows // 2 - 1, self.n_cols // 2 - 2)])
        self.snake_dynamic = np.repeat(SnakeMove.RIGHT, len(self.snake), axis=0)
        self.event_queue = deque()

        # food logic
        self.spawn_food()
                    
    def trigger_event(self, movement):
        self.event_queue.append((movement, 0))
        
    def spawn_food(self):
        if not self.debug:
            self.food_x, self.food_y = random.choice(np.argwhere(self.board_state == 0))
        else:
            self.food_x, self.food_y = self.n_rows // 2 - 1, self.n_cols // 2
        self.board_state[self.food_x, self.food_y] = SnakeComponent.FOOD
        
    def propagate_event(self):
        count_event_propagate = 0
        max_count_event = len(self.event_queue)
        while count_event_propagate < max_count_event:
            movement, current_info_pos = self.event_queue.popleft()
            count_event_propagate += 1
            if current_info_pos < len(self.snake):
                self.snake_dynamic[current_info_pos] = movement
                current_info_pos += 1
                self.event_queue.append((movement, current_info_pos))
        
        
    def move(self, movement):
        future_movement = self.snake[0] + movement.flatten()
        eat_food = False
        if not (0 <= future_movement[0] < self.board_state.shape[0]) or not (0 <= future_movement[1] < self.board_state.shape[1]):
            return eat_food, False
        if np.any(self.snake_dynamic[0] + movement != np.zeros((1, 2))):
            self.trigger_event(movement)
            self.propagate_event()
            self.board_state[self.snake[:, 0], self.snake[:, 1]] = 0
            self.snake += self.snake_dynamic
            self.board_state[self.snake[:, 0], self.snake[:, 1]] = 1
            
            # grow snake if eat food
            if self.snake[0, 0] == self.food_x and self.snake[0, 1] == self.food_y:
                eat_food = True
                self.snake_dynamic = np.concatenate((self.snake_dynamic, self.snake_dynamic[-1:]), axis=0)
                new_block = self.snake[-1:] - self.snake_dynamic[-1:]
                self.snake = np.concatenate((self.snake, new_block), axis=0)
                self.spawn_food()
                
            return eat_food, not np.any((self.snake[0, 0] == self.snake[1:, 0]) & (self.snake[0, 1] == self.snake[1:, 1]))
        return eat_food, False
    
    def get_food_location(self):
        return self.food_x, self.food_y
    
    def get_snake_head(self):
        return self.snake[0, 0], self.snake[0, 1]
    
    def get_board_state(self):
        return self.board_state
    
    def get_summary_state(self):
        h, w = self.board_state.shape
        state = np.array([
            self.snake[0, 1] + 1 >= w or self.board_state[self.snake[0, 0], self.snake[0, 1] + 1] == 1, # danger to the right
            self.snake[0, 1] - 1 < 0 or self.board_state[self.snake[0, 0], self.snake[0, 1] - 1] == 1, # danger to the left
            self.snake[0, 0] + 1 >= h or self.board_state[self.snake[0, 0] + 1, self.snake[0, 1]] == 1, # danger below
            self.snake[0, 0] - 1 < 0 or self.board_state[self.snake[0, 0] - 1, self.snake[0, 1]] == 1, # danger above
            self.food_x > self.snake[0, 0], # is food below?
            self.food_x < self.snake[0, 0], # is food above?
            self.food_y > self.snake[0, 1], # is food right?
            self.food_y < self.snake[0, 1] # is food left?
        ], dtype=np.float32)
        return state
