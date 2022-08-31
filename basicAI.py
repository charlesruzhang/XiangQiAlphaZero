import sys, os
# Basic minimax and alpha-beta pruning is done in this file, but they are no longer used.

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

def getAllMoves(board):
    moves = []
    if board.turn == 0:
        pieces = board.rpieces
    else: 
        pieces = board.bpieces
    for key in pieces:
        if pieces[key] is not None:
            (vh, vv) = pieces[key]
            for (mh, mv) in board.board[vh][vv].moves:
                blockPrint()
                if board.checkmove(pieces[key], (vh + mh, vv + mv)) > -1:
                    enablePrint()
                    moves.append((pieces[key], (vh + mh, vv + mv)))
    enablePrint()
    return moves
'''
def search(board, depth):
    moves = getAllMoves(board)
    bestMove = None
    alpha = -99999
    beta = 99999
    for move in moves:
        (mfrom, mto) = move
        newBoard = board.copy()
        newBoard.move(mfrom, mto)
        val = alphabeta(newBoard, depth - 1, alpha, beta)
        if val > alpha:
            print(move)
            alpha = val
            bestMove = move
    print(alpha, beta)
    return bestMove
'''
              
def alphabeta(board, depth, alpha, beta):
    if depth <= 0 or board.rpieces['Jiang'] is None or board.bpieces['Jiang'] is None:
        return (evaluate(board), None)
    bestMove = None
    moves = getAllMoves(board)
    for move in moves:
        (mfrom, mto) = move
        board.move(mfrom, mto)
        val, _ = alphabeta(board, depth - 1, -beta, -alpha)
        board.undo()
        val = -val
        if val >= beta:
            return (val, None)
        if val > alpha:
            alpha = val
            bestMove = move
    return (alpha, bestMove)

def evaluate(board):
    if board.turn == 0:
        factor = 1
    else:
        factor = -1
    if board.rpieces['Jiang'] is None:
        return factor * -49999
    if board.bpieces['Jiang'] is None:
        return factor * 49999
    ev = 0
    for key in board.rpieces:
        val = board.rpieces[key]
        if val is not None:
            (vh, vv) = val
            ev += board.board[vh][vv].score
    
    for key in board.bpieces:
        val = board.bpieces[key]
        if val is not None:
            (vh, vv) = val
            ev -= board.board[vh][vv].score
    return factor * ev