import unittest
import cv2


class TestRewardImplementation(unittest.TestCase):
    def test_penalty_for_tiny_case(self):
        import gym
        import snake_gym_grid
        
        env = gym.make("snake-gym-grid-10x20-tiny-v0")
        done = False
        env.reset()
        reward = 0
        while not done:
            _, reward, done, _ = env.step(1)
            
        self.assertEqual(reward, -1)
    
    def test_penalty_for_normal_case(self):
        import gym
        import snake_gym_grid
        
        env = gym.make("snake-gym-grid-10x20-normal-v0")
        done = False
        env.reset()
        reward = 0
        while not done:
            _, reward, done, _ = env.step(1)
            
        self.assertEqual(reward, -1)
        
    def test_die_if_going_in_opposite_direction(self):
        import gym
        import snake_gym_grid
        
        env = gym.make("snake-gym-grid-10x20-normal-v0")
        done = False
        env.reset()
        _, reward, done, _ = env.step(0)
            
        self.assertEqual(reward, -1)
        self.assertTrue(done)
        
        env.reset()
        env.step(1)
        _, reward, done, _ = env.step(0)
        self.assertEqual(reward, -1)
        self.assertTrue(done)
        
        env.reset()
        env.step(2)
        _, reward, done, _ = env.step(3)
        self.assertEqual(reward, -1)
        self.assertTrue(done)
        
        env.reset()
        env.step(3)
        _, reward, done, _ = env.step(2)
        self.assertEqual(reward, -1)
        self.assertTrue(done)
        
    def test_reward_when_snake_eats_food(self):
        import gym
        import snake_gym_grid
        
        env = gym.make("snake-gym-grid-10x20-normal-v0", debug=True)
        env.reset()
        _, reward, _, _ = env.step(1)
        
        self.assertEqual(reward, 1)
        
        env = gym.make("snake-gym-grid-10x20-tiny-v0", debug=True)
        env.reset()
        _, reward, _, _ = env.step(1)
        
        self.assertEqual(reward, 1)
        