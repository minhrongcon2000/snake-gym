import gym
from gym import spaces
from gym.utils.renderer import Renderer
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


class SnakeGym(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array", "single_rgb_array"], "render_fps": 60}
    def __init__(self, render_mode=None):
        super().__init__()
        
        self.render_mode = render_mode
        self.width = 900
        self.height = 500
        
        self.n_rows = 10
        self.n_cols = 20
        controller = SnakeController(self.n_rows, self.n_cols)
        self.view = SnakeView(900, 500, controller)
        
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0, high=255, shape=(self.height, self.width, 3), dtype=np.uint8)
        
        self.possible_actions = [SnakeMove.LEFT, SnakeMove.RIGHT, SnakeMove.UP, SnakeMove.DOWN]
        self.render_rect_colors = [SnakeWindowColor.CELL_BORDER_COLOR, SnakeWindowColor.SNAKE_COLOR, SnakeWindowColor.FOOD_COLOR]
        self.widths = [-1, 0, 0]
        self.window = None
        self.num_steps = 0
        self.renderer = Renderer(self.render_mode, self._render_frame)
        
    def reset(self, seed=None, return_info = False, options=None):
        super().reset(seed=seed)
        self.num_steps = 0
        self.view.controller = SnakeController(self.n_rows, self.n_cols, random_state=seed)
        self.view.draw_game_view()
        observations = self.view.game_view
        observations = cv2.cvtColor(observations, cv2.COLOR_BGR2RGB)
        return observations
    
    def step(self, action):
        hasEatenFood, isAlive = self.view.move(self.possible_actions[action])
        observations = self.view.game_view
        observations = cv2.cvtColor(observations, cv2.COLOR_BGR2RGB)
        self.num_steps += 1
        return observations, float(hasEatenFood), not isAlive, {}
    
    def render(self, mode="human"):
        if mode is None:
            return self.renderer.get_renders()
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