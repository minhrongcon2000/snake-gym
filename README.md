# snake-gym

This package is my own implementation on Snake game with Gym integration.

## Usage

```python
import gym
import snake_gym_grid

env = gym.make("snake-gym-10x20-normal-v0")
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
- reward: 1.0 when a food is eaten, -1.0 if snake dies, 0.0 otherwise
- done: whether the snake dies
- truncate: whether the game is running for more than 100000 time steps
- info: an empty dictionary for now

## Env registration

- `snake-gym-grid-10x20-normal-v0`: Snake game with 10 x 20 board and 500 x 900 observation
- `snake-gym-grid-10x20-tiny-v0`: Snake game with 10 x 20 board and 80 x 80 observation
- `snake-gym-grid-10x20-1d-v0`: Snake game with 10 x 20 board and summarized observation. Observation in this case is vector `[dangerRight, dangerLeft, dangerBelow, dangerAbove, foodBelow, foodAbove, foodRight, foodLeft]`.

_Note_:

- `danger<Direction>` = neighbor block of snake head in the `<Direction>` is occupied by a snake body or is out of game board.

- `food<Direction>` = is the food in the `<Direction>` of the snake head?

- For any other environment, observation is the raw image from the game view. For tiny, the size is 80 x 80 and for normal, it's 500 x 900.

## Customize environment

Instead of using registered environment, one can utilize the built-in `SnakeGymGrid` class.

```python
# this import is kinda ugly but I have no choice but to follow the gym standard
from snake_gym_grid.envs.snake_gym_grid import SnakeGymGrid

env = SnakeGymGrid(width=..., height=..., n_rows=..., n_cols=...)
...
```
