import pygame


class Figure(object):
    """ This class can be used to generate a figure.
        You can choose one of the original shapes that are
        O, I, S, Z, L, J and T. Input that one of those as
        string args to generate them. """

    O = [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]
    I = [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]
    S = [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]
    Z = [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]
    L = [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]
    J = [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]
    T = [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]

    def __init__(self, *colour: tuple, shape: str):
        pygame.init()
        self.colour = colour
        self.shape = shape

    def drawFigure(self):
        # Följande kan vi flytta till gameboard när vi börjar med den.
        window = pygame.display.set_mode([640, 600])
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            window.fill((0, 0, 0))

            for i in range(len(self.O)):
                for j in range(len(self.O[i])):
                    if self.O[j] == 0:
                        pygame.draw.rect(window, self.colour,
                                         pygame.Rect(20, 20, 20, 20))
                    pygame.display.update()


figure = Figure((255, 255, 255), shape="O")
figure.drawFigure()
