import pygame as pg

pg.init()

margin = 1
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (250, 250, 0)
turq = (20, 250, 250)
green = (0, 255, 0)
red = (255, 0, 0)
orange = (255, 150, 20)
blue = (0, 0, 255)
pink = (200, 20, 250)
colors = [black, yellow, turq, green, red, orange, blue, pink, white]


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
            board[i][0] = 8
            board[i][len(board[0]) - 1] = 8
            if i == rows - 1:
                board[i] = [8 for j in range(len(board[0]))]
        return board

    def drawMatrix(self, window, matrix):
        for column in range(len(matrix[0])):
            for row in range(len(matrix)):
                pg.draw.rect(window, colors[matrix[row][column]],
                             ((self.posX + self.blockSize * column + margin * column,
                               self.posY + row * self.blockSize + row * margin),
                              (self.blockSize, self.blockSize)))