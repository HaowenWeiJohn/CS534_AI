from Assignment1.Queen import queens
import itertools as it
import copy
import numpy as np
import random


def noSamePosition(thisQueen, otherQueens):
    i = 0
    for Q in otherQueens:
        if thisQueen.column == Q.column and thisQueen.row == Q.row:
            i += 1
        if i > 1:
            return False

    return True


def movesForAllQueens(AllQueens):
    boards = []
    moveCost = []
    stateCost = []

    boardSize = AllQueens[0].boardSize

    for index in range(0, len(AllQueens)):
        row = AllQueens[index].row
        # queens.chessBoard(AllQueens, 10)
        # loop the column
        for i in range(1, row + 1):
            # down
            AllQueensCopy = copy.deepcopy(AllQueens)

            AllQueensCopy[index].down(i)

            if noSamePosition(AllQueensCopy[index], AllQueensCopy):
                move_cost = AllQueensCopy[index].weight * i
                state_cost = AllQueensCopy[index].weight * i + queens.attacking(AllQueensCopy) * 100

                boards.append(AllQueensCopy)
                moveCost.append(move_cost)
                stateCost.append(state_cost)
                # queens.chessBoard(AllQueensCopy, 10)

        for j in range(1, boardSize - row):  # up

            AllQueensCopy = copy.deepcopy(AllQueens)
            AllQueensCopy[index].up(j)

            if noSamePosition(AllQueensCopy[index], AllQueensCopy):
                move_cost = AllQueensCopy[index].weight * j
                state_cost = AllQueensCopy[index].weight * j + queens.attacking(AllQueensCopy) * 100

                boards.append(AllQueensCopy)
                moveCost.append(move_cost)
                stateCost.append(state_cost)
                # queens.chessBoard(AllQueensCopy, 10)

    return boards, np.array(moveCost), np.array(stateCost)


def hillCliming(Queens, temperature=10):
    # Queens = queens.generateQueens(boardSize, True)
    initialStateCost = queens.attacking(Queens) * 100

    # for round in range(0,10):

    init_T = temperature
    time = 0
    initialState = copy.deepcopy(Queens)

    previousTotalCost = initialStateCost
    previousTotalMoveCost = 0
    previousState = copy.deepcopy(initialState)
    cost_record = []

    while True:
        cost_record.append(previousTotalCost)
        T = np.exp(-time / 2) * temperature

        boards, moveCost, stateCost = movesForAllQueens(previousState)
        totalCost = stateCost + previousTotalMoveCost
        # decision based on the difference between total cost on this state and the total cost on previous state
        delta = totalCost - previousTotalCost
        # print(np.min(delta))
        if np.min(delta) >= 0:
            return cost_record, previousState

        delta_T = delta / T
        delta_T[delta_T >= 100] = 100
        # print(delta_T)
        acceptRate = 1 / (1 + np.exp(delta_T))

        decision_index = random.choices(list(range(len(boards))), acceptRate)[0]

        thisBoard = boards[decision_index]
        thisMoveCost = moveCost[decision_index]
        thisStateCost = stateCost[decision_index]

        previousState = thisBoard
        previousTotalMoveCost += thisMoveCost
        previousTotalCost = previousTotalMoveCost + thisStateCost

        time = time + 1
        # queens.chessBoard(thisBoard, boardSize)


def hillClimingMultiStart(boardSize=8, init_temperature=20, round=10):
    Queens = queens.generateQueens(boardSize=boardSize, nPlusOne=True)

    for i in range(0, round):
        queens.chessBoard(Queens, boardSize=boardSize)
        loss_function, finalState = hillCliming(Queens=Queens, temperature=init_temperature)
        print(loss_function)
        queens.chessBoard(finalState, boardSize=boardSize)


if __name__ == '__main__':
    hillClimingMultiStart(boardSize=16, init_temperature=10, round=10)
