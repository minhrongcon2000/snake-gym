from gym.envs.registration import register

register(
    id="snake-gym-10x20-v0",
    entry_point="snake_gym.envs.snake_gym:SnakeGym",
    max_episode_steps=100000,
    reward_threshold=199
)
