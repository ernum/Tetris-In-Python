import pygame as pg
import pygameTitleScreen
import time
from UI import *
import Animations

FPS = 60
clock = pg.time.Clock()
playAgain = False


def exit_game():
    raise SystemExit


def play():
    global playAgain
    playAgain = not playAgain


def titleScreen():
    pass


def gameOverAnimation(dis, matrix_merge, landAnimation, gb, f, tickReset):
    fontPath = "../fonts/game_over.ttf"

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

    tickReset = True
    if landAnimation != None:
        landAnimation.finished = True

    game = Text("GAME", textColor,
                gameOverFontSize, (textPositionX, textPositionY))
    over = Text("OVER", textColor,
                gameOverFontSize, (textPositionX, textPositionY + 50))
    playAgainButton = Button((buttonPositionX, buttonPositionY, buttonWidth, buttonHeight),
                             (255, 255, 255), 0, (100, 100, 100), "PLAY AGAIN", buttonFontSize, (0, 0, 0), play, buttonHoverColor)
    titleButton = Button((buttonPositionX, buttonPositionY + 55, buttonWidth, buttonHeight),
                         (255, 255, 255), 0, (100, 100, 100), "TITLE", buttonFontSize, (0, 0, 0), titleScreen, buttonHoverColor)
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
                if exitButton.isInside(p):
                    exitButton.click()

            if playAgainButton.isInside(pg.mouse.get_pos()):
                playAgainButton.hover()
            else:
                playAgainButton.noHover()

            if exitButton.isInside(pg.mouse.get_pos()):
                exitButton.hover()
            else:
                exitButton.noHover()

        game.draw(dis)
        over.draw(dis)
        playAgainButton.draw(dis)
        exitButton.draw(dis)
        titleButton.draw(dis)

        pg.display.update()

        clock.tick(FPS)
    play()
