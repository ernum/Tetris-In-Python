import pygame as pg
import time
from .UI import *

FPS = 60
clock = pg.time.Clock()
playAgain = False
fontPath = "../fonts/game_over.ttf"

# Paths
GAMEOVER_SOUND_PATH = pathlib.Path(
    __file__).absolute().parents[1] / "SOUND" / "SoundEffects" / "gameover.wav"

# Sound
gameover_sound = pg.mixer.Sound(str(GAMEOVER_SOUND_PATH))
gameover_sound.set_volume(0.5)


def exit_game():
    raise SystemExit


def play():
    global playAgain
    playAgain = not playAgain


def gameOverAnimation(dis, matrix_merge, landAnimation, gb, f, tickReset, volume):
    """This function will quit if the user chooses exit, return true if the user chooses
    play again or return false if the user chooses title."""
    pg.mixer.Sound.play(gameover_sound)

    w, h = dis.get_rect().size

    gameOverFontSize = 50
    textPositionX = 250
    textPositionY = 70
    textColor = (0, 0, 0)

    buttonWidth = 150
    buttonHeight = 50
    buttonFontSize = 20
    buttonPositionX = 175
    buttonPositionY = 175
    buttonHoverColor = (200, 200, 200)

    volumeIconW = 40
    muteClickRadius = 20

    sliderWidth = 20
    sliderHeight = 60
    sliderMargin = 20
    sliderRect = (w-sliderWidth-sliderMargin, h-sliderHeight -
                  sliderMargin, sliderWidth, sliderHeight)

    tickReset = True
    if landAnimation != None:
        landAnimation.finished = True

    # Text
    game = Text("GAME", textColor,
                gameOverFontSize, (textPositionX, textPositionY))
    over = Text("OVER", textColor,
                gameOverFontSize, (textPositionX, textPositionY + 50))

    # Buttons
    playAgainButton = Button((buttonPositionX, buttonPositionY, buttonWidth, buttonHeight),
                             (255, 255, 255), 0, (100, 100, 100), "PLAY AGAIN", buttonFontSize, (0, 0, 0), play, buttonHoverColor)
    titleButton = Button((buttonPositionX, buttonPositionY + 55, buttonWidth, buttonHeight),
                         (255, 255, 255), 0, (100, 100, 100), "TITLE", buttonFontSize, (0, 0, 0), None, buttonHoverColor)
    exitButton = Button((buttonPositionX, buttonPositionY + 110, buttonWidth, buttonHeight),
                        (255, 255, 255), 0, (100, 100, 100), "EXIT", buttonFontSize, (0, 0, 0), exit_game, buttonHoverColor)

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
                if titleButton.isInside(p):
                    return False
                if exitButton.isInside(p):
                    exitButton.click()

                if volume.buttonInside(p):
                    volume.click()

        if playAgainButton.isInside(pg.mouse.get_pos()):
            playAgainButton.hover()
        else:
            playAgainButton.noHover()

        if titleButton.isInside(pg.mouse.get_pos()):
            titleButton.hover()
        else:
            titleButton.noHover()

        if exitButton.isInside(pg.mouse.get_pos()):
            exitButton.hover()
        else:
            exitButton.noHover()

        if pg.mouse.get_pressed()[0]:
            if volume.update():
                pg.mixer.music.set_volume(volume.val)

        game.draw(dis)
        over.draw(dis)
        playAgainButton.draw(dis)
        exitButton.draw(dis)
        titleButton.draw(dis)
        volume.draw(dis)

        pg.display.update()

        clock.tick(FPS)

    play()
    return True
