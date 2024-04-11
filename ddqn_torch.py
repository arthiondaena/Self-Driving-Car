import gymnasium as gym
import math
import random
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple, deque
from itertools import count
import numpy as np

import torch
import torch.nn as nn 
import torch.optim as optim 
import torch.nn.functional as F 

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

is_ipython = 'inline' in matplotlib.get_backend()
if is_ipython:
  from IPython import display
plt.ion()

Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))

def plt_graph(scores, show_result = False):
  plt.figure(1)
  scores_t = torch.tensor(scores, dtype=torch.float)
  if show_result:
    plt.title('Result')
  else:
    plt.clf()
    plt.title('Training')
  plt.xlabel('Episode')
  plt.ylabel('Score')
  plt.plot(scores_t.numpy())

  if len(scores_t) >= 100:
    means = scores_t.unfold(0, 100, 1).mean(1).view(-1)
    means = torch.cat((torch.zeros(99), means))
    plt.plot(means.numpy())
  
  # pause a bit so that plots are updated
  plt.pause(0.001)
  if is_ipython:
    if not show_result:
      display.display(plt.gcf())
      display.clear_output(wait=True)
    else:
      display.display(plt.gcf())

class ReplayMemory():

  def __init__(self, capacity):
    self.memory = deque([], maxlen=capacity)

  def push(self, *args):
    self.memory.append(Transition(*args))
    
  def sample(self, batch_size):
    return random.sample(self.memory, batch_size)
  
  def __len__(self):
    return len(self.memory)

class Network(nn.Module):

  def __init__(self, n_observations, n_actions):
    super(Network, self).__init__()
    self.layer1 = nn.Linear(n_observations, 128)
    self.layer2 = nn.Linear(128, 128)
    self.layer3 = nn.Linear(128, n_actions)
  
  def forward(self, x):
    x = F.relu(self.layer1(x))
    x = F.relu(self.layer2(x))
    return self.layer3(x)
  
class DQN():

  def __init__(self, env, gamma=0.99, episodes=1000, batch_size=256, epsilon=0.9, epsilon_end=0.01, epsilon_dec=10000, tau=0.005, learning_rate=1e-4):
    self.env = env
    self.gamma = gamma
    self.episodes = episodes
    self.steps_done = 0
    self.batch_size = 256
    self.epsilon = epsilon
    self.epsilon_end = epsilon_end
    self.epsilon_dec = epsilon_dec
    self.tau = 0.005
    self.lr = learning_rate

    n_actions = self.env.action_space.n
    state, info = self.env.reset()
    n_observations = len(state)
    state, info = self.env.reset()

    # policy and target network
    self.policy_net = Network(n_observations, n_actions).to(device)
    self.target_net = Network(n_observations, n_actions).to(device)
    self.target_net.load_state_dict(self.policy_net.state_dict())

    self.optimizer = optim.AdamW(self.policy_net.parameters(), lr=self.lr, amsgrad=True)
    self.memory = ReplayMemory(25000)
  
  def choose_action(self, state):
    sample = random.random()
    epsilon = self.epsilon_end + (self.epsilon - self.epsilon_end) * \
        math.exp(-1. * self.steps_done / self.epsilon_dec)
    self.steps_done += 1
    if sample > epsilon:
      with torch.no_grad():
        # t.max(1) will return the largest column value of each row.
        # second column on max result is index of where max element was
        # found, so we pick action with the larger expected reward.
        return self.policy_net(state).max(1).indices.view(1, 1)
    else:
      return torch.tensor([[self.env.action_space.sample()]], device=device, dtype=torch.long)
  
  def best_action(self, state):
    with torch.no_grad():
      return self.policy_net(state).max(1).indices.view(1, 1)

  def optimize(self):
    if len(self.memory) < self.batch_size:
      return
    
    transitions = self.memory.sample(self.batch_size)

    # Transpose the batch. This converts batch-array of Transitions to 
    # Transitions of batch-arrays.
    batch = Transition(*zip(*transitions))

    # Compute a mask of non-final states and concatenate the batch elements
    # (a final state would've been the one after which simulation ended)
    non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                        batch.next_state)), device=device, dtype=torch.bool)
    non_final_next_states = torch.cat([s for s in batch.next_state if s is not None])

    state_batch = torch.cat(batch.state)
    action_batch = torch.cat(batch.action)
    reward_batch = torch.cat(batch.reward)

    # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
    # columns of actions taken. These are the actions which would've been taken
    # for each batch state according to policy_net
    q_eval = self.policy_net(state_batch).gather(1, action_batch)

    # Compute V(s_{t+1}) for all next states.
    # Expected values of actions for non_final_next_states are computed based
    # on the "older" target_net; selecting their best reward with max(1).values
    # This is merged based on the mask, such that we'll have either the expected
    # state value or 0 in case the state was final.
    v_next = torch.zeros(self.batch_size, device=device)
    with torch.no_grad():
      v_next[non_final_mask] = self.target_net(non_final_next_states).max(1).values
    
    # Compute the expected Q values
    q_expected = (v_next * self.gamma) + reward_batch

    # Compute Huber Loss
    criterion = nn.SmoothL1Loss()
    loss = criterion(q_eval, q_expected.unsqueeze(1))

    # Optimize the model
    self.optimizer.zero_grad()
    loss.backward()
    # In-place gradient clipping
    torch.nn.utils.clip_grad_value_(self.policy_net.parameters(), 100)
    self.optimizer.step()

  def train(self, output=False, show_graph=False, ouput=None):

    if output:
      file = open("output.txt", "w")

    scores = []

    for i in range(self.episodes):
      # Initialize the environment and get its state
      state, info = self.env.reset()
      state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
      score = 0
      
      for t in count():
        action = self.choose_action(state)
        observation, reward, terminated, truncated, _ = self.env.step(action.item())

        score += reward
        
        reward = torch.tensor([reward], device=device)
        done = terminated or truncated

        if terminated:
          next_state = None
        else:
          next_state = torch.tensor(observation, dtype=torch.float32, device=device).unsqueeze(0)

        self.memory.push(state, action, next_state, reward)

        state = next_state

        # Perfom one step of the optimization (on the policy network)
        self.optimize()

        # Soft update of the target network's weights
        # θ′ ← τ θ + (1 −τ )θ′
        target_net_state_dict = self.target_net.state_dict()
        policy_net_state_dict = self.policy_net.state_dict()
        for key in policy_net_state_dict:
          target_net_state_dict[key] = policy_net_state_dict[key]*self.tau + target_net_state_dict[key]*(1-self.tau)
        self.target_net.load_state_dict(target_net_state_dict)

        if done:
          scores.append(score)
          if show_graph:
            plt_graph(scores)
          if output:
            avg_score = np.mean(scores[max(0, i-100):(i+1)])
            with open('output.txt', 'a') as fw:
              fw.write(f"episode: {i}, score: {round(score, 2)}, reward gate: {self.env.game.gates_passed()}, average score: {round(avg_score, 2)}, steps: {t}\n")
          break

    self.save()

    if show_graph:
      plt_graph(scores, show_result=True)
      plt.ioff()
      plt.show()
  
  def save(self):
    torch.save(self.policy_net.state_dict(), 'policy.pt')
  
  def load(self):
    self.policy_net.load_state_dict(torch.load('policy.pt'))
    self.target_net.load_state_dict(torch.load('policy.pt'))
    self.policy_net.eval()
    self.target_net.eval()