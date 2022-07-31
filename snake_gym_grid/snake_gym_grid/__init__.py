from gym.envs.registration import register

register(
    id="snake-gym-grid-10x20-v0",
    entry_point="snake_gym_grid.snake_gym_grid.envs.snake_gym_grid:SnakeGymGrid10x20",
    max_episode_steps=100000,
    reward_threshold=199
)
