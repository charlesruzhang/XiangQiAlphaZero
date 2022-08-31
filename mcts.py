import basicAI as b
import numpy as np
import board as bd
import network
import random
import torch
from bisect import bisect

# All of the codes here lied under the structure of Alphazero. For details, please directly read the paper: 
# The Monte Carlo Tree Search algorithm is implemented here with:
#   class MCTS as the main tree, which records the root node and provides helper functions.
#   class Node as the node class.
# For more information about the algorithm itself, please find the source online. 

class Node():
    def __init__(self, val):
        self.val = val
        self.children = []
        self.P = 0
        self.Q = 0
        self.N = 0
        self.W = 0

    def addSubNode(self, node):
        self.children.append(node)
    
    def isLeaf(self):
        return len(self.children) == 0

    def initializeProbs(self, probs):
        for i in range(len(self.children)):
            self.children[i].P = probs[i]

class MCTS():
    def __init__(self, root, net, cpunct=np.sqrt(2)):
        self.root = root
        self.cpunct = cpunct
        self.originalBoard = root.val.copy()
        self.net = net

    def resetBoard(self):
        self.root.val = self.originalBoard.copy()

    def searchNPlay(self, count=1200, tau = 1):
        # The MCTS does three steps in a cycle:
        #   1: select from the child nodes until a leaf node is got.
        #   2: use the neural network for expanding the node, 
        #   3: update the values for each node on the search route after the expansion.
        # SearchNPlay does a default of 1200 cycles for a single move, and decide the 'best' move after the cycles.
        # Then index of the move is returned. 
        self.root.val.printBoard()
        print('\n')
        if self.root.isLeaf():
            self.expand(self.root)
        
        for i in range(count):
            res = self.select(self.root)
            self.backup(self.root, res)
            self.resetBoard()
        totalCount = 0
        pi = []
        for child in self.root.children:
            totalCount += child.N ** (1 / tau)
        for i in range(len(self.root.children)):
            if i == 0:
                last = 0
            else:
                last = pi[-1]
            pi.append((self.root.children[i].N ** (1 / tau)) / totalCount + last)
        chosenIndex = bisect(pi, random.random())
        return chosenIndex

    def select(self, current):
        X = []
        for child in current.children:
            X.append(self.cpunct * child.P * np.sqrt(current.N) / (1 + child.N) + child.Q)
        index = X.index(max(X))
        child = current.children[index]
        (pfrom, pto) = child.val
    
        res = self.root.val.move(pfrom, pto)
        if res != 0:
            self.backup(child, res)
            print(pfrom, pto)
            return -res
        if child.isLeaf():
            res = self.expand(child)
            self.backup(child, res)
            return -res
        else:
            res = self.select(child)
            self.backup(child, res)
            return -res

    def backup(self, current, res):
        current.N += 1
        current.W += res
        current.Q = current.W / current.N

    def expand(self, child):
        root = self.root
        possibleMoves = b.getAllMoves(root.val)
        parsedBoard = parseBoard(root.val)
        (nprobs, nv) = self.net(parsedBoard)
        for move in possibleMoves:
            subNode = Node(move)
            child.addSubNode(subNode)
        probs = parseProbsFromNet(nprobs, possibleMoves, root.val)
        s = sum(probs)
        probs = [ i/s for i in probs ]
        child.initializeProbs(probs)
        return nv

def parseBoard(board):
    # PaseBoard function takes in a board entry, and outputs a torch tensor with shape: (33, 10, 9)
    # The main target is to transform a board to something that can be thrown into the network.
    boardArray = []
    for piece in board.rpieces:
        boardArray.append(parseOnePiece(piece, board.rpieces))
    for piece in board.bpieces:
        boardArray.append(parseOnePiece(piece, board.bpieces))
    if board.turn == 0:
        pieces = board.rpieces
    else:
        pieces = board.bpieces
    array = torch.zeros((10, 9))
    for piece in pieces:
        if pieces[piece] is not None:
            (ph, pv) = pieces[piece]
            array[ph][pv] = 1
    boardArray.append(array)
    boardArray = torch.stack(boardArray)
    return boardArray

def parseOnePiece(piece, side):
    # Helper function to parse each single piece on the board.
    array = torch.zeros((10, 9))
    if side[piece] is not None:
        (ph, pv) = side[piece]
        array[ph][pv] = 1
    return array

