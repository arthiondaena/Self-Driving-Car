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
Q-Learning is required as a pre-requisite as it is a process of Q-Learning creates an exact matrix for the working agent which it can “refer to” to maximize its reward in the long run. Although this approach is not wrong in itself, this is only practical for very small environments and quickly loses it’s feasibility when the number of states and actions in the environment increases. The solution for the above problem comes from the realization that the values in the matrix only have relative importance ie the values only have importance with respect to the other values. Thus, this thinking leads us to Deep Q-Learning which uses a deep neural network to approximate the values. This approximation of values does not hurt as long as the relative importance is preserved. The basic working step for Deep Q-Learning is that the initial state is fed into the neural network and it returns the Q-value of all possible actions as an output. 

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
