import pygame as pg
import figure
import gameboard
import generateShapes
import pygameTitleScreen
import time
from UI import *

BG_COLOR = (0, 0, 0)
FPS = 60
width, height = 500, 500
dis = pg.display.set_mode((width, height))
pg.init()
clock = pg.time.Clock()

shapes = ["O", "I", "S", "Z", "L", "J", "T"]
currentShapeNumber = 0
board_rows = 18
board_cols = 12

BLOCK_SIZE = 20

# Music
pg.mixer.init()
pg.mixer.music.load("../Sound/noraprap (1).wav")
pg.mixer.music.play(-1)
pg.mixer.music.set_volume(0.6)

pygameTitleScreen.titlePage(dis)
start_pos = (width/2 - 15, 20)
gb = gameboard.Board((255, 255, 255), ((width - 21*board_cols)/2),
                     0, board_rows, board_cols, 20)


def matrix_merge(currentMatrix, figure):
    rotation = figure.currentRotation
    fig_m = figure.shapeList[rotation]

    newMatrix = [[i for i in row] for row in currentMatrix]
    for j in range(len(fig_m[0])):
        for i in range(len(fig_m)):
            if fig_m[j][i] != 0:
                row = j + figure.matrixPosY
                column = i + figure.matrixPosX
                current = newMatrix[row][column]
                if current == 0:
                    newMatrix[row][column] = fig_m[j][i]

    return newMatrix


def checkCollision(currentMatrix, figure, movement, rotation):
    fig_m = figure.shapeList[(figure.currentRotation + rotation) % 4]

    for j in range(len(fig_m[0])):
        for i in range(len(fig_m)):
            if fig_m[j][i] != 0:
                row = j + figure.matrixPosY + movement[1]
                column = i + figure.matrixPosX + movement[0]
                nextBlock = currentMatrix[row][column]
                if nextBlock != 0:
                    return True
    return False


def nextShape(queue, currentMatrix):
    figure = queue.next()
    fig_m = figure.shape_from_input(shapes[currentShapeNumber])[
        figure.currentRotation]
    middle = len(currentMatrix[0])//2 - len(fig_m)//2
    figure.matrixPosX = middle
    return figure


def gameOver(figure, matrix):
    top_row = [a for a in matrix[0]]
    for i in top_row:
        if i != 0 and i != 8:
            return True
    return False

# Checks the board matrix for full rows from the bottom.


def row_check(currentMatrix):
    removed_index = []
    for r in range(len(currentMatrix)-2, -1, -1):
        full_rows = [True for n in range(len(currentMatrix[0])-2)]
        for k in range(1, len(currentMatrix[r])-1):
            if currentMatrix[r][k] == 0:
                full_rows[k-1] = False
        if all(full_rows):
            removed_index.append(r)
            currentMatrix[r][1:len(currentMatrix[0]) -
                             1] = [0 for n in range(len(currentMatrix[0])-2)]
    return currentMatrix, removed_index


# Removes empty row and updates the board
def empty_row_removal(currentMatrix, removed_index):
    for i in removed_index:
        for r in range(removed_index[0], -1, -1):
            if r == 0:
                currentMatrix[r][1:len(
                    currentMatrix[r]) - 1] = [0 for n in range(len(currentMatrix[0]) - 2)]
            else:
                currentMatrix[r] = currentMatrix[r - 1]
    return currentMatrix


def rotationCollision(figure, clockwise):
    if clockwise > 1:
        if f.shape != 'I':
            movements = [[(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],  # 0 >> 1
                         [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],  # 1 >> 2
                         [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],  # 2 >> 3
                         [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)]]  # 3 >> 0
        else:
            movements = [[(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],  # 0 >> 1
                         [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],  # 1 >> 2
                         [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],  # 2 >> 3
                         [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)]]  # 3 >> 0
    else:
        if f.shape != 'I':
            movements = [[(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],  # 0 >> 3
                         [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],  # 1 >> 0
                         [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],  # 2 >> 1
                         [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)]]  # 3 >> 2
        else:
            movements = [[(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],  # 0 >> 3
                         [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],  # 1 >> 0
                         [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],  # 2 >> 1
                         [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)]]  # 3 >> 2

    # Test movements
    for i in movements[f.currentRotation]:
        if not checkCollision(gb.board, f, i, 1 if clockwise else -1):
            f.rotate_clockwise() if clockwise else f.rotate_anticlockwise()
            f.move(i)
            break


def moveIfPossible(board, f, move):
    if not checkCollision(board, f, move, 0):
        f.move(move)
        return True
    return False


def drawGhost(board, drawMatrix, figure):
    for down in range(1, len(board)):
        if checkCollision(board, figure, (0, down), 0):
            ghost = figure.ghostCopy()
            ghost.move((0, down-1))
            newMatrix = matrix_merge(drawMatrix, ghost)
            return newMatrix


def exit():
    raise SystemExit


def play():
    global playAgain
    playAgain = True


def reset():
    gb = gameboard.Board((255, 255, 255), ((width - 21*board_cols)/2),
                         0, board_rows, board_cols, 20)
    drawMatrix = matrix_merge(gb.board, f)
    ghostMatrix = drawGhost(gb.board, drawMatrix, f)
    gb.drawMatrix(dis, ghostMatrix)
    pg.display.update()


