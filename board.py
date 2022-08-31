import numpy as np
import pieces as p
import copy

# The board class which records information about the current board.
# Four major types of information is recorded:
# .board: The current board as a 2-D array. Empty slots are occupied by an Empty class. Others are by the pieces.
# .rpieces, .bpieces: The red pieces and black pieces as well as their positions. Pieces that are already killed has position 'None'
# .turn: Records whose turn is it
# .record: The history of plays(Very useful for implementing undo). 
class Board():
    def __init__(self):
        self.board = np.full((10, 9), p.Empty(), dtype=p.Piece)
        for i in range(5):
            self.board[3][i * 2] = p.Bing(0)
        for i in range(5):
            self.board[6][i * 2] = p.Bing(1)
        self.board[0][1] = p.Ma(0)
        self.board[0][7] = p.Ma(0)
        self.board[9][1] = p.Ma(1)
        self.board[9][7] = p.Ma(1)
        self.board[2][1] = p.Pao(0)
        self.board[2][7] = p.Pao(0)
        self.board[7][1] = p.Pao(1)
        self.board[7][7] = p.Pao(1)
        self.board[0][0] = p.Ju(0)
        self.board[0][8] = p.Ju(0)
        self.board[9][0] = p.Ju(1)
        self.board[9][8] = p.Ju(1)
        self.board[0][2] = p.Xiang(0)
        self.board[0][6] = p.Xiang(0)
        self.board[9][2] = p.Xiang(1)
        self.board[9][6] = p.Xiang(1)
        self.board[0][3] = p.Shi(0)
        self.board[0][5] = p.Shi(0)
        self.board[9][3] = p.Shi(1)
        self.board[9][5] = p.Shi(1)
        self.board[0][4] = p.Jiang(0)
        self.board[9][4] = p.Jiang(1)
        
        self.turn = 0

        self.rpieces = {}
        self.rpieces["Jiang"] = (0, 4)
        self.rpieces["Shi1"] = (0, 3)
        self.rpieces["Shi2"] = (0, 5)
        self.rpieces["Xiang1"] = (0, 2)
        self.rpieces["Xiang2"] = (0, 6)
        self.rpieces["Ma1"] = (0, 1)
        self.rpieces["Ma2"] = (0, 7)
        self.rpieces["Ju1"] = (0, 0)
        self.rpieces["Ju2"] = (0, 8)
        self.rpieces["Pao1"] = (2, 1)
        self.rpieces["Pao2"] = (2, 7)
        self.rpieces["Bing1"] = (3, 0)
        self.rpieces["Bing2"] = (3, 2)
        self.rpieces["Bing3"] = (3, 4)
        self.rpieces["Bing4"] = (3, 6)
        self.rpieces["Bing5"] = (3, 8)

        self.bpieces = {}
        self.bpieces["Jiang"] = (9, 4)
        self.bpieces["Shi1"] = (9, 3)
        self.bpieces["Shi2"] = (9, 5)
        self.bpieces["Xiang1"] = (9, 2)
        self.bpieces["Xiang2"] = (9, 6)
        self.bpieces["Ma1"] = (9, 1)
        self.bpieces["Ma2"] = (9, 7)
        self.bpieces["Ju1"] = (9, 0)
        self.bpieces["Ju2"] = (9, 8)
        self.bpieces["Pao1"] = (7, 1)
        self.bpieces["Pao2"] = (7, 7)
        self.bpieces["Bing1"] = (6, 0)
        self.bpieces["Bing2"] = (6, 2)
        self.bpieces["Bing3"] = (6, 4)
        self.bpieces["Bing4"] = (6, 6)
        self.bpieces["Bing5"] = (6, 8)

        self.record = []

    def checkmove(self, pfrom, pto):
        # Check if a move from 'pfrom' to 'pto' is valid.
        # All the functions are straight-forward
        (pfromh, pfromv) = pfrom
        (ptoh, ptov) = pto
        if (pfromh < 0) or (pfromh > 9) or (ptoh < 0) or (ptoh > 9) or (pfromv < 0) or (pfromv > 8) or (ptov < 0) or (ptov > 8):
            return -1
        piece = self.board[pfromh][pfromv]
        pieceto = self.board[ptoh][ptov]
        if piece.empty:
            return -1
        elif piece.color != self.turn:
            print("It's ", self.turn, "'s turn")
            return -1
        elif piece.empty is False and pieceto.color == self.turn:
            return -1
        if piece.move(self.board, pfrom, pto) == -1:
            return -1
        # Checks if jiang was 'kill'ed
        if pieceto.jiang is True:
            print(self.turn, " wins!")
            return 1
        # Checks whether Jiang face against each other.
        if piece.jiang:
            if piece.color == 0:
                (pjiangh, pjiangv) = self.rpieces["Jiang"]
            else:
                (pjiangh, pjiangv) = self.bpieces["Jiang"]
            if pjiangv == ptov:
                duiJiang = True
                mmin = min(pjiangh, ptoh)
                mmax = max(pjiangh, ptoh)
                for i in range(mmin + 1, mmax):
                    if self.board[i][pjiangv].empty is False:
                        duiJiang = False
                        break
                if duiJiang:
                    return -1
        else:
            (pshuaih, pshuaiv) = self.rpieces["Jiang"]
            (pjiangh, pjiangv) = self.bpieces["Jiang"]
            if pjiangv == pshuaiv and pshuaiv == pfromv and pfromh < pjiangh and pshuaih < pfromh and (ptov != pfromv or ptoh > pjiangh or ptoh < pshuaih):
                duiJiang = True
                for i in range(pshuaih + 1, pjiangh):
                    if i == pfromh:
                        continue
                    if self.board[i][pjiangv].empty is False:
                        duiJiang = False
                        break
                if duiJiang:
                    return -1   
        '''
        if piece.jiang:
            if piece.color == 0:
                self.shuai = (ptoh, ptov)
            else:
                self.jiang = (ptoh, ptov)
        '''
        return 0

    def move(self, pfrom, pto):
        '''
            Move a piece from 'pform' to 'pto'
            Also switch the turn
            return 1/-1 if red wins/black wins.
            return 0 if game continues.
        '''
        (pfromh, pfromv) = pfrom
        (ptoh, ptov) = pto
        piece = self.board[pfromh][pfromv]
        pieceto = self.board[ptoh][ptov]
        nameto = ""
        if pieceto.name != [] and pieceto.name[0] == 'Jiang':
            return self.turn * 2 - 1
        for name in pieceto.name:
            if pieceto.color == 0 and self.rpieces[name] == pto:
                self.rpieces[name] = None
                nameto = name
                break
            elif pieceto.color == 1 and self.bpieces[name] == pto:
                self.bpieces[name] = None
                nameto = name
                break
        for name in piece.name:
            if piece.color == 0 and self.rpieces[name] == pfrom:
                self.rpieces[name] = pto
                break
            elif piece.color == 1 and self.bpieces[name] == pfrom:
                self.bpieces[name] = pto
                break
        self.record.append((pfrom, pto, nameto, pieceto))
        self.board[ptoh][ptov] = piece
        self.board[pfromh][pfromv] = p.Empty()
        self.turn = 1 - self.turn
        return 0

    def printBoard(self):
        # print the board in a trivial format.
        for i in range(9, -1, -1):
            line = "== "
            for j in range(9):
                piecename = self.board[i][j].ab
                if self.board[i][j].color == 1:
                    piecename = piecename.lower()
                line += piecename
            line += " =="
            print(line)
    
    def undo(self):
        # Undo the most recent play
        (pfrom, pto, nameto, pieceto) = self.record[-1]
        (pfromh, pfromv) = pfrom
        (ptoh, ptov) = pto
        piece = self.board[ptoh][ptov]
        self.board[pfromh][pfromv] = piece
        self.board[ptoh][ptov] = pieceto
        for name in piece.name:
            if piece.color == 0 and self.rpieces[name] == pto:
                self.rpieces[name] = pfrom
                if nameto != "":
                    self.bpieces[nameto] = pto
                break
            elif piece.color == 1 and self.bpieces[name] == pto:
                self.bpieces[name] = pfrom
                if nameto != "":
                    self.rpieces[nameto] = pto
                break
        self.record.pop()
        self.turn = 1 - self.turn

    def copy(self):
        # Make a deep copy of the board when we need anothe board with same information.
        newBoard = Board()
        newBoard.board = copy.deepcopy(self.board)
        newBoard.turn = self.turn
        newBoard.rpieces = copy.deepcopy(self.rpieces)
        newBoard.bpieces = copy.deepcopy(self.bpieces)
        newBoard.record = copy.deepcopy(self.record)
        return newBoard
