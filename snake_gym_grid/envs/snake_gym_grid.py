import gym
from gym import spaces
from gym.error import DependencyNotInstalled
import numpy as np
from .controller import SnakeMove, SnakeController
import cv2

from .view import SnakeView


class SnakeWindowColor:
    BACKGROUND_COLOR = (255, 255, 255)
    FOOD_COLOR = (255, 0, 0)
    SNAKE_COLOR = (0, 0, 255)
    CELL_BORDER_COLOR = (0, 0, 0)


class SnakeGymGrid(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array", "single_rgb_array"], "render_fps": 60}
    def __init__(self, render_mode=None, seed=None, width=900, height=500, n_rows=10, n_cols=20, debug=False):
        super().__init__()
        self.seed = seed
        
        self.render_mode = render_mode
        self.width = width
        self.height = height
        
        self.n_rows = n_rows
        self.n_cols = n_cols
        controller = SnakeController(self.n_rows, self.n_cols, debug=debug)
        self.view = SnakeView(self.width, self.height, controller)
        
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0, high=255, shape=(self.height, self.width, 3), dtype=np.uint8)
        
        self.possible_actions = [SnakeMove.LEFT, SnakeMove.RIGHT, SnakeMove.UP, SnakeMove.DOWN]
        self.render_rect_colors = [SnakeWindowColor.CELL_BORDER_COLOR, SnakeWindowColor.SNAKE_COLOR, SnakeWindowColor.FOOD_COLOR]
        self.widths = [-1, 0, 0]
        self.window = None
        
    def reset(self):
        observations = self.view.reset()
        observations = cv2.cvtColor(observations, cv2.COLOR_BGR2RGB)
        return observations
    
    def step(self, action):
        hasEatenFood, isAlive = self.view.move(self.possible_actions[action])
        observations = self.view.game_view
        observations = cv2.cvtColor(observations, cv2.COLOR_BGR2RGB)
        if isAlive:
            return observations, float(hasEatenFood), not isAlive, {}
        return observations, -1, not isAlive, {}
    
    def render(self, mode="human"):
        return self._render_frame(mode)
    
    def _render_frame(self, mode="human"):
        assert mode in self.metadata["render_modes"]
        try:
            import pygame
        except ImportError:
            raise DependencyNotInstalled("pygame not install. Please run python3 -m pip install pygame==2.1.2")
        
        if mode == "human":
            pygame.init()
            pygame.display.init()
            
            self.clock = pygame.time.Clock()
            if self.window is None:
                self.window = pygame.display.set_mode((self.view.image_width, self.view.image_height))
            game_ui = pygame.surfarray.make_surface(self.view.game_view.transpose((1, 0, 2)))
            self.window.blit(game_ui, game_ui.get_rect())
            pygame.event.pump()
            pygame.display.update()
            self.clock.tick(self.metadata["render_fps"])
        else:
            return cv2.cvtColor(self.view.game_view, cv2.COLOR_BGR2RGB)
        
    def close(self):
        if self.window is not None:
            import pygame
            pygame.display.quit()
            pygame.quit()
            
    def get_food_location(self):
        return self.view.get_food_location()
    
    def get_snake_head(self):
        return self.view.get_snake_head()
    
    def get_board_state(self):
        return self.view.get_board_state()
    
class SnakeGymGrid1D(SnakeGymGrid):
    def __init__(self, render_mode=None, seed=None, width=900, height=500, n_rows=10, n_cols=20, debug=False):
        super().__init__(render_mode, seed, width, height, n_rows, n_cols, debug)
        self.observation_space = spaces.Box(low=1, high=1, shape=(8,), dtype=np.float32)
    
    def reset(self):
        super().reset()
        return self.view.get_summary_state()
    
    def step(self, action):
        _, reward, done, info = super().step(action)
        return self.view.get_summary_state(), reward, done, info

            
class SnakeGymGrid10x20Tiny(SnakeGymGrid):
    def __init__(self, render_mode=None, seed=None, debug=False):
        super().__init__(render_mode, seed, 80, 80, 10, 20, debug=debug)
        

class SnakeGymGrid10x20Normal(SnakeGymGrid):
    def __init__(self, render_mode=None, seed=None, debug=False):
        super().__init__(render_mode, seed, debug=debug)