tickRate = 1  # Times per second shapes are falling downwards
tickCount = 1

queue = generateShapes.figureQueue(4, BLOCK_SIZE)
f = nextShape(queue, gb.board)

sliderWidth = 20
sliderHeight = 60
sliderMargin = 20
sliderRect = (width - sliderWidth - sliderMargin, height -
              sliderHeight - sliderMargin, sliderWidth, sliderHeight)

volumeIconW = 40
muteClickRadius = 20

volume = VolumeController(sliderRect, (sliderRect[0] - volumeIconW / 2 - 10, sliderRect[1] + sliderRect[3] / 2),
                          muteClickRadius)

volume.val = pg.mixer.music.get_volume()
volume.muted = pygameTitleScreen.muted

keyCheckRate = 20  # How many times per second the game checks if a key is held down
das = 0.2  # delayed auto shift, how long after pressing a key it will be checked again. In seconds

lastPressed = [0, 0, 0]  # Left, Down, Right

while True:

    dis.fill(BG_COLOR)
    queue.draw(dis, width-90, 0, 90, 200)

    drawMatrix = matrix_merge(gb.board, f)
    ghostMatrix = drawGhost(gb.board, drawMatrix, f)
    gb.drawMatrix(dis, ghostMatrix)

    if gameOver(f, gb.board):

        fontPath = "../fonts/VCR_OSD_MONO_1.ttf"
        global playAgain
        playAgain = False
        gameOverFontSize = 50
        buttonWidth = 150
        buttonHeight = 50
        buttonFontSize = 20
        buttonHoverColor = (200, 200, 200)

        game = Text("GAME", (0, 0, 0),
                    gameOverFontSize, (250, 100))
        over = Text("OVER", (0, 0, 0),
                    gameOverFontSize, (250, 150))
        playAgainButton = Button((175, 200, buttonWidth, buttonHeight),
                                 (255, 255, 255), 0, (100, 100, 100), "PLAY AGAIN", buttonFontSize, (0, 0, 0), play, buttonHoverColor)
        exit_button = Button((175, 255, buttonWidth, buttonHeight),
                      (255, 255, 255), 0, (100, 100, 100), "EXIT", buttonFontSize, (0, 0, 0), exit, buttonHoverColor)

        for i in range(len(gb.board)-2, -1, -1):
            for j in range(1, len(gb.board[i])-1):
                gb.board[i][j] = 8
                drawMatrix = matrix_merge(gb.board, f)
                gb.drawMatrix(dis, drawMatrix)
                pg.display.update()
                clock.tick(FPS)

        while not playAgain:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    raise SystemExit

            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                p = pg.mouse.get_pos()
                if playAgainButton.isInside(p):
                    playAgainButton.click()
                if exit_button.isInside(p):
                    exit_button.click()

            if playAgainButton.isInside(pg.mouse.get_pos()):
                playAgainButton.hover()
            else:
                playAgainButton.noHover()

            if exit_button.isInside(pg.mouse.get_pos()):
                exit_button.hover()
            else:
                exit_button.noHover()

            game.draw(dis)
            over.draw(dis)
            playAgainButton.draw(dis)
            exit_button.draw(dis)
            pg.display.update()
        reset()

    volume.draw(dis)
    pg.display.update()

    if pg.mouse.get_pressed()[0]:
        if volume.update():
            pg.mixer.music.set_volume(volume.val)

    if tickCount % (FPS//tickRate) == 0:
        if not checkCollision(gb.board, f, (0, 1), 0):
            f.fall()
        else:
            gb.board = drawMatrix
            gb.board, removed_index = row_check(gb.board)
            if len(removed_index) > 0:
                gb.board = empty_row_removal(gb.board, removed_index)

            f = nextShape(queue, gb.board)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            raise SystemExit

        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            p = pg.mouse.get_pos()
            if volume.buttonInside(p):
                volume.click()

        if event.type == pg.KEYDOWN:
            # Controls
            if event.key == pg.K_x:
                rotationCollision(f, True)
            if event.key == pg.K_z:
                rotationCollision(f, False)

            if event.key == pg.K_LEFT:
                moveIfPossible(gb.board, f, (-1, 0))
                lastPressed[0] = time.time()
            if event.key == pg.K_DOWN:
                moveIfPossible(gb.board, f, (0, 1))
                lastPressed[1] = time.time()
            if event.key == pg.K_RIGHT:
                moveIfPossible(gb.board, f, (1, 0))
                lastPressed[2] = time.time()

    pressed = pg.key.get_pressed()

    t = time.time()
    if tickCount % (FPS//keyCheckRate) == 0:
        if pressed[pg.K_LEFT] and t-lastPressed[0] >= das:
            moveIfPossible(gb.board, f, (-1, 0))

        if pressed[pg.K_RIGHT] and t-lastPressed[2] >= das:
            moveIfPossible(gb.board, f, (1, 0))

        if pressed[pg.K_DOWN] and t-lastPressed[1] >= das:
            moveIfPossible(gb.board, f, (0, 1))

    clock.tick(FPS)
    tickCount += 1
