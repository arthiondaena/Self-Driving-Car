# Self Driving Car using Deep Q-learning Network (DQN)

## Introduction
This is a Pytorch implementation of DQN Agent

In this project, I represent a simple self-driving car using the DQN algorithm

## Gameplay
### Agent
<img src = imgs/Agent.gif>

### Agent vs Player
<img src = imgs/AgentVsPlayer.gif>

## Neural Network
<img src = imgs/model.png>

- __Input Layer (states)__ - represents the distance of the car from the track boundaries on 7 different angles from left to right and the 8th value represents the speed of the car.

- __Hidden Layers__ - consists of two hidden layers, each layer containing 128 neurons.

- __Output Layer (actions)__ - represents the actions the agent takes based on the calculation of the NN.
  - Three possible actions are: left, right, and brake.

## Brief introduction to DQN
## Deep Q-Network (DQN)

DQN is a type of reinforcement learning algorithm that utilizes deep neural networks to help an agent learn the best course of action within an environment.

**Here's the gist:**

1. The agent interacts with the environment (think video game) and gathers experiences. These experiences include the state it was in, the action it took, the reward it received, and the new state it transitioned to.
2. DQN utilizes a technique called experience replay. It stores these experiences in a memory buffer, allowing the agent to learn from them even after they occur.
3. A deep neural network, called the Q-network, estimates the Q-value for each state-action pair. The Q-value signifies the expected future reward the agent can obtain by taking a specific action in a particular state.
4. The DQN trains by updating the Q-network's estimates using experiences from the replay memory. It adjusts the network to make its Q-value predictions more accurate over time.
5. Once trained, the agent leverages the Q-network to make decisions. It selects the action with the highest Q-value in a given state, aiming to maximize future rewards.

**In essence, DQN learns from experience, predicts future rewards, and makes decisions to optimize them.**


## Usage
Cloning the repo
```
git clone https://github.com/arthiondaena/Car-game.git
```
Installing requirements
```
pip install -r requirements.txt
```
Training the model
```
python train.py
```
Testing the model
```
python test_model.py
```
You can compete with the model by changing `players=1` argument in [test_model](test_model.py) to `players=2`.
