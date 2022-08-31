from abc import ABC

class Piece(ABC):
    # For each piece in the XiangQi game, (An empty slot is also a piece except that nothing can be done to that piece.)
    # when initialization: 
    #   .color records the color of the piece.
    #   .jiang records whether the piece is Jiang or not (for checking whether game is over)
    #   .empty records wheter the piece is non-trivial.
    # .ab: Abbreviation for printing the board.
    # .name: Name for finding the piece in the board.
    # .score: Score is no longer in use( was used for basicAI, alpha-beta pruning)
    # .moves: All possible moves for that piece.
    # def move(self, board, from, to): check if a move from 'from' to 'to' is valid under the board 'board'
    #   returns 0 if valid, -1 elsewhere.
    # For more details about the rules of XiangQi, please visit: https://www.ymimports.com/pages/how-to-play-xiangqi-chinese-chess
    def __init__(self, color):
        self.color = color
        self.empty = False
        self.jiang = False

class Ju(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.ab = 'J'
        self.name = ["Ju1", "Ju2"]
        self.score = 1000
        self.moves = []
        for i in range(-9, 0):
            self.moves.append((i, 0))
        for i in range(1, 10):
            self.moves.append((i, 0))
        for i in range(-8, 0):
            self.moves.append((0, i))
        for i in range(1, 9):
            self.moves.append((0, i))

    def move(self, board, pfrom, pto):
        (pfromh, pfromv) = pfrom
        (ptoh, ptov) = pto
        if pfromh == ptoh:
            if pfromv == ptov:
                return -1
            mmin = min(pfromv, ptov) 
            mmax = max(pfromv, ptov)
            for i in range(mmin+1, mmax):
                if board[pfromh][i].empty is False:
                    return -1
        elif pfromv == ptov:
            mmin = min(pfromh, ptoh) 
            mmax = max(pfromh, ptoh)
            for j in range(mmin+1, mmax):
                if board[j][pfromv].empty is False:
                    return -1
        else:
            return -1
        return 0
    
class Ma(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.ab = 'M'
        self.name = ["Ma1", "Ma2"]
        self.score = 500
        self.moves = [(2, 1), (-2, -1), (-2, 1), (2, -1), (1, 2), (-1, -2), (-1, 2), (1, -2)]

    def move(self, board, pfrom, pto):
        (pfromh, pfromv) = pfrom
        (ptoh, ptov) = pto
        if (pfromh - ptoh) ** 2 + (pfromv - ptov) ** 2 != 5:
            return -1
        if abs(pfromh - ptoh) == 1:
            if board[pfromh][(pfromv+ptov) // 2].empty is False:
                return -1
        elif abs(pfromv - ptov) == 1:
            if board[(pfromh + ptoh) // 2][pfromv].empty is False:
                return -1
        return 0

        

class Pao(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.ab = 'P'
        self.name = ["Pao1", "Pao2"]
        self.score = 500
        self.moves = []
        for i in range(-9, 0):
            self.moves.append((i, 0))
        for i in range(1, 10):
            self.moves.append((i, 0))
        for i in range(-8, 0):
            self.moves.append((0, i))
        for i in range(1, 9):
            self.moves.append((0, i))

    def move(self, board, pfrom, pto):
        (pfromh, pfromv) = pfrom
        (ptoh, ptov) = pto
        pieceto = board[ptoh][ptov]
        if pfromh == ptoh:
            if pfromv == ptov:
                return -1
            mmin = min(pfromv, ptov) 
            mmax = max(pfromv, ptov)
        elif pfromv == ptov:
            mmin = min(pfromh, ptoh) 
            mmax = max(pfromh, ptoh)      
        else:
            return -1
        count = 0
        for i in range(mmin+1, mmax):
            if pfromh == ptoh:
                target = board[pfromh][i]
            else:
                target = board[i][pfromv]
            if target.empty is False:
                count += 1
            if count >= 2:
                return -1
        if (count == 0 and pieceto.empty is False) or (count == 1 and pieceto.empty):
            return -1
        return 0

class Xiang(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.ab = 'X'
        self.name = ["Xiang1", "Xiang2"]
        self.score = 200
        self.moves = [(2, 2), (-2, -2), (-2, 2), (2, -2)]
    
    def move(self, board, pfrom, pto):
        (pfromh, pfromv) = pfrom
        (ptoh, ptov) = pto
        piece = board[pfromh][pfromv]
        if (pfromh - ptoh) ** 2 + (pfromv - ptov) ** 2 != 8:
            return -1
        if ((ptoh > 4) and piece.color == 0) or ((ptoh < 5) and piece.color == 1):
            return -1
        if board[(pfromh + ptoh) // 2][(pfromv+ptov) // 2].empty is False:
            return -1
        return 0

class Shi(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.ab = 'S'
        self.name = ["Shi1", "Shi2"]
        self.score = 250
        self.moves = [(1, 1), (-1, -1), (-1, 1), (1, -1)]

    def move(self, board, pfrom, pto):
        (pfromh, pfromv) = pfrom
        (ptoh, ptov) = pto
        piece = board[pfromh][pfromv]
        if (pfromh - ptoh) ** 2 + (pfromv - ptov) ** 2 != 2:
            return -1
        if ((ptoh > 2) and piece.color == 0) or ((ptoh < 7) and piece.color == 1) or (ptov > 5) or (ptov < 3):
            return -1
        return 0

class Bing(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.ab = 'B'
        self.name = ["Bing1", "Bing2", "Bing3", "Bing4", "Bing5"]
        self.score = 100
        self.moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    def move(self, board, pfrom, pto):
        (pfromh, pfromv) = pfrom
        (ptoh, ptov) = pto
        piece = board[pfromh][pfromv]
        if (pfromh - ptoh) ** 2 + (pfromv - ptov) ** 2 != 1:
            return -1
        if (piece.color == 0 and pfromh > ptoh) or (piece.color == 1 and pfromh < ptoh): 
            return -1
        if (piece.color == 0 and pfromh < 5 and pfromv != ptov) or (piece.color == 1 and pfromh > 4 and pfromv != ptov):
            return -1
        return 0

class Jiang(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.ab = 'I'
        self.name = ["Jiang"]
        self.jiang = 1
        self.score = 0
        self.moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def move(self, board, pfrom, pto):
        (pfromh, pfromv) = pfrom
        (ptoh, ptov) = pto
        piece = board[pfromh][pfromv]
        if (pfromh - ptoh) ** 2 + (pfromv - ptov) ** 2 != 1:
            return -1
        if ((ptoh > 2) and piece.color == 0) or ((ptoh < 7) and piece.color == 1) or (ptov > 5) or (ptov < 3):
            return -1
        return 0

class Empty(Piece):
    def __init__(self):
        super().__init__(-1)
        self.ab = ' '
        self.name = []
        self.empty = 1
        self.score = 0
