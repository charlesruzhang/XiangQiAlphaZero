This projects learns from AlphaGo Zero's paper on playing the game of Go, and targets to find a similar solution to the game of Xiangqi(Chinese Chess).

The project is still under construction where the training and testing of the network still needs more work.

Currently the project is run on my personal laptop, with Windows 10 and Python 3.9 installed. 

Structure of the project:
    board.py and piece.py implements the rule of Xiangqi,
    network.py and mcts.py implements the Monte Carlo Search Tree and the network, 
    # Game.py and basicAI.py is no longer being used. (That includes an implementation of Alpha-Beta pruning)