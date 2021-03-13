import queens
import copy


def AStarSearch(initBoard,boardSize):
    states=[]
    attack=queens.attacking(initBoard)
    PreviousBoard=[initBoard,attack,0]
    closedStates=[]
    node=0
    while 1:
        for i in range(boardSize):
            y=PreviousBoard[0][i].row
            for j in range(boardSize):
                if y==j:
                    continue
                states.append(copy.deepcopy(PreviousBoard))
                states[-1][0][i].up(j-y)
                attack=queens.attacking(states[-1][0])
                cost=abs(j-y)*states[-1][0][i].weight**2
                states[-1][1]=attack
                states[-1][2]=cost+PreviousBoard[2]
                if attack==0:
                    return states[-1]
        allCost=[_[1]*100+_[2] for _ in states]
        while 1:
            minCost=min(allCost)
            node=allCost.index(minCost)
            x=list(_.row for _ in states[node][0])
            if x in closedStates:
                states.pop(node)
                allCost.pop(node)
            else:
                closedStates.append(x)
                break
        print(minCost)
        #queens.chessBoard(states[node][0],boardSize)
        PreviousBoard=states[node]
        states.pop(node)



if __name__=="__main__":
    boardSize=8
    nPlusOne=False
    initBoard=queens.generateQueens(boardSize,nPlusOne)
    attack=queens.attacking(initBoard)
    print(attack)
    queens.chessBoard(initBoard,boardSize)
    result=AStarSearch(initBoard,boardSize)
    print(result[2])
    queens.chessBoard(result[0],boardSize)
