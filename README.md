# snake-gym

This package is my own implementation on Snake game with Gym integration.

## Usage

```python
import gym
import snake_gym_grid.snake_gym_grid

env = gym.make("snake-gym-10x20-v0")
env.reset()

done = False # whether the snake dies

"""
action ranges from 0 to 3.
0 - LEFT
1 - RIGHT
2 - UP
3 - DOWN
"""
action = ...

observation = env.reset()

while not done:
    env.render()
    observation, reward, done, info = env.step(action)
env.close()
```

## Output at each time step

- observation: Pixel image of the game
- reward: 1.0 when a food is eaten 0.0 otherwise
- done: whether the snake dies
- truncate: whether the game is running for more than 100000 time steps
- info: an empty dictionary for now

## Customize environment

Instead of using registered environment, one can utilize the built-in `SnakeGymGrid` class.

```python
# this import is kinda ugly but I have no choice but to follow the gym standard
from snake_gym_grid.snake_gym_grid.envs.snake_gym_grid import SnakeGymGrid

env = SnakeGymGrid(width=..., height=..., n_rows=..., n_cols=...)
...
```
