import game
import pygame
import numpy as np
from collections import deque
import random, math
from ddqn_keras import DDQNAgent

TOTAL_GAMETIME = 1000
N_EPISODES = 10000
REPLACE_TARGET = 50

print('init')
pygame.init()

game = game.GameInfo()

GameTime = 100
GameHistory = []
renderFlag = True

ddqn_agent = DDQNAgent(gamma=0.99, n_actions=4, epsilon=1.00, epsilon_end=0.10, epsilon_dec=0.9999, replace_target=REPLACE_TARGET, batch_size=512, input_dims=7)

ddqn_scores = []
eps_his = []

def run():

  for e in range(N_EPISODES):

    game.reset()
    done = False
    score = 0
    counter = 0

    observation_, reward, done = game.step(0)
    observation = np.array(observation_)

    gtime = 0

    renderFlag = False

    while not done:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          return
      if e % 10 == 0:
        renderFlag = True
        game.play_game(render=False)
      else:
        game.play_game(render=False)

      action = ddqn_agent.choose_action(observation)
      observation_, reward, done = game.step(action)
      observation_ = np.array(observation_)
      # print(action)
      # print(game.computer_car.x, game.computer_car.y)
      # This is a countdown if no reward is collected in 100 ticks then done is True
      if score <= 0:
        counter += 1
        if counter > 100:
          done = True
      
      else:
        counter = 0
      
      score += reward

      ddqn_agent.remember(observation, action, reward, observation_, int(done))
      observation = observation_
      ddqn_agent.learn()

      gtime += 1
      print(game.rewards)

      if gtime >= TOTAL_GAMETIME:
        done = True
      
    eps_his.append(ddqn_agent.epsilon)
    ddqn_scores.append(score)
    avg_score = np.mean(ddqn_scores[max(0, e-100):(e+1)])

    if e % REPLACE_TARGET == 0 and e > REPLACE_TARGET:
      ddqn_agent.update_network_parameters()
    
    if e % 10 == 0 and e > 10:
      ddqn_agent.save_model()
      print("save model")
    
    print('episode: ', e, 'score: %.2f' % score,
          ' average score %.2f' % avg_score,
          ' epsilon: ', ddqn_agent.epsilon,
          ' memory size', ddqn_agent.memory.mem_cntr % ddqn_agent.memory.mem_size)

run()
