import pygame as pg
import pathlib

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

# Paths
WALLS_IMG_PATH = pathlib.Path(
    __file__).absolute().parents[1] / "images" / "block2020.png"
YEL_IMG_PATH = pathlib.Path(
    __file__).absolute().parents[1] / "images" / "yel.png"
TURQ_IMG_PATH = pathlib.Path(
    __file__).absolute().parents[1] / "images" / "turq.png"
GREEN_IMG_PATH = pathlib.Path(
    __file__).absolute().parents[1] / "images" / "green.png"
RED_IMG_PATH = pathlib.Path(
    __file__).absolute().parents[1] / "images" / "red.png"
ORANGE_IMG_PATH = pathlib.Path(
    __file__).absolute().parents[1] / "images" / "orange.png"
BLUE_IMG_PATH = pathlib.Path(
    __file__).absolute().parents[1] / "images" / "blue.png"
PINK_IMG_PATH = pathlib.Path(
    __file__).absolute().parents[1] / "images" / "pink.png"
GHOST_IMG_PATH = pathlib.Path(
    __file__).absolute().parents[1] / "images" / "ghost.png"

# Images
walls_img = pg.image.load(str(WALLS_IMG_PATH))
yel_img = pg.image.load(str(YEL_IMG_PATH))
turq_img = pg.image.load(str(TURQ_IMG_PATH))
green_img = pg.image.load(str(GREEN_IMG_PATH))
red_img = pg.image.load(str(RED_IMG_PATH))
orange_img = pg.image.load(str(ORANGE_IMG_PATH))
blue_img = pg.image.load(str(BLUE_IMG_PATH))
pink_img = pg.image.load(str(PINK_IMG_PATH))
ghost_img = pg.image.load(str(GHOST_IMG_PATH))

images = [yel_img, turq_img, green_img, red_img,
          orange_img, blue_img, pink_img, walls_img, ghost_img]


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
                number = matrix[row][column]
                pg.draw.rect(window, (111, 111, 111),
                             pg.Rect((self.posX + self.blockSize * column + margin * column - 1,
                                      self.posY + row * self.blockSize + row * margin - 1), (margin, 21)))
                pg.draw.rect(window, (111, 111, 111),
                             pg.Rect((self.posX + self.blockSize * column + margin * column - 1,
                                      self.posY + row * self.blockSize + row * margin - 1), (20, margin)))
                if number != 0:
                    window.blit(images[number-1], (self.posX + self.blockSize * column + margin * column,
                                                   self.posY + row * self.blockSize + row * margin))
