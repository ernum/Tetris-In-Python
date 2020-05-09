from . import figure
import pygame as pg
import random

allShapes = ("O", "I", "S", "Z", "L", "J", "T")
shapeColors = ((250, 250, 0), (20, 250, 250), (0, 255, 0),
               (255, 0, 0), (255, 150, 20), (0, 0, 255), (200, 20, 250))


def randomShape(blockSize):
    randInt = random.randint(0, len(allShapes)-1)
    shape = allShapes[randInt]
    color = shapeColors[randInt]

    return figure.Figure(color, shape, (0, 0), blockSize)


class figureQueue:
    def __init__(self, queueSize, blockSize):
        self.queueSize = queueSize
        self.blockSize = blockSize
        self.buffer = [randomShape(blockSize) for _ in range(queueSize)]

    def __len__(self):
        return self.queueSize

    def next(self):
        first = self.buffer[0]
        self.buffer = self.buffer[1:] + [randomShape(self.blockSize)]
        return first

    def getSurface(self, width, height):
        surf = pg.Surface((width, height))
        pg.draw.rect(surf, (255, 255, 255), (0, 0, width, height), 2)

        shapeWidth = width
        shapeHeight = height // (self.queueSize + 1)

        font = pg.font.Font("../fonts/VCR_OSD_MONO_1.ttf",
                            int(shapeHeight*0.8))
        textSurf = font.render("Next", True, (255, 255, 255))
        textSize = textSurf.get_rect().size
        surf.blit(textSurf, ((
            shapeWidth-textSize[0])/2, (shapeHeight-textSize[1])/2, textSize[0], textSize[1]))
        x = 0
        y = shapeHeight
        for i in self.buffer:
            miniShape = i.copy()
            miniShape.blockSize = shapeHeight // 5
            shapeSize = len(miniShape.shapeList[0])
            miniShape.posX = x + shapeWidth/2 - shapeSize/2*miniShape.blockSize
            if miniShape.shape == "I":
                miniShape.posX += miniShape.blockSize / 2
            miniShape.posY = y + shapeHeight/2 - shapeSize/2*miniShape.blockSize
            miniShape.drawFigure(surf)
            y += shapeHeight

        return surf

    def draw(self, dis, x, y, width, height):
        dis.blit(self.getSurface(width, height), (x, y))
