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

walls_img = pg.image.load("../images/block2020.png")
yel_img = pg.image.load("../images/yel.png")
turq_img = pg.image.load("../images/turq.png")
green_img = pg.image.load("../images/green.png")
red_img = pg.image.load("../images/red.png")
orange_img = pg.image.load("../images/orange.png")
blue_img = pg.image.load("../images/blue.png")
pink_img = pg.image.load("../images/pink.png")

images = [yel_img, turq_img, green_img, red_img, orange_img, blue_img, pink_img]

class Board:
    """ Game board represented as a nxm matrix
    with borders as number n (n will give which type of block the wall is). Ex:
    [n000n]
    [n000n]
    [n000n]
    [nnnnn]
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
                pg.draw.rect(window, (111, 111, 111),
                             pg.Rect((self.posX + self.blockSize * column + margin * column - 1,
                                      self.posY + row * self.blockSize + row * margin - 1), (margin, 21)))
                pg.draw.rect(window, (111, 111, 111),
                             pg.Rect((self.posX + self.blockSize * column + margin * column - 1,
                                      self.posY + row * self.blockSize + row * margin - 1), (20, margin)))
                if matrix[row][column] == 8:
                    window.blit(walls_img, (self.posX + self.blockSize * column + margin * column,
                                            self.posY + row * self.blockSize + row * margin))
                elif matrix[row][column] == 1:
                    window.blit(yel_img, (self.posX + self.blockSize * column + margin * column,
                                          self.posY + row * self.blockSize + row * margin))
                elif matrix[row][column] == 2:
                    window.blit(turq_img, (self.posX + self.blockSize * column + margin * column,
                                           self.posY + row * self.blockSize + row * margin))
                elif matrix[row][column] == 3:
                    window.blit(green_img, (self.posX + self.blockSize * column + margin * column,
                                            self.posY + row * self.blockSize + row * margin))
                elif matrix[row][column] == 4:
                    window.blit(red_img, (self.posX + self.blockSize * column + margin * column,
                                          self.posY + row * self.blockSize + row * margin))
                elif matrix[row][column] == 5:
                    window.blit(orange_img, (self.posX + self.blockSize * column + margin * column,
                                             self.posY + row * self.blockSize + row * margin))
                elif matrix[row][column] == 6:
                    window.blit(blue_img, (self.posX + self.blockSize * column + margin * column,
                                           self.posY + row * self.blockSize + row * margin))
                elif matrix[row][column] == 7:
                    window.blit(pink_img, (self.posX + self.blockSize * column + margin * column,
                                           self.posY + row * self.blockSize + row * margin))
