import pygame as pg
import time
from . import Animations
from . import figure
from . import gameboard
from . import generateShapes
from . import pygameGameOverScreen
from . import pygameTitleScreen
from .UI import *


BG_COLOR = (0, 0, 0)
FPS = 60
width, height = 500, 500
dis = pg.display.set_mode((width, height))
pg.mixer.pre_init(44100, -16, 1, 128)
pg.init()
clock = pg.time.Clock()

shapes = ["O", "I", "S", "Z", "L", "J", "T"]
currentShapeNumber = 0
board_rows = 18
board_cols = 12

BLOCK_SIZE = 20

# Paths
MUSIC_SOUND_PATH = pathlib.Path(
    __file__).absolute().parents[1] / "Sound" / "Soundtrack" / "electrify.wav"
SWOOSH_SOUND_PATH = pathlib.Path(
    __file__).absolute().parents[1] / "Sound" / "SoundEffects" / "Swoosh.wav"
IMPACT_SOUND_PATH = pathlib.Path(
    __file__).absolute().parents[1] / "Sound" / "SoundEffects" / "Impact.wav"
REMOVAL_SOUND_PATH = pathlib.Path(
    __file__).absolute().parents[1] / "Sound" / "SoundEffects" / "Removal.wav"
ERROR_SOUND_PATH = pathlib.Path(
    __file__).absolute().parents[1] / "Sound" / "SoundEffects" / "error.wav"
PAUSE_IMG_PATH = pathlib.Path(
    __file__).absolute().parents[1] / "images" / "pauseScreen3.png"

# Music
pg.mixer.init()
pg.mixer.music.load(str(MUSIC_SOUND_PATH))
pg.mixer.music.play(-1)
pg.mixer.music.set_volume(0.6)

# Sound effects
rot_sound = pg.mixer.Sound(str(SWOOSH_SOUND_PATH))
rot_sound.set_volume(0.5)
impact_sound = pg.mixer.Sound(str(IMPACT_SOUND_PATH))
impact_sound.set_volume(0.4)
rem_sound = pg.mixer.Sound(str(REMOVAL_SOUND_PATH))
rem_sound.set_volume(0.5)
err_sound = pg.mixer.Sound(str(ERROR_SOUND_PATH))
err_sound.set_volume(0.5)

sounds = [rot_sound,impact_sound,rem_sound,err_sound]


pygameTitleScreen.titlePage(dis)
start_pos = (width/2 - 15, 20)
gb = gameboard.Board((255, 255, 255), ((width - 21*board_cols)/2),
                     0, board_rows, board_cols, 20)

tickRate = 1  # Times per second shapes are falling downwards
tickCount = 1

queue = generateShapes.figureQueue(4, BLOCK_SIZE)

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

for i in sounds:
    i.set_volume(volume.val)

keyCheckRate = 20  # How many times per second the game checks if a key is held down
das = 0.2  # delayed auto shift, how long after pressing a key it will be checked again. In seconds

lastPressed = [0, 0, 0]  # Left, Down, Right

level = -1
levelText = None
levelTextSize = 50

linesCleared = 0
linesClearedForNewLevel = 10

score = 0

levelTextCenterY = int(height - 0.5 * levelTextSize - 15)
scoreTextCenterY = int(levelTextCenterY - levelTextSize)

pointsPerLine = [40, 100, 300, 1200]


def framePerGridToTickrate(fpg, fps):
    return 1/fpg * fps


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

    if checkCollision(currentMatrix, figure, (0, 0), 0):
        if pygameGameOverScreen.gameOverAnimation(dis, matrix_merge, landAnimation, gb, f, tickReset, volume):
            reset()
        else:
            pygameTitleScreen.titlePage(dis)

    return figure


def gameOver(matrix):
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
                         [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],      # 1 >> 2
                         [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],     # 2 >> 3
                         [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)]]   # 3 >> 0
        else:
            movements = [[(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],  # 0 >> 1
                         [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],  # 1 >> 2
                         [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],  # 2 >> 3
                         [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)]]  # 3 >> 0
    else:
        if f.shape != 'I':
            movements = [[(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],     # 0 >> 3
                         [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],      # 1 >> 0
                         [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],  # 2 >> 1
                         [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)]]   # 3 >> 2
        else:
            movements = [[(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],  # 0 >> 3
                         [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],  # 1 >> 0
                         [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],  # 2 >> 1
                         [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)]]  # 3 >> 2

    # Test movements
    for i in movements[f.currentRotation]:
        if not checkCollision(gb.board, f, i, 1 if clockwise else -1):
            if not volume.muted:
                pg.mixer.Sound.play(rot_sound)
            f.rotate_clockwise() if clockwise else f.rotate_anticlockwise()
            f.move(i)
            return True
    return False


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


def reset():
    gb = gameboard.Board((255, 255, 255), ((width - 21*board_cols)/2),
                         0, board_rows, board_cols, 20)
    drawMatrix = matrix_merge(gb.board, f)
    ghostMatrix = drawGhost(gb.board, drawMatrix, f)
    gb.drawMatrix(dis, ghostMatrix)
    pg.display.update()


