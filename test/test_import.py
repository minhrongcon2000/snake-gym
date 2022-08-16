import unittest

class TestImport(unittest.TestCase):
    REGISTERED_ENV = {
        "snake-gym-grid-10x20-tiny-v0",
        "snake-gym-grid-10x20-normal-v0"
    }
    
    def test_if_environment_is_registered(self):
        import gym
        import snake_gym_grid
        
        all_env_ids = set(env.id for env in gym.envs.registry.all())
        
        self.assertTrue(self.REGISTERED_ENV.issubset(all_env_ids))
        
