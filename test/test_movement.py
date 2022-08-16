import unittest

class TestImport(unittest.TestCase):
    REGISTERED_ENV = {
        "snake-gym-grid-10x20-tiny-v0",
        "snake-gym-grid-10x20-normal-v0"
    }
    
    def test_move_right(self):
        import gym
        import snake_gym_grid
        
        env = gym.make("snake-gym-grid-10x20-normal-v0")
        prev_snake_x, prev_snake_y = env.get_snake_head()
        MOVE_RIGHT = 1
        env.reset()
        env.step(MOVE_RIGHT)
        snake_x, snake_y = env.get_snake_head()
        
        self.assertEqual(snake_y - prev_snake_y, 1)
        self.assertEqual(prev_snake_x, snake_x)
        
    def test_move_up(self):
        import gym
        import snake_gym_grid
        
        env = gym.make("snake-gym-grid-10x20-normal-v0")
        prev_snake_x, prev_snake_y = env.get_snake_head()
        MOVE_UP = 2
        env.reset()
        env.step(MOVE_UP)
        snake_x, snake_y = env.get_snake_head()
        
        self.assertEqual(snake_y, prev_snake_y)
        self.assertEqual(snake_x - prev_snake_x, -1)
    
    def test_move_down(self):
        import gym
        import snake_gym_grid
        
        env = gym.make("snake-gym-grid-10x20-normal-v0")
        prev_snake_x, prev_snake_y = env.get_snake_head()
        MOVE_DOWN = 3
        env.reset()
        env.step(MOVE_DOWN)
        snake_x, snake_y = env.get_snake_head()
        
        self.assertEqual(snake_y, prev_snake_y)
        self.assertEqual(snake_x - prev_snake_x, 1)
    
    def test_move_left(self):
        import gym
        import snake_gym_grid
        
        env = gym.make("snake-gym-grid-10x20-normal-v0")
        MOVE_UP = 2
        MOVE_LEFT = 0
        env.reset()
        env.step(MOVE_UP)
        prev_snake_x, prev_snake_y = env.get_snake_head()
        env.step(MOVE_LEFT)
        snake_x, snake_y = env.get_snake_head()
        
        self.assertEqual(snake_y - prev_snake_y, -1)
        self.assertEqual(snake_x, prev_snake_x)
        
    def test_move_south_east(self):
        import gym
        import snake_gym_grid
        
        env = gym.make("snake-gym-grid-10x20-normal-v0")
        MOVE_UP = 2
        MOVE_RIGHT = 1
        env.reset()
        prev_snake_x, prev_snake_y = env.get_snake_head()
        env.step(MOVE_UP)
        env.step(MOVE_RIGHT)
        snake_x, snake_y = env.get_snake_head()
        
        self.assertEqual(snake_y - prev_snake_y, 1)
        self.assertEqual(snake_x - prev_snake_x, -1)
    
    def test_move_south_west(self):
        import gym
        import snake_gym_grid
        
        env = gym.make("snake-gym-grid-10x20-normal-v0")
        MOVE_UP = 2
        MOVE_LEFT = 0
        env.reset()
        prev_snake_x, prev_snake_y = env.get_snake_head()
        env.step(MOVE_UP)
        env.step(MOVE_LEFT)
        snake_x, snake_y = env.get_snake_head()
        
        self.assertEqual(snake_y - prev_snake_y, -1)
        self.assertEqual(snake_x - prev_snake_x, -1)
    
    def test_move_north_east(self):
        import gym
        import snake_gym_grid
        
        env = gym.make("snake-gym-grid-10x20-normal-v0")
        MOVE_DOWN = 3
        MOVE_RIGHT = 1
        env.reset()
        prev_snake_x, prev_snake_y = env.get_snake_head()
        env.step(MOVE_DOWN)
        env.step(MOVE_RIGHT)
        snake_x, snake_y = env.get_snake_head()
        
        self.assertEqual(snake_y - prev_snake_y, 1)
        self.assertEqual(snake_x - prev_snake_x, 1)
    
    def test_move_north_west(self):
        import gym
        import snake_gym_grid
        
        env = gym.make("snake-gym-grid-10x20-normal-v0")
        MOVE_DOWN = 3
        MOVE_LEFT = 0
        env.reset()
        
        prev_snake_x, prev_snake_y = env.get_snake_head()
        env.step(MOVE_DOWN)
        env.step(MOVE_LEFT)
        snake_x, snake_y = env.get_snake_head()

        self.assertEqual(snake_y - prev_snake_y, -1)
        self.assertEqual(snake_x - prev_snake_x, 1)
        
        
