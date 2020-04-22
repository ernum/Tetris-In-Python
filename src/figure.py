import pygame
import sys


class Figure(object):
    """ This class can be used to generate a figure.
        You can choose one of the original shapes that are
        O, I, S, Z, L, J and T. Input that one of those as
        string args to generate them. """

    O = [[1, 1, 0, 0],
         [1, 1, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]
    I = [[1, 0, 0, 0],
         [1, 0, 0, 0],
         [1, 0, 0, 0],
         [1, 0, 0, 0]]
    S = [[0, 1, 1, 0],
         [1, 1, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]
    Z = [[1, 1, 0, 0],
         [0, 1, 1, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]
    L = [[1, 0, 0, 0],
         [1, 0, 0, 0],
         [1, 1, 0, 0],
         [0, 0, 0, 0]]
    J = [[0, 1, 0, 0],
         [0, 1, 0, 0],
         [1, 1, 0, 0],
         [0, 0, 0, 0]]
    T = [[1, 1, 1, 0],
         [0, 1, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]

    def __init__(self, *colour: tuple, shape: str):
        pygame.init()
        self.colour = colour
        self.shape = shape

    def shape_from_input(self):
        return {
            'O': self.O,
            'I': self.I,
            'S': self.S,
            'Z': self.Z,
            'L': self.L,
            'J': self.J,
            'T': self.T,
        }.get(self.shape, None)

    def drawFigure(self):
        # Följande kan vi flytta till gameboard när vi börjar med den.
        window = pygame.display.set_mode([640, 600])
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            window.fill((0, 0, 0))

            shape = self.shape_from_input()
            if shape:  # None is a falsy value so returns false if element is 0
                for y, row in enumerate(shape):
                    for x, element in enumerate(row):
                        if element:
                            pygame.draw.rect(window, self.colour,
                                             pygame.draw.rect(window, self.colour, pygame.Rect(((20*x)+20, (20*y)+20), (20, 20))))
                pygame.display.update()
            else:
                raise ValueError(
                    'The shape {} does not exist.'.format(self.shape))


figure = Figure((255, 255, 255), shape="O")
figure.drawFigure()
