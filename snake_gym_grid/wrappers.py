import gym

class NoImprovementWrapper(gym.Wrapper):
    def __init__(self, env: gym.Env, max_no_eat_times=200):
        gym.Wrapper.__init__(self, env)
        self.max_no_eat_times = max_no_eat_times
        self.reset()
    
    def reset(self):
        self.no_food_times = 0
        return self.env.reset()
    
    def step(self, action):
        obs, reward, done, info = self.env.step(action)
        
        if reward == 0:
            self.no_food_times += 1
        else:
            self.no_food_times = 0
        
        if self.no_food_times == self.max_no_eat_times:
            done = True
        
        return obs, reward, done, info
