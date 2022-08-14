from gym.envs.registration import register

register(
    id="snake-gym-grid-10x20-tiny-v0",
    entry_point="snake_gym_grid.snake_gym_grid.envs.snake_gym_grid:SnakeGymGrid10x20Tiny",
    max_episode_steps=1000000,
    reward_threshold=198
)

register(
    id="snake-gym-grid-10x20-normal-v0",
    entry_point="snake_gym_grid.snake_gym_grid.envs.snake_gym_grid:SnakeGymGrid10x20Normal",
    max_episode_steps=1000000,
    reward_threshold=198
)
