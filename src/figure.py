import pygame as pg


class Figure:
    """ This class can be used to generate a figure.
        You can choose one of the original shapes that are
        O, I, S, Z, L, J and T. Input that one of those as
        string args to generate them. """

    O = [[[1, 1, 0, 0],
          [1, 1, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0]]]*4

    I = [[[1, 0, 0, 0],
          [1, 0, 0, 0],
          [1, 0, 0, 0],
          [1, 0, 0, 0]],

         [[1, 1, 1, 1],
          [0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0]],

         [[1, 0, 0, 0],
          [1, 0, 0, 0],
          [1, 0, 0, 0],
          [1, 0, 0, 0]],

         [[1, 1, 1, 1],
          [0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0]]]

    S = [[[0, 1, 1, 0],
          [1, 1, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0]],

         [[1, 0, 0, 0],
          [1, 1, 0, 0],
          [0, 1, 0, 0],
          [0, 0, 0, 0]],

         [[0, 1, 1, 0],
          [1, 1, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0]],

         [[1, 0, 0, 0],
          [1, 1, 0, 0],
          [0, 1, 0, 0],
          [0, 0, 0, 0]]]

    Z = [[[1, 1, 0, 0],
          [0, 1, 1, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0]],

         [[0, 1, 0, 0],
          [1, 1, 0, 0],
          [1, 0, 0, 0],
          [0, 0, 0, 0]],

         [[1, 1, 0, 0],
          [0, 1, 1, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0]],

         [[0, 1, 0, 0],
          [1, 1, 0, 0],
          [1, 0, 0, 0],
          [0, 0, 0, 0]]]

    L = [[[1, 0, 0, 0],
          [1, 0, 0, 0],
          [1, 1, 0, 0],
          [0, 0, 0, 0]],

         [[1, 1, 1, 0],
          [1, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0]],

         [[1, 1, 0, 0],
          [0, 1, 0, 0],
          [0, 1, 0, 0],
          [0, 0, 0, 0]],

         [[0, 0, 1, 0],
          [1, 1, 1, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0]]]

    J = [[[0, 1, 0, 0],
          [0, 1, 0, 0],
          [1, 1, 0, 0],
          [0, 0, 0, 0]],

         [[1, 0, 0, 0],
          [1, 1, 1, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0]],

         [[1, 1, 0, 0],
          [1, 0, 0, 0],
          [1, 0, 0, 0],
          [0, 0, 0, 0]],

         [[1, 1, 1, 0],
          [0, 0, 1, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0]]]

    T = [[[1, 1, 1, 0],
          [0, 1, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0]],

         [[0, 1, 0, 0],
          [1, 1, 0, 0],
          [0, 1, 0, 0],
          [0, 0, 0, 0]],

         [[0, 1, 0, 0],
          [1, 1, 1, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0]],

         [[1, 0, 0, 0],
          [1, 1, 0, 0],
          [1, 0, 0, 0],
          [0, 0, 0, 0]]]

    def __init__(self, colour, shape, startPos, blockSize):
        self.colour = colour
        self.shapeList = self.shape_from_input(shape)
        self.currentRotation = 0
        self.posX, self.posY = startPos
        self.blockSize = blockSize

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

        if not s:  # None is a falsy value so returns false.
            raise ValueError(
                'The shape {} does not exist.'.format(self.shapeList))
        return s

    def rotateRight(self):
        self.currentRotation = (self.currentRotation + 1) % 4

    def rotateLeft(self):
        self.currentRotation = (self.currentRotation - 1) % 4

    def drawFigure(self, window):
        shape = self.shapeList[self.currentRotation]

        for y, row in enumerate(shape):
            for x, element in enumerate(row):
                if element:
                    pg.draw.rect(window, self.colour, pg.Rect(
                        self.posX + x * self.blockSize, self.posY + y * self.blockSize, self.blockSize, self.blockSize))
