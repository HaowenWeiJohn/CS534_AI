import queens
import copy


def AStarSearch(initBoard,boardSize):
    states=[]
    attack=queens.attacking(initBoard)
    node=0
    while 1:
        for i in range(boardSize):
            y=initBoard[i].row
            for j in range(boardSize):
                if y==j:
                    continue
                states.append([copy.deepcopy(initBoard),0,0])
                states[-1][0][i].up(j-y)
                attack=queens.attacking(states[-1][0])
                cost=abs(j-y)*states[-1][0][i].weight**2
                states[-1][1]=attack
                states[-1][2]=cost
                if attack==0:
                    return states[-1]
        allAttack=[a[1] for a in states]
        minAttack=min(allAttack)
        node=allAttack.index(minAttack)
        print(minAttack)
        queens.chessBoard(states[node][0],boardSize)
        initBoard=states[node][0]
        states.pop(node)



if __name__=="__main__":
    boardSize=8
    nPlusOne=False
    initBoard=queens.generateQueens(boardSize,nPlusOne)
    attack=queens.attacking(initBoard)
    print(attack)
    queens.chessBoard(initBoard,boardSize)
    result=AStarSearch(initBoard,boardSize)
    print(result[1])
    queens.chessBoard(result[0],boardSize)
