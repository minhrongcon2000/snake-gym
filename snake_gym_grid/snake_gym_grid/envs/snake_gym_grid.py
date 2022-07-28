import gym
from gym import spaces
from gym.utils.renderer import Renderer
import numpy as np
from .controller import SnakeMove, SnakeController
import cv2


class SnakeWindowColor:
    BACKGROUND_COLOR = (255, 255, 255)
    FOOD_COLOR = (255, 0, 0)
    SNAKE_COLOR = (0, 0, 255)
    CELL_BORDER_COLOR = (0, 0, 0)


class SnakeGym(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array", "single_rgb_array"], "render_fps": 4}
    def __init__(self, render_mode="human"):
        super().__init__()
        
        self.render_mode = render_mode
        self.width = 900
        self.height = 500
        
        self.n_rows = 10
        self.n_cols = 20
        self.controller = SnakeController(self.n_rows, self.n_cols)
        
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0, high=255, shape=(self.height, self.width, 3), dtype=np.uint8)
        
        self.possible_actions = [SnakeMove.LEFT, SnakeMove.RIGHT, SnakeMove.UP, SnakeMove.DOWN]
        self.render_rect_colors = [SnakeWindowColor.CELL_BORDER_COLOR, SnakeWindowColor.SNAKE_COLOR, SnakeWindowColor.FOOD_COLOR]
        self.widths = [-1, 0, 0]
        
        self.window = None
        
        if self.render_mode == "human":
            import pygame
            
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.width, self.height))
            self.clock = pygame.time.Clock()
            
        self.num_steps = 0
            
        self.renderer = Renderer(self.render_mode, self._render_frame)
        
    def reset(self, seed= None, return_info = False, options=None):
        import pygame
        super().reset(seed=seed)
        self.num_steps = 0
        self.controller = SnakeController(self.n_rows, self.n_cols, random_state=seed)
        self.renderer.reset()
        self.renderer.render_step()
        observations = np.transpose(pygame.surfarray.array3d(self.window), axes=(1, 0, 2))
        observations = cv2.cvtColor(observations, cv2.COLOR_BGR2RGB)
        return observations
    
    def step(self, action):
        import pygame
        hasEatenFood, isAlive = self.controller.move(self.possible_actions[action])
        self.renderer.render_step()
        observations = np.transpose(pygame.surfarray.array3d(self.window), axes=(1, 0, 2))
        observations = cv2.cvtColor(observations, cv2.COLOR_BGR2RGB)
        self.num_steps += 1
        return observations, float(hasEatenFood), not isAlive, self.num_steps == 100000, {}
    
    def render(self):
        return self.renderer.get_renders()
    
    def _render_frame(self, mode):
        assert mode is not None
        
        import pygame
        canvas = pygame.Surface((self.width, self.height))
        
        canvas.fill(SnakeWindowColor.BACKGROUND_COLOR)
        
        blockWidth = self.width // self.n_cols
        blockHeight = self.height // self.n_rows
        for x in range(0, self.width, blockWidth):
            for y in range(0, self.height, blockHeight):
                rect = pygame.Rect(x, y, blockWidth, blockHeight)
                logic_value = self.controller.board_state[y // blockHeight, x // blockWidth]
                pygame.draw.rect(canvas, self.render_rect_colors[logic_value], rect, self.widths[logic_value])
                pygame.draw.rect(canvas, SnakeWindowColor.CELL_BORDER_COLOR, rect, 1)
                
        if mode == "human":
            assert self.window is not None
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()
            self.clock.tick(self.metadata["render_fps"])
        else:
            return np.transpose(pygame.surfarray.array3d(canvas), axes=(1, 0, 2))
        
    def close(self):
        if self.window is not None:
            import pygame
            pygame.display.quit()
            pygame.quit()
            
if __name__ == "__main__":
    env = SnakeGym(render_mode="human")
    observations = env.reset()
    done = False
    while not done:
        env.render()
        observations, _, done, _ = env.step(0)
    env.close()