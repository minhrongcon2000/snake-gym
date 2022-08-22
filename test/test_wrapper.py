import unittest


class TestWrapper(unittest.TestCase):
    def test_no_improve_wrapper(self):
        import gym
        import snake_gym_grid
        from snake_gym_grid.wrappers import NoImprovementWrapper
        
        env = gym.make("snake-gym-grid-10x20-normal-v0")
        env = NoImprovementWrapper(env, max_no_eat_times=10)
        
        env.reset()
        done = False
        i = 0
        moves = [1, 2, 0, 3]
        while not done:
            self.assertLessEqual(i, 10)
            _, _, done, _ = env.step(moves[i % 4])
            i += 1