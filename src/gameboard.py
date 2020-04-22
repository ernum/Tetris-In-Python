import pygame as pg
import figure

BG_COLOR = (0,0,0)
FPS = 60
width, height = 500,500
dis = pg.display.set_mode((width,height))

pg.init()
clock = pg.time.Clock()

shapes = ["O", "I", "S", "Z", "L", "J", "T"]
currentShapeNumber = 0
f = figure.Figure((255,255,255),shapes[currentShapeNumber],(250,250),20)

while True:
    dis.fill(BG_COLOR)

    f.drawFigure(dis)

    pg.display.update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            raise SystemExit

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                f.rotateRight()
            elif event.key == pg.K_LEFT:
                f.rotateLeft()
            elif event.key == pg.K_SPACE:
                currentShapeNumber = (currentShapeNumber + 1) % len(shapes)
                f = figure.Figure((255, 255, 255), shapes[currentShapeNumber], (250, 250), 20)

    clock.tick(FPS)
