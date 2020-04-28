import pygame as pg


def drawRect(display, color, x, y, w, outlineColor=(0, 0, 0), outlineWidth=1):
    pg.draw.rect(display, outlineColor, pg.Rect(x, y, w, w))
    pg.draw.rect(display, color, pg.Rect(x+outlineWidth, y +
                                         outlineWidth, w-outlineWidth*2, w-outlineWidth*2))


class Figure:
    """ This class can be used to generate a figure.
        You can choose one of the original shapes that are
        O, I, S, Z, L, J and T. Input that one of those as
        string args to generate them. """

    O = [[[1, 1],
          [1, 1]]] * 4

    I = [[[0, 2, 0, 0],
          [0, 2, 0, 0],
          [0, 2, 0, 0],
          [0, 2, 0, 0]],

         [[0, 0, 0, 0],
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
          [0, 0, 0, 0]]]

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

    L = [[[0, 5, 0],
          [0, 5, 0],
          [0, 5, 5]],

         [[0, 0, 0],
          [5, 5, 5],
          [5, 0, 0]],

         [[5, 5, 0],
          [0, 5, 0],
          [0, 5, 0]],

         [[0, 0, 5],
          [5, 5, 5],
          [0, 0, 0]]]

    J = [[[0, 6, 0],
          [0, 6, 0],
          [6, 6, 0]],

         [[6, 0, 0],
          [6, 6, 6],
          [0, 0, 0]],

         [[0, 6, 6],
          [0, 6, 0],
          [0, 6, 0]],

         [[0, 0, 0],
          [6, 6, 6],
          [0, 0, 6]]]

    T = [[[0, 0, 0],
          [7, 7, 7],
          [0, 7, 0]],

         [[0, 7, 0],
          [7, 7, 0],
          [0, 7, 0]],

         [[0, 7, 0],
          [7, 7, 7],
          [0, 0, 0]],

         [[0, 7, 0],
          [0, 7, 7],
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

    def copy(self):
        return Figure(self.colour,self.shape,(self.posX,self.posY),self.blockSize)

    def fall(self):
        self.posY += self.blockSize

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

    def rotate_clockwise(self):
        self.currentRotation = (self.currentRotation + 1) % 4

    def rotate_anticlockwise(self):
        self.currentRotation = (self.currentRotation - 1) % 4

    def move_left(self):
        self.sideways_speed -= 2

    def move_right(self):
        self.sideways_speed += 2

    def move_down(self):
        self.downwards_speed += 2

    def counter_move_down(self):
        self.downwards_speed -= 2

    def fall(self):
        self.posY += self.blockSize

    def drawFigure(self, window):
        shape = self.shapeList[self.currentRotation]

        for y, row in enumerate(shape):
            for x, element in enumerate(row):
                if element:
                    drawRect(window, self.colour, self.posX + x * self.blockSize,
                             self.posY + y * self.blockSize, self.blockSize)

