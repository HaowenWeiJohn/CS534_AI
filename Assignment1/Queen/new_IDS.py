
from Assignment1.Queen import queens
import copy
import time

def ids(queenList, depth):
    orignQueens = queenList.copy()
    for depth in range(depth + 1):
        state = [0]
        idsPrpcess(orignQueens, depth, state)
        if (queens.attacking(queenList) == 0):
            return

def idsPrpcess(queenList, depth , state):
    if depth == 0 and queens.attacking(queenList) == 0:
        return
    elif depth > 0:
        for index in range(len(queenList)):
            if state[0] == 1:
                return
            r = queenList[index].row
            for y in range(len(queenList)):
                if r == y:
                    continue
                queenList[index].up(y - r)

                if queens.attacking(queenList) == 0:
                    state[0] = 1
                    return
                else:
                    idsPrpcess(queenList, depth - 1, state)
                    if(state[0]==1):
                        return
                    queenList[index].up(r - y)

    return


def totalCost(originQueens, targetQueens):
    total = 0
    for index in range(len(targetQueens)):
        total += abs(originQueens[index].row - targetQueens[index].row) * pow(targetQueens[index].weight, 2)
    return total


if __name__ == "__main__":
    boardSize = 7
    nPlusOne = False
    initBoard = queens.generateQueens(boardSize, nPlusOne)
    attack = queens.attacking(initBoard)
    print("Original attack : ", attack)
    original_board = copy.deepcopy(initBoard)
    # queens.chessBoard(initBoard, boardSize)
    # print(original_board[0].row)
    # 　run  ids to get result
    start = time.time()
    ids(initBoard, 7)
    end = time.time()
    new_attack = queens.attacking(initBoard)
    # print(initBoard[0].row)
    print("New attack : ", new_attack)
    cost = totalCost(original_board , initBoard)
    print("Total cost : " , cost)
    print("Run time : ", end - start)
    queens.chessBoard(initBoard, boardSize)






