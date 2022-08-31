import board
import basicAI as b
                            
# A trivial game client that can be played by two humans.
def main():
    newBoard = board.Board()
    newBoard.printBoard()
    while True:
        inputstr = str(newBoard.turn) + "\'s turn!"
        line = input(inputstr)
        if line == "s":
            print(b.alphabeta(newBoard, 3, -99999, 99999))
            continue
        inputList = line.split(" ")
        if len(inputList) != 4:
            print("Invalid input! Please Retry!")
            continue
        try:
            pfromh = int(inputList[0])
            pfromv = int(inputList[1])
            ptoh = int(inputList[2])
            ptov = int(inputList[3])    
        except ValueError:
            print("Integers only!")
            continue
        res = newBoard.checkmove((pfromh, pfromv), (ptoh, ptov))
        if res == 1:
            break
        elif res == 0:
            newBoard.move((pfromh, pfromv), (ptoh, ptov))
            newBoard.printBoard()
           
            
if __name__ == "__main__":
    main()
