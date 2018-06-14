#Ant World
#Frank L Brasington
#this file contains all the infomation needed for the AI of the ant to work

#these are all the imports are needed for the file to wrok
import numpy as np
import random
import os

#this AI uses pyTorch for the N.Network
#https://pytorch.org/docs/stable.nn.html
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.autograd as autograd
from torch.autograd import Variable

#this creates the architecture of the Neural Network
class Network(nn.Module):
    #The class's constructor
    #input_size the number of inputs
    #nb_action is for the number of actions that can be taken
    def __init__(self, input_size, nb_action):
        super(Network, self).__init__()
        self.input_size = input_size
        self.nb_action = nb_action

        #nn.linear(in_features, out_features, bias=True)
        #in_featrues: size of each input sample
        #out_feature: size of each output sample
        self.fc1 = nn.Linear(input_size, 30)
        self.fc2 = nn.Linear(30, nb_action)

    #Defines the computation performed at every call
    def forward(self, state):
        x = F.relu(self.fc1(state))
        q_values = self.fc2(x)
        return q_values

#This implements the Experinece Replay
class ReplayMemory(object):
    #This sets up the class
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []

    def push(self, event):
        self.memory.append(event)
        #keeps the number in memory set to the capacity
        #deletes the oldest entry if needed
        if len(self.memory) > self.capacity:
            del self.memory[0]

    def sample(self, batch_size):
        samples = zip(*random(self.memory, batch_size))
        return  map(lambda x: Variable(torch.cat(x,0)), samples)

#implementing Deep Q Learning

class Dqn():
    #constructor
    def __init__(self,input_size, nb_action, gamma):
        #these are variable that can be changed to easily see changes
        self.temputure = 50
        self.mem_size = 100000
        self.learning = 0.001

        #sets up the class
        self.gamma = gamma
        self.reward_window = []
        self.model = Network(input_size, nb_action)
        self.memory = ReplayMemory(self.mem_size)
        #uses the Adam Algorithm
        #torch.optim.Adam(params, lr=.001, betas=(.9,.999), eps=1e-8, weight_decay, amsgrad=False)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning)
        self.last_state = torch.Tensor(input_size).unsqueeze(0)

        self.last_action = 0
        self.last_reward = 0

    #this selects all the possible actions for the agent
    def select_action(self, state):
        probs = F.softmax(self.model(Variable(state, volatile=True)) * self.temputure)
        action = probs.multinomial()
        return action.data[0,0]

    #this section is where the AI learns
    def learn(selfself, batch_state, batch_next_state, batch_reward, batch_action):
        outputs = self.model(batch_state).gather(1, batch_action.unsqueeze(1)).squeeze(1)
        next_outputs = self.model(batch_next_state).detach().max(1)[0]
        target = self.gamma * next_outputs + batch_reward
        td_loss = F.smooth_l1_loss(outputs, target)
        self.optimizer.zero_grad()
        td_loss.backward(retain_variables=True)
        self.optimizer.step()

    def update(self, reward, new_signal):
        new_state = torch.Tensor(new_signal).float().unsqueeze(0)
        self.memory.push(
            (self.last_state, new_state, torch.LongTensor([int(self.last_action)]), torch.Tensor([self.last_reward])))
        action = self.select_action(new_state)
        if len(self.memory.memory) > 100:
            batch_state, batch_next_state, batch_action, batch_reward = self.memory.sample(100)
            self.learn(batch_state, batch_next_state, batch_reward, batch_action)
        self.last_action = action
        self.last_state = new_state
        self.last_reward = reward
        self.reward_window.append(reward)
        if len(self.reward_window) > 1000:
            del self.reward_window[0]
        return action

    def score(self):
        return sum(self.reward_window) / (len(self.reward_window) + 1.)

    def save(self):
        torch.save({'state_dict': self.model.state_dict(),
                    'optimizer': self.optimizer.state_dict(),
                    }, 'last_brain.pth')

    def load(self):
        if os.path.isfile('last_brain.pth'):
            print("=> loading checkpoint... ")
            checkpoint = torch.load('last_brain.pth')
            self.model.load_state_dict(checkpoint['state_dict'])
            self.optimizer.load_state_dict(checkpoint['optimizer'])
            print("done !")
        else:
            print("no checkpoint found...")
