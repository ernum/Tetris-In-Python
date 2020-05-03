import pygame as pg
#from gameboarddemo import BLOCK_SIZE, board_rows, board_cols, width, height

BLOCK_SIZE = 21
board_rows = 18
board_cols = 10
width = 500
height = 500
FPS = 60
clock = pg.time.Clock()

class Animation:
    def __init__(self, surfaces, pos):
        self.surfaces = surfaces
        self.pos = pos

    def play(self, display):
        beforeBlit = display.copy()
        for i in self.surfaces:
            display.blit(beforeBlit,(0,0))
            display.blit(i,self.pos)
            pg.display.update()
            clock.tick(FPS)


class RowAnimation(Animation):
    def __init__(self, rows, surfWithRows, surfWithoutRows):
        self.rows = rows

        surfaces = []
        frames = 30

        pos = (width // 2 - board_cols // 2 * BLOCK_SIZE, 0)
        surfW, surfH = board_cols * BLOCK_SIZE, board_rows * BLOCK_SIZE

        speed = 8

        for i in range(frames):
            alpha = 255 - int(i / frames * 255)

            surf = pg.Surface((surfW, surfH), pg.SRCALPHA)

            for row in rows:
                oldR = surfWithRows.subsurface((pos[0] + surfW // 2, row * BLOCK_SIZE, surfW // 2, BLOCK_SIZE))
                oldL = surfWithRows.subsurface((pos[0], row * BLOCK_SIZE, surfW // 2, BLOCK_SIZE))
                new = surfWithoutRows.subsurface((pos[0], row * BLOCK_SIZE, surfW, BLOCK_SIZE))
                oldL.set_alpha(alpha)
                oldR.set_alpha(alpha)
                surf.blit(new, (0, row * BLOCK_SIZE))
                surf.blit(oldL, (-speed * i, row * BLOCK_SIZE))
                surf.blit(oldR, (surfW // 2 + speed * i, row * BLOCK_SIZE))

                pg.draw.rect(surf,(255,255,255,70),(-speed * i - board_cols // 2 * BLOCK_SIZE, row * BLOCK_SIZE, surfW, BLOCK_SIZE))
                pg.draw.rect(surf,(255,255,255,70),(surfW // 2 + speed * i, row * BLOCK_SIZE, surfW, BLOCK_SIZE))


            surfaces.append(surf)

        Animation.__init__(self,surfaces, pos)

class LandAnimation:
    def __init__(self, fig, frames):
        self.figure = fig
        self.currFig = -1
        self.finished = False
        self.frames = frames
        self.surf = self.next()


    def next(self):
        self.currFig += 1
        if self.currFig >= self.frames - 1:
            self.finished = True


    def draw(self, dis):
        maxAlpha = 100
        alpha = int(maxAlpha - ((self.currFig - self.frames / 2) ** 2 / (self.frames ** 2 / 4)) * maxAlpha)
        surf = pg.Surface((board_cols * BLOCK_SIZE, board_rows * BLOCK_SIZE), pg.SRCALPHA)
        shape = self.figure.shapeList[self.figure.currentRotation]

        for i in range(len(shape)):
            row = shape[i]
            for j in range(len(row)):
                val = row[j]
                if val != 0:
                    pg.draw.rect(surf, (255, 255, 255, alpha), (
                    (j - 1 + self.figure.matrixPosX) * BLOCK_SIZE, (i + self.figure.matrixPosY) * BLOCK_SIZE,
                    BLOCK_SIZE, BLOCK_SIZE))

        dis.blit(surf,(width // 2 - board_cols // 2 * BLOCK_SIZE, 0))