def nextLevel():
    global level, levelText, tickRate
    level += 1
    levelText = Text("Level: " + str(level), (255, 255, 255),
                     levelTextSize, (width//2, levelTextCenterY))
    tickRate = levelsTickrate[len(
        levelsTickrate)-1] if level >= len(levelsTickrate) else levelsTickrate[level]


def createScoreText(score):
    return Text("Score: " + str(score), (0, 255, 0), levelTextSize, (width//2, scoreTextCenterY))


def calcPoints(level, linesCleared):
    return pointsPerLine[linesCleared-1] * (level + 1)


levelsFPG = [i for i in range(48, 3, -5)] + [6] + \
    [5]*3 + [4]*3 + [3]*3 + [2]*10 + [1]

levelsTickrate = [framePerGridToTickrate(i, FPS) for i in levelsFPG]
scoreText = createScoreText(0)

f = nextShape(queue, gb.board)
nextLevel()

tickReset = False

landAnimation = None
rowAnimations = True

RUNNING, PAUSE = 1, 0
game_state = RUNNING


while True:
    dis.fill(BG_COLOR)
    queue.draw(dis, width-90, 0, 90, 200)

    drawMatrix = matrix_merge(gb.board, f)
    ghostMatrix = drawGhost(gb.board, drawMatrix, f)

    gb.drawMatrix(dis, ghostMatrix)

    # Draw pause message
    if game_state == PAUSE:
        pause_img = pg.image.load(str(PAUSE_IMG_PATH))
        pause_img = pg.transform.scale(
            pause_img, ((board_cols - 2)*21 + 1, 100))
        dis.blit(pause_img, ((width - 21*board_cols)/2 + BLOCK_SIZE, 70))

    volume.draw(dis)
    levelText.draw(dis)
    scoreText.draw(dis)

    if game_state == RUNNING:
        if gameOver(gb.board):
            if pygameGameOverScreen.gameOverAnimation(dis, matrix_merge, landAnimation, gb, f, tickReset):
                reset()

    if landAnimation != None and not landAnimation.finished:
        landAnimation.draw(dis)
        landAnimation.next()

    if pg.mouse.get_pressed()[0]:
        if volume.update():
            pg.mixer.music.set_volume(volume.val)
            for i in sounds:
                i.set_volume(volume.val)

    if not tickReset and checkCollision(gb.board, f, (0, 1), 0):
        if not volume.muted:
            pg.mixer.Sound.play(impact_sound)
        landAnimation = Animations.LandAnimation(f, int(1/(tickRate / FPS)))
        tickCount = 1
        tickReset = True

    if game_state == RUNNING:

        if tickCount % (FPS//tickRate) == 0:
            tickReset = False
            if not checkCollision(gb.board, f, (0, 1), 0):
                f.fall()
            else:
                gb.board = drawMatrix
                gb.board, removed_index = row_check(gb.board)
                if len(removed_index) > 0:
                    if not volume.muted:
                        pg.mixer.Sound.play(rem_sound)
                    newSurf = pg.Surface((width, height))
                    newSurf.fill(BG_COLOR)
                    queue.draw(newSurf, width - 90, 0, 90, 200)
                    gb.drawMatrix(newSurf, gb.board)

                    if rowAnimations:
                        Animations.RowAnimation(
                            removed_index, dis, newSurf).play(dis)

                    gb.board = empty_row_removal(gb.board, removed_index)
                    linesCleared += len(removed_index)

                    if len(removed_index) <= 4:
                        score += calcPoints(level, len(removed_index))
                        scoreText = createScoreText(score)
                        if linesCleared >= linesClearedForNewLevel:
                            nextLevel()
                            linesCleared %= linesClearedForNewLevel

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
            if game_state == RUNNING:
                if event.key == pg.K_x:
                    if not rotationCollision(f, True) and not volume.muted:
                        pg.mixer.Sound.play(err_sound)
                if event.key == pg.K_z:
                    if not rotationCollision(f, False) and not volume.muted:
                        pg.mixer.Sound.play(err_sound)

                if event.key == pg.K_LEFT:
                    moveIfPossible(gb.board, f, (-1, 0))
                    lastPressed[0] = time.time()
                if event.key == pg.K_DOWN:
                    moveIfPossible(gb.board, f, (0, 1))
                    lastPressed[1] = time.time()
                if event.key == pg.K_RIGHT:
                    moveIfPossible(gb.board, f, (1, 0))
                    lastPressed[2] = time.time()
            if event.key == pg.K_p:
                if game_state == RUNNING:
                    game_state = PAUSE
                elif game_state == PAUSE:
                    game_state = RUNNING

    pressed = pg.key.get_pressed()
    if game_state == RUNNING:
        t = time.time()
        if tickCount % (FPS//keyCheckRate) == 0:
            if pressed[pg.K_LEFT] and t-lastPressed[0] >= das:
                moveIfPossible(gb.board, f, (-1, 0))

            if pressed[pg.K_RIGHT] and t-lastPressed[2] >= das:
                moveIfPossible(gb.board, f, (1, 0))

            if pressed[pg.K_DOWN] and t-lastPressed[1] >= das:
                moveIfPossible(gb.board, f, (0, 1))

        tickCount += 1

        pg.display.update()
        clock.tick(FPS)
