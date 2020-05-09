import pygame as pg
from .gameboard import images


def drawRect(display, imageNumber, x, y, w):
    image = pg.transform.scale(images[imageNumber-1], (w, w))
    display.blit(image, (x, y, w, w))


class Figure:
    """ This class can be used to generate a figure.
        You can choose one of the original shapes that are
        O, I, S, Z, L, J and T. Input that one of those as
        string args to generate them. """

    O = [[[1, 1],
          [1, 1]]] * 4

    I = [[[0, 0, 0, 0],
          [2, 2, 2, 2],
          [0, 0, 0, 0],
          [0, 0, 0, 0]],

         [[0, 0, 2, 0],
          [0, 0, 2, 0],
          [0, 0, 2, 0],
          [0, 0, 2, 0]],

         [[0, 0, 0, 0],
          [0, 0, 0, 0],
          [2, 2, 2, 2],
          [0, 0, 0, 0]],

         [[0, 2, 0, 0],
          [0, 2, 0, 0],
          [0, 2, 0, 0],
          [0, 2, 0, 0]]]

    S = [[[0, 3, 3],
          [3, 3, 0],
          [0, 0, 0]],

         [[0, 3, 0],
          [0, 3, 3],
          [0, 0, 3]],

         [[0, 0, 0],
          [0, 3, 3],
          [3, 3, 0]],

         [[3, 0, 0],
          [3, 3, 0],
          [0, 3, 0]]]

    Z = [[[4, 4, 0],
          [0, 4, 4],
          [0, 0, 0]],

         [[0, 0, 4],
          [0, 4, 4],
          [0, 4, 0]],

         [[0, 0, 0],
          [4, 4, 0],
          [0, 4, 4]],

         [[0, 4, 0],
          [4, 4, 0],
          [4, 0, 0]]]

    L = [[[0, 0, 5],
          [5, 5, 5],
          [0, 0, 0]],

         [[0, 5, 0],
          [0, 5, 0],
          [0, 5, 5]],

         [[0, 0, 0],
          [5, 5, 5],
          [5, 0, 0]],

         [[5, 5, 0],
          [0, 5, 0],
          [0, 5, 0]]]

    J = [[[6, 0, 0],
          [6, 6, 6],
          [0, 0, 0]],

         [[0, 6, 6],
          [0, 6, 0],
          [0, 6, 0]],

         [[0, 0, 0],
          [6, 6, 6],
          [0, 0, 6]],

         [[0, 6, 0],
          [0, 6, 0],
          [6, 6, 0]]]

    T = [[[0, 7, 0],
          [7, 7, 7],
          [0, 0, 0]],

         [[0, 7, 0],
          [0, 7, 7],
          [0, 7, 0]],

         [[0, 0, 0],
          [7, 7, 7],
          [0, 7, 0]],

         [[0, 7, 0],
          [7, 7, 0],
          [0, 7, 0]]]

    def __init__(self, colour, shape, startPos, blockSize):
        self.colour = colour
        self.shape = shape
        self.shapeList = self.shape_from_input(shape)
        self.currentRotation = 0
        self.sideways_speed = 0
        self.downwards_speed = 0
        self.posX, self.posY = startPos
        self.blockSize = blockSize
        self.matrixPosX = 0
        self.matrixPosY = 0
        self.imageNumber = 0

        for i in self.shapeList[0]:
            for j in i:
                if j != 0:
                    self.imageNumber = j
                    break

    def copy(self):
        newF = Figure(self.colour, self.shape,
                      (self.posX, self.posY), self.blockSize)
        newF.matrixPosX = self.matrixPosX
        newF.matrixPosY = self.matrixPosY
        newF.currentRotation = self.currentRotation
        return newF

    def ghostCopy(self):
        f = self.copy()
        f.shapeList = [[[0 for val in row] for row in shape]
                       for shape in f.shapeList]
        for i in range(4):
            shape = f.shapeList[i]
            for j in range(len(shape)):
                row = shape[j]
                for k in range(len(row)):
                    val = self.shapeList[i][j][k]
                    f.shapeList[i][j][k] = 0 if val == 0 else 9

        return f

    def fall(self):
        self.posY += self.blockSize
        self.matrixPosY += 1

    def move(self, dist):
        xMove, yMove = dist

        self.matrixPosX += xMove
        self.posX += xMove * self.blockSize

        self.matrixPosY += yMove
        self.posY += yMove * self.blockSize

    def shape_from_input(self, shape):
        s = {
            'O': self.O,
            'I': self.I,
            'S': self.S,
            'Z': self.Z,
            'L': self.L,
            'J': self.J,
            'T': self.T,
        }.get(shape)

        if not s:
            raise ValueError(
                'The shape {} does not exist.'.format(self.shapeList))
        return s

    def change_rotation(self, rotation):
        return self.shapeList[rotation]

    def rotate_clockwise(self):
        self.currentRotation = (self.currentRotation + 1) % 4

    def rotate_anticlockwise(self):
        self.currentRotation = (self.currentRotation - 1) % 4

    def move_left(self):
        self.posX -= self.blockSize
        self.matrixPosX -= 1

    def move_right(self):
        self.posX += self.blockSize
        self.matrixPosX += 1

    def move_down(self):
        self.posY += self.blockSize
        self.matrixPosY += 1

    def move_up(self):
        self.posY += self.blockSize
        self.matrixPosY += 1

    def fall(self):
        self.posY += self.blockSize
        self.matrixPosY += 1

    def drawFigure(self, window):
        shape = self.shapeList[self.currentRotation]

        for y, row in enumerate(shape):
            for x, element in enumerate(row):
                if element:
                    drawRect(window, self.imageNumber, self.posX + x * self.blockSize,
                             self.posY + y * self.blockSize, self.blockSize)