def parseProbsFromNet(nprobs, moves, board):
    # The network should 'learn' that invalid moves are not favored.
    # input: nprobs, result returned by the neural network.
    #        moves,  all valid moves on the board. 
    #        board, the current board where players are playing on.
    # The main target of the function is to tranform the output of the network to an array of length len(moves)
    # returns p, used to compute the loss.
    p = np.zeros(len(moves))
    for i in range(len(moves)):
        p[i] = i + 1
    # A trick is used here to more efficiently check whether an entry in 'nprobs' belongs to valid move:
    # For each valid moves in move: i.e. m = moves[i],
    #   i is recorded in p's ith entry, and thus after passing it into parseProbsToNet,
    # The newly parsed array has value i if that index belongs to the move with index i.
    # Then we can use this information to find valid moves in 'nprobs'
    newp = parseProbsToNet(p, moves, board)
    for i in range(len(newp)):
        if newp[i] == 0:
            continue
        p[int(newp[i]) - 1] = nprobs[0][i]
    return p

def parseProbsToNet(probs, moves, board):
    # The input consists of all the possible moves (those which follow the rule),
    # and we want to have a longer list of all the moves possible. 
    # (i.e. All the moves that are against the rule will have a prob = 0)
    # The purpose of doing this is to 'train' the network to learn the rules.
    # The output has the format of:
    # Red: [0..33] Ju1 [34..67] Ju2 [68..75] Ma1 [76..83] Ma2 
    #      [84..87] Xiang1 [88..91] Xiang2 [92..95] Shi1 [96..99] Shi2 
    #      [100..103] Jiang [104..106] Bing1 [107..109] Bing2 [110..112] Bing3
    #      [113..115] Bing4 [116..118] Bing5 [119..152] Pao1 [153..186] Pao2
    # Black + 187
    indexDict = {
        "Ju1": 0,
        "Ju2": 34,
        "Ma1": 68,
        "Ma2": 76,
        "Xiang1": 84,
        "Xiang2": 88,
        "Shi1": 92,
        "Shi2": 96,
        "Jiang": 100,
        "Bing1": 104,
        "Bing2": 107,
        "Bing3": 110,
        "Bing4": 113,
        "Bing5": 116,
        "Pao1": 119,
        "Pao2": 153
    }
    outputProbs = np.zeros(374)
    if board.turn == 0:
        pieces = board.rpieces
    else:
        pieces = board.bpieces

    for i in range(len(moves)):
        (pfrom, pto) = moves[i]
        (ph, pv) = pfrom
        (ptoh, ptov) = pto
        tofind = (ptoh - ph, ptov - pv) 
        indexInPiece = board.board[ph][pv].moves.index(tofind)
        name = list(pieces.keys())[list(pieces.values()).index(pfrom)]
        indexInPiece += indexDict[name]
        if board.turn == 1:
            indexInPiece += 187
        #print(indexInPiece)
        outputProbs[indexInPiece] = probs[i]
    return torch.tensor(outputProbs)
        
def delnode(c):
    if len(c.children) == 0:
        del c
        return
    for child in c.children:
        delnode(child)
    del c
    return 

def selfPlay(board, net, opt):
    # Self playing using MCTS and DNN.
    root = Node(board)
    '''
    moves = b.getAllMoves(board)
    for move in moves:
        subNode = Node(move)
        root.addSubNode(subNode)
    '''
    turnCount = 0
    current = root
    mcts = MCTS(current, net)
    while turnCount < 400:
        turnCount += 1
        moveIndex = mcts.searchNPlay()
        x = parseBoard(current.val)
        probs = []
        for child in current.children:
            probs.append(child.N / current.N)
        probs = parseProbsToNet(probs, b.getAllMoves(current.val), current.val)
        y = (probs, torch.tensor(current.Q))

        net.train()
        network.train(net, x, y, opt)
        net.eval()

        child = current.children[moveIndex]
        (pfrom, pto) = child.val
        res = current.val.move(pfrom, pto)
        if res != 0:
            current.val.printBoard()
            print(current.val.turn, " wins")
            break
        
        child.val = current.val
        
        #Trying to delete the entire tree
        for c in mcts.root.children:
            if c != child:
                delnode(c)
        del mcts

        mcts = MCTS(child, net)
        current = child

if __name__ == "__main__": 
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    newBoard = bd.Board()
    net = network.network()
    net.to(device)
    opt = torch.optim.Adagrad(net.parameters(), lr=0.01)
    selfPlay(newBoard, net, opt)
