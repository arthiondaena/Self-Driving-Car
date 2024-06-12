import torch
from gameenv import CustomEnv
from ddqn_torch import DQN

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

env = CustomEnv(players=1)
agent = DQN(env)
agent.load()

def play():
  state, info = env.reset()
  state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
  score = 0

  while True:
      action = agent.best_action(state)
      observation, reward, terminated, truncated, _ = env.step(action.item(), render=True)
      score += reward
      reward = torch.tensor([reward], device=device)
      done = terminated or truncated
      print("score: ",score,sep='',end="\r",flush=True)

      if truncated:
          next_state, info = env.reset()
          next_state = torch.tensor(next_state, dtype=torch.float32, device=device).unsqueeze(0)
          score = 0

      else:
          next_state = torch.tensor(observation, dtype=torch.float32, device=device).unsqueeze(0)
      
      state = next_state
      env.render()

play()