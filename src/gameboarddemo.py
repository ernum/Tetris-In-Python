import pygame as pg
import figure
import gameboard


BG_COLOR = (0, 0, 0)
FPS = 60
width, height = 500, 500
dis = pg.display.set_mode((width, height))

pg.init()
clock = pg.time.Clock()

shapes = ["O", "I", "S", "Z", "L", "J", "T"]
currentShapeNumber = 0
board_rows = 18
board_cols = 14
gb = gameboard.Board((255, 255, 255), ((width - 20*board_cols)/2),
                     ((height - 20*board_rows)/2), 18, 14, 20)
f = figure.Figure((250, 250, 0), shapes[currentShapeNumber], (250, 250), 20)

while True:
    dis.fill(BG_COLOR)
    # f.drawFigure(dis)
    gb.drawFigure(dis)

    pg.display.update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            raise SystemExit

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                f.rotateRight()
            elif event.key == pg.K_LEFT:
                f.rotateLeft()
            elif event.key == pg.K_1:
                currentShapeNumber = 0
                f = figure.Figure(
                    (250, 250, 0), shapes[currentShapeNumber], (250, 250), 20)
            elif event.key == pg.K_2:
                currentShapeNumber = 1
                f = figure.Figure(
                    (20, 250, 250), shapes[currentShapeNumber], (250, 250), 20)
            elif event.key == pg.K_3:
                currentShapeNumber = 2
                f = figure.Figure(
                    (0, 255, 0), shapes[currentShapeNumber], (250, 250), 20)
            elif event.key == pg.K_4:
                currentShapeNumber = 3
                f = figure.Figure(
                    (255, 0, 0), shapes[currentShapeNumber], (250, 250), 20)
            elif event.key == pg.K_5:
                currentShapeNumber = 4
                f = figure.Figure(
                    (255, 150, 20), shapes[currentShapeNumber], (250, 250), 20)
            elif event.key == pg.K_6:
                currentShapeNumber = 5
                f = figure.Figure(
                    (0, 0, 255), shapes[currentShapeNumber], (250, 250), 20)
            elif event.key == pg.K_7:
                currentShapeNumber = 6
                f = figure.Figure(
                    (200, 20, 250), shapes[currentShapeNumber], (250, 250), 20)

    clock.tick(FPS)
