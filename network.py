import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

# The network follows AlphaGo Zero's paper on playing Go.

class network(nn.Module):
    def __init__(self, rb=1):
        # The neural networked used to predict moves for unseen boards.
        super(network, self).__init__()
        self.rb = rb
        self.conv1 = nn.Conv2d(33, 256, 3, padding=1)
        self.bnorm = nn.BatchNorm2d(256)
        self.bnormp = nn.BatchNorm2d(2)
        self.bnormv = nn.BatchNorm2d(1)
        self.conv2 = []
        for _ in range(rb):
            self.conv2.append(nn.Conv2d(256, 256, 3, padding=1))
        self.conv3 = []
        for _ in range(rb):
            self.conv3.append(nn.Conv2d(256, 256, 3, padding=1))
        self.policyconv = nn.Conv2d(256, 2, 1)
        self.fc1 = nn.Linear(180, 374)
        self.valconv = nn.Conv2d(256, 1, 1)
        self.fc2 = nn.Linear(90, 256)
        self.fc3 = nn.Linear(256, 1)


    def forward(self, x):
        # The input should have the size of (33, 10, 9) where each channel contains exactly one piece of the pieces, 
        # and an extra channel that contains all pieces of players on their turn.
        '''
        x = x.view(1, 33, 10, 9)
        x = F.relu(self.bnorm(self.conv1(x)))
        for i in range(self.rb):
            f1x = F.relu(self.bnorm(self.conv2[i](x)))
            f2x = self.bnorm(self.conv3[i](f1x))
            x = F.relu(f2x + x)
        px = F.relu(self.bnormp(self.policyconv(x)))
        px = px.view(1,-1)
        prob = self.fc1(px)
        vx = F.relu(self.bnormv(self.valconv(x)))
        vx = vx.view(1,-1)
        v = torch.tanh(self.fc3(F.relu(self.fc2(vx))))
        '''
        output = [prob, v]
        return output

   
def train(net, x, y, opt):
    cn = nn.CrossEntropyLoss()
    msc = nn.MSELoss()
    nx = net(x)
    nprobs = nx[0]
    nv = nx[1]
    (probs, v) = y
    probs = probs.view(1, -1).clone()
    loss1 = msc(nv, v)
    loss2 = cn(nprobs, probs)
    loss = loss1 + loss2
    opt.zero_grad()
    loss.backward()
    opt.step()
