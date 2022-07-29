from .controller import SnakeController
import numpy as np


class SnakeView:
    def __init__(self, 
                 image_width: int, 
                 image_height: int, 
                 controller: SnakeController):
        self.image_width = image_width
        self.image_height = image_height
        self.controller = controller
        self.n_rows, self.n_cols = self.controller.board_state.shape
        self.create_game_materials()
        self.draw_game_view()
        
    def create_game_materials(self):
        self.grid_height = self.image_height // self.n_rows
        self.grid_width = self.image_width // self.n_cols
        
        self.normal_ceil = np.zeros((self.grid_height, self.grid_width, 3), dtype=np.uint8)
        self.snake_ceil = np.zeros((self.grid_height, self.grid_width, 3), dtype=np.uint8)
        self.food_ceil = np.zeros((self.grid_height, self.grid_width, 3), dtype=np.uint8)
        
        # normal ceil is a white square covered by black border
        self.normal_ceil[1:-1, 1:-1, :] = 255
        
        # snake ceil is a blue square covered by black border
        self.snake_ceil[1:-1, 1:-1, 2] = 255
        
        # food ceil is a red square with black cover
        self.food_ceil[1:-1, 1:-1, 0] = 255
        
    def draw_game_view(self):
        self.game_view = np.tile(self.normal_ceil, (self.n_rows, self.n_cols, 1))
        for x, y in self.controller.snake:
            self.game_view[x * self.grid_height:(x + 1) * self.grid_height, y * self.grid_width:(y + 1) * self.grid_width, :] = self.snake_ceil
        self.game_view[self.controller.food_x * self.grid_height:(self.controller.food_x + 1) * self.grid_height, self.controller.food_y * self.grid_width:(self.controller.food_y + 1) * self.grid_width, :] = self.food_ceil
        
    def move(self, direction):
        hasEatenFood, hasDied = self.controller.move(direction)
        self.draw_game_view()
        return hasEatenFood, hasDied