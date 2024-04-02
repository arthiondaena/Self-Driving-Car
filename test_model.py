import game
import pygame
import numpy as np
from keras.activations import *

from ddqn_keras import DDQNAgent

from collections import deque
import random, math

TOTAL_GAMETIME = 10000
N_EPISODES = 10000
REPLACE_TARGET = 10

game = game.GameInfo()

GameTime = 0
GameHistory = []
renderFlag = True

ddqn_agent = DDQNAgent(gamma=0.995, n_actions=4, epsilon=0.1, epsilon_end=0.1, epsilon_dec=0.9999, replace_target=REPLACE_TARGET, batch_size=512, input_dims=7)

ddqn_agent.load_model()
ddqn_agent.update_network_parameters()

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
        game.play_game(render=True)
      else:
        game.play_game(render=True)

      action = ddqn_agent.choose_action(observation)
      observation_, reward, done = game.step(action)
      observation_ = np.array(observation_)
      if score <= 0:
        counter += 1
        if counter > 100:
          done = True
      
      else:
        counter = 0
      
      score += reward

      observation = observation_

      gtime += 1
      if gtime >= TOTAL_GAMETIME:
        done = True
    
    print('episode: ', e, 'score: %.2f' % score,
          ' reward gates passed: ', game.gates_passed(),
          ' ray distances ', game.calculate_rays(game.computer_car)
)

run()
