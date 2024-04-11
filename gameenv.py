import gymnasium
from gymnasium import spaces
import numpy as np
import game

class CustomEnv(gymnasium.Env):
  """Custom Environment that follows gym interface"""
  metadata = {'render.modes': ['human']}

  def __init__(self, players: int = 1):
    super(CustomEnv, self).__init__()
    # Define action and observation space
    self.action_space = spaces.Discrete(4)
    self.observation_space = spaces.Box(low=0.0, high=201.0, shape=(8,), dtype=np.float64)
    self.current_step = 0
    self.num_resets = -1
    self.game = game.GameInfo(players)
    self.reset()

  def step(self, action, render=False):
    observation, reward, done = self.game.step(action, render)
    # self.game.play_game()
    info = self.game.gates_passed()
    truncated = False
    if self.game.get_time() >= 60.0:
      truncated = True
    self.current_step += 1
    return observation, reward, done, truncated, {}

  def reset(self, seed: int | None = None):
    self.game.reset()
    observation, _, _ = self.game.step(0)
    return observation, {}  # reward, done, info can't be included

  def _choose_next_state(self):
    self.state = self.action_space.sample()

  def render(self, mode='human'):
    if mode == 'human':
      self.game.play_game()

  def close (self):
    pass