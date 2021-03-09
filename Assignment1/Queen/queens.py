import random
import matplotlib.pyplot as plt
import numpy as np


class queen():
    def __init__(self, no, boardSize):
        self.row = no // boardSize
        self.column = no % boardSize

        # right top to left down
        self.diagonalR = self.row - self.column + boardSize - 1
        # left top to right down
        self.diagonalL = self.column + self.row
        self.weight = random.randint(1, 9)

    def up(self, step):
        self.row = self.row + step
        self.diagonalR = self.diagonalR + step
        self.diagonalL = self.diagonalL + step

    def down(self, step):
        self.row = self.row - step
        self.diagonalR = self.diagonalR - step
        self.diagonalL = self.diagonalL - step

    def left(self, step):
        self.column = self.column - step
        self.diagonalR = self.diagonalR + step
        self.diagonalL = self.diagonalL - step

    def right(self, step):
        self.column = self.column + step
        self.diagonalR = self.diagonalR - step
        self.diagonalL = self.diagonalL + step

    def upleft(self, step):
        self.row = self.row + step
        self.column = self.column - step
        self.diagonalR = self.diagonalR + step * 2

    def upright(self, step):
        self.row = self.row + step
        self.column = self.column + step
        self.diagonalL = self.diagonalL + step * 2

    def downleft(self, step):
        self.row = self.row - step
        self.column = self.column - step
        self.diagonalL = self.diagonalL - step * 2

    def downright(self, step):
        self.row = self.row - step
        self.column = self.column + step
        self.diagonalR = self.diagonalR - step * 2


def chessBoard(queens, boardSize):
    fig, ax = plt.subplots(figsize=(6, 6))
    plt.axis([-1, boardSize, -1, boardSize])
    y = list(i.row for i in queens)
    x = list(i.column for i in queens)
    w = list(i.weight for i in queens)
    ax.scatter(x, y, s=20)
    for i in range(len(queens)):
        ax.annotate([i, w[i]], [x[i], y[i]])
    grids = np.linspace(-0.5, boardSize - 0.5, boardSize + 1)
    for i in grids:
        plt.axvline(x=i, lw=0.2)
        plt.axhline(y=i, lw=0.2)
    plt.show()


def generateQueens(boardSize,nPlusOne):
    queens=[]
    for column in range(boardSize):
        row=random.randint(0,boardSize-1)
        queens.append(queen(row,column))
    if nPlusOne:
        n=boardSize//8
        for _ in range(n):
            occupied=True
            while occupied:
                column=random.randint(0,boardSize-1)
                row=random.randint(0,boardSize-1)
                for i in queens:
                    if i.row == row and i.column == column:
                        continue
                occupied=False
            queens.append(queen(row,column))
    return(queens)



def attacking(queens):
    queens2 = list(queens).copy()
    attack = 0
    while len(queens2) > 1:
        attack_row = list(i.row for i in queens2).count(queens2[0].row) - 1
        attack_column = list(i.column for i in queens2).count(queens2[0].column) - 1
        attack_diagonalL = list(i.diagonalL for i in queens2).count(queens2[0].diagonalL) - 1
        attack_diagonalR = list(i.diagonalR for i in queens2).count(queens2[0].diagonalR) - 1
        attack = attack + attack_row + attack_column + attack_diagonalL + attack_diagonalR
        queens2.pop(0)
    return attack


if __name__ == "__main__":

    boardSize = 8
    queenNum = 8
    nPlusOne = True
    queens = generateQueens(boardSize,nPlusOne)
    attack = attacking(queens)
    print(attack)
    chessBoard(queens, boardSize)
    queens[0].upleft(1)
    chessBoard(queens, boardSize)
