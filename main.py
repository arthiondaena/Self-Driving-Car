import game
import pygame
import numpy as np
from collections import deque
import random, math
from ddqn_keras import DDQNAgent
import matplotlib.pyplot as plt

TOTAL_GAMETIME = 1000
N_EPISODES = 10000
REPLACE_TARGET = 50

pygame.init()

game = game.GameInfo()

ddqn_agent = DDQNAgent(gamma=0.99, n_actions=4, epsilon=0.8, epsilon_end=0.03, epsilon_dec=0.995, replace_target=REPLACE_TARGET, batch_size=512, input_dims=7)

# Try existing model
# ddqn_agent.load_model()

plt.xlabel('episodes')
plt.ylabel('reward gates')

fig = plt.figure()
ax = fig.gca()

episodesNo = []
reward_gates = []
ddqn_scores = []
eps_his = []

avg_time = 20

file = open("output.txt", "w")

def run():

  for e in range(N_EPISODES):

    game.reset()
    done = False
    score = 0
    counter = 0

    observation_, reward, done = game.step(0)
    observation = np.array(observation_)

    gtime = 0

    while not done:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          return
      # if e % 10 == 0:
      #   game.play_game()

      action = ddqn_agent.choose_action(observation)
      observation_, reward, done = game.step(action)
      observation_ = np.array(observation_)

      if game.get_time()>=30.0:
        done = True
      
      score += reward

      ddqn_agent.remember(observation, action, reward, observation_, int(done))
      observation = observation_
      ddqn_agent.learn()

      gtime += 1
      
    eps_his.append(ddqn_agent.epsilon)
    ddqn_scores.append(score)
    avg_score = np.mean(ddqn_scores[max(0, e-100):(e+1)])
    reward_gates.append(game.gates_passed())

    if e%avg_time==0 and e>0:
      plt.cla()
      episodesNo.append(e)
      reward_gates1 = np.array(reward_gates)
      reward_avg = np.array([[x.mean(), x.min(), x.max()]            
         for x in np.array_split(reward_gates1, reward_gates1.shape[0]/avg_time)])
      ax.plot(episodesNo, reward_avg[:, 0], label = "mean")
      ax.plot(episodesNo, reward_avg[:, 1], label = "min")
      ax.plot(episodesNo, reward_avg[:, 2], label = "max")
      plt.legend()
      plt.draw()
      plt.savefig("plot.png")

    if e % REPLACE_TARGET == 0 and e > REPLACE_TARGET:
      ddqn_agent.update_network_parameters()
    
    if e % 10 == 0 and e > 10:
      ddqn_agent.save_model()
      print("save model")
    
    print('episode: ', e, 'score: %.2f' % score,
          ' reward gates passed: ', game.gates_passed(),
          ' average score %.2f' % avg_score,
          ' epsilon: ', ddqn_agent.epsilon,
          ' memory size', ddqn_agent.memory.mem_cntr % ddqn_agent.memory.mem_size)
    with open('output.txt', 'a') as fw:
      fw.write(f"episode: {e}, score: {round(score, 2)}, reward gates passed: {game.gates_passed()}, average score: {round(avg_score, 2)}, time: {game.get_time()}, steps: {gtime}, epsilon: {ddqn_agent.epsilon}, memory size: {ddqn_agent.memory.mem_cntr % ddqn_agent.memory.mem_size}\n")
    ddqn_agent.decay_epsilon()

run()
