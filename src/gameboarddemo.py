import pygame as pg
import figure
import gameboard
import generateShapes
import pygameTitleScreen
import math


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

BLOCK_SIZE = 20

# Music
pg.mixer.init()
pg.mixer.music.load("../Sound/electrifyLowerTempDelayed.wav")
pg.mixer.music.play(-1)
pg.mixer.music.set_volume(0.6)

pygameTitleScreen.titlePage(dis)
start_pos = (width/2 - 15, 20)
gb = gameboard.Board((255, 255, 255), ((width - 21*board_cols)/2),
                     0, 18, 14, 20)

def matrix_merge(currentMatrix, figure):
    # Right now first pos of fig ([0]). Will need to get the right rotation as well.
    rotation = figure.currentRotation
    fig_m = figure.shapeList[rotation]

    collisionFound = False
    newMatrix = [[i for i in row] for row in currentMatrix]
    for j in range(len(fig_m[0])):
        for i in range(len(fig_m)):
            if fig_m[j][i] != 0:
                row = j + figure.matrixPosY
                column = i + figure.matrixPosX
                under = currentMatrix[row+1][column]
                if under != 0:
                    collisionFound = True
                newMatrix[row][column] = fig_m[j][i]

    return newMatrix, collisionFound


def checkCollision(currentMatrix, figure, movement, rotation):
    # Right now first pos of fig ([0]). Will need to get the right rotation as well.
    fig_m = figure.shapeList[(figure.currentRotation + rotation) % 4]

    for j in range(len(fig_m[0])):
        for i in range(len(fig_m)):
            if fig_m[j][i] != 0:
                row = j + figure.matrixPosY + movement[1]
                column = i  + figure.matrixPosX + movement[0]
                nextBlock = currentMatrix[row][column]
                if nextBlock != 0:
                    return True
    return False
  
def nextShape(queue, currentMatrix):
    figure = queue.next()
    fig_m = figure.shape_from_input(shapes[currentShapeNumber])[figure.currentRotation]
    middle = len(currentMatrix[0])//2 - len(fig_m)//2
    figure.matrixPosX = middle
    return figure

def gameOver(figure, matrix):
    top_row = [a for a in matrix[0]]
    for i in top_row:
        if i != 0 and i != 8:
            return True
    return False


tickRate = 1  # Times per second shapes are falling downwards

tickCount = 1
pos = [0, 0]
queue = generateShapes.figureQueue(4, BLOCK_SIZE)
f = nextShape(queue, gb.board)

while True:

    dis.fill(BG_COLOR)
    queue.draw(dis, width-90, 0, 90, 200)

    drawMatrix, collision = matrix_merge(gb.board, f)
    gb.drawMatrix(dis, drawMatrix)

    if collision:
        gb.board = drawMatrix
        f = nextShape(queue, gb.board)

    if gameOver(f, gb.board):
        raise SystemExit
    
    pg.display.update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            raise SystemExit

        if event.type == pg.KEYDOWN:
            # Controls
            if event.key == pg.K_x:
                if f.shape != 'I':
                    movements = [[(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],  # 0 >> 1
                                 [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],  # 1 >> 2
                                 [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],  # 2 >> 3
                                 [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)]]  # 3 >> 0
                else:
                    movements = [[(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)], # 0 >> 1                   
                                 [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)], # 1 >> 2
                                 [(0, 0), (2, 0), (-1, 0), (2, 1), (-1,-2)],  # 2 >> 3
                                 [( 0, 0), (1, 0), (-2, 0), (1,-2), (-2, 1)]] # 3 >> 0
                # Test movements
                for i in movements[f.currentRotation]:
                    if not checkCollision(gb.board, f, i, 1):
                        f.rotate_clockwise()
                        f.move(i)
                        break

            if event.key == pg.K_z:
                if f.shape != 'I':
                    movements = [[(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],  # 0 >> 3
                                 [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)], # 1 >> 0
                                 [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],  # 2 >> 1
                                 [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)]]  # 3 >> 2
                else:
                    movements = [[(0, 0), (-1, 0), (2, 0), (-1, 2), (2,-1)],  # 0 >> 3
                                 [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)], # 1 >> 0
                                 [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],  # 2 >> 1
                                 [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)]]   # 3 >> 2
                # Test movements
                for i in movements[f.currentRotation]:
                    if not checkCollision(gb.board, f, i, -1):
                        f.rotate_anticlockwise()
                        f.move(i)
                        break

            if event.key == pg.K_LEFT:
                if not checkCollision(gb.board, f, (-1, 0), 0):
                    f.move_left()
            if event.key == pg.K_RIGHT:
                if not checkCollision(gb.board, f, (1, 0), 0):
                    f.move_right()
            if event.key == pg.K_DOWN:
                f.move_down()

            # Demo content
            if event.key == pg.K_1:
                currentShapeNumber = 0
                f = figure.Figure(
                    (250, 250, 0), shapes[currentShapeNumber], (f.posX, f.posY), 20)
            elif event.key == pg.K_2:
                currentShapeNumber = 1
                f = figure.Figure(
                    (20, 250, 250), shapes[currentShapeNumber], (f.posX, f.posY), 20)
            elif event.key == pg.K_3:
                currentShapeNumber = 2
                f = figure.Figure(
                    (0, 255, 0), shapes[currentShapeNumber], (f.posX, f.posY), 20)
            elif event.key == pg.K_4:
                currentShapeNumber = 3
                f = figure.Figure(
                    (255, 0, 0), shapes[currentShapeNumber], (f.posX, f.posY), 20)
            elif event.key == pg.K_5:
                currentShapeNumber = 4
                f = figure.Figure(
                    (255, 150, 20), shapes[currentShapeNumber], (f.posX, f.posY), 20)
            elif event.key == pg.K_6:
                currentShapeNumber = 5
                f = figure.Figure(
                    (0, 0, 255), shapes[currentShapeNumber], (f.posX, f.posY), 20)
            elif event.key == pg.K_7:
                currentShapeNumber = 6
                f = figure.Figure(
                    (200, 20, 250), shapes[currentShapeNumber], (f.posX, f.posY), 20)

    if tickCount % (FPS/tickRate) == 0:
        f.fall()
    clock.tick(FPS)
    tickCount += 1
