from ddqn_torch import DQN
from gameenv import CustomEnv


env = CustomEnv()
agent = DQN(env, episodes=1000)

agent.train(show_graph=True, output=True)
