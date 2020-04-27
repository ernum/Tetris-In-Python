import pygame as pg

pg.init()

margin = 1
white = (255, 255, 255)
black = (0, 0, 0)


class Board:
    """ Game board represented as a nxm matrix
    with borders as nines. Ex:
    [90009]
    [90009]
    [90009]
    [99999]
    """

    def __init__(self, colour, startX, startY, no_of_rows, no_of_cols, blockSize):
        self.colour = colour
        self.posX = startX
        self.posY = startY
        self.no_of_rows = no_of_rows
        self.no_of_cols = no_of_cols
        self.board = self.board_matrix(no_of_rows, no_of_cols)
        self.blockSize = blockSize

    def board_matrix(self, rows, cols):
        board = [[0 for i in range(cols)] for j in range(rows)]
        for i in range(rows):
            board[i][0] = 9
            board[i][len(board[0]) - 1] = 9
            if i == rows - 1:
                board[i] = [9 for j in range(len(board[0]))]
        return board

    def drawFigure(self, window):
        for column in range(self.no_of_cols):
            for row in range(self.no_of_rows):
                if self.board[row][column] == 9:
                    pg.draw.rect(window, self.colour,
                                 ((self.posX + self.blockSize * column + margin * column,
                                   self.posY + row * self.blockSize + row * margin),
                                  (self.blockSize, self.blockSize)))
                if self.board[row][column] == 0:
                    pg.draw.rect(window, black,
                                 ((self.posX + self.blockSize * column + margin * column,
                                   self.posY + row * self.blockSize + row * margin),
                                  (self.blockSize, self.blockSize)))

