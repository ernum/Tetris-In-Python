import time

import pygame as pg
from random import randint as ri

fontPath = "../fonts/VCR_OSD_MONO_1.ttf"

white = (255, 255, 255)
black = (0, 0, 0)
yellow = (250, 250, 0)
turq = (20, 250, 250)
green = (0, 255, 0)
red = (255, 0, 0)
orange = (255, 150, 20)
blue = (0, 0, 255)
pink = (200, 20, 250)
colors = [black, yellow, turq, green, red, orange, blue, pink, white]
t = time.time()
# do stuff
elapsed = time.time() - t

class Button:
    def __init__(self,rect,color,outlineWidth,outlineColor,text,textSize,textColor,onClickFunction,hoverColor):
        self.color = color
        self.currentColor = color
        self.hoverColor = hoverColor
        self.outlineWidth = outlineWidth
        self.outlineColor = outlineColor
        self.x, self.y, self.w, self.h = rect
        self.onClickFunction = onClickFunction
        self.text = text
        self.textSize = textSize
        self.textColor = textColor


    def isInside(self,pos):
        x, y = pos
        return x >= self.x and x <= self.x + self.w and y >= self.y and y <= self.y + self.h

    def click(self):
        self.onClickFunction()

    def hover(self):
        self.currentColor = self.hoverColor

    def noHover(self):
        self.currentColor = self.color

    def draw(self,dis):
        pg.draw.rect(dis,self.outlineColor,(self.x,self.y,self.w,self.h))
        pg.draw.rect(dis, self.currentColor, (self.x + self.outlineWidth, self.y + self.outlineWidth, self.w - 2*self.outlineWidth, self.h - 2*self.outlineWidth))
        font = pg.font.Font(fontPath,self.textSize)
        rend = font.render(self.text,True,self.textColor)
        textSize = rend.get_rect().size
        dis.blit(rend,(self.x + self.w/2 - textSize[0]/2,self.y + self.h/2 - textSize[1]/2))


class Text:
    def __init__(self,text,color,size,center):
        self.text = text
        self.color = color
        self.size = size
        self.font = pg.font.Font(fontPath,size)
        self.rend = self.font.render(text,True, color)
        self.center = center
        self.textSize = self.rend.get_rect().size
        self.pos = (self.center[0] - self.textSize[0]/2, self.center[1]-self.textSize[1]/2)

    def recalcPos(self):
        self.pos = (self.center[0] - self.textSize[0]/2, self.center[1]-self.textSize[1]/2)

    def draw(self, dis):
        self.rend = self.font.render("TETRIS", True, self.color)
        dis.blit(self.rend,self.pos)

def exit():
    raise SystemExit

def start():
    global started
    started = True

started = False


def titlePage(dis):
    pg.display.set_caption("TETRIS")
    icon = pg.image.load("../images/tetrisIcon2.png")
    pg.display.set_icon(icon)

    w,h = dis.get_rect().size
    titleFontSize = 100
    titleStartY = -titleFontSize
    titleDropSpeed = 1

    buttonWidth = 100
    buttonHeight = 50
    buttonFontSize = 30

    buttonHoverColor = (200,200,200)

    titleEndY = (h-buttonHeight)/2 - buttonHeight*1.5 - titleFontSize/2
    title = Text("TETRIS",(255, 255, 255),titleFontSize,(w/2,titleStartY))

    startButton = Button(((w-buttonWidth)/2-buttonWidth*0.6,(h-buttonHeight)/2, buttonWidth, buttonHeight),(255,255,255),0,(100,100,100),"START",buttonFontSize,(0,0,0),start,buttonHoverColor)
    exitButton = Button(((w-buttonWidth)/2+buttonWidth*0.6,(h-buttonHeight)/2, buttonWidth, buttonHeight),(255,255,255),0,(100,100,100),"EXIT",buttonFontSize,(0,0,0),exit, buttonHoverColor)


    clock = pg.time.Clock()
    t = time.time()

    colorIndex = 0

    while not started:
        dis.fill((0,0,0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                raise SystemExit

            if event.type == pg.MOUSEBUTTONUP:
                if startButton.isInside(pg.mouse.get_pos()):
                    startButton.click()
                if exitButton.isInside(pg.mouse.get_pos()):
                    exitButton.click()

        if startButton.isInside(pg.mouse.get_pos()):
            startButton.hover()
        else:
            startButton.noHover()

        if exitButton.isInside(pg.mouse.get_pos()):
            exitButton.hover()
        else:
            exitButton.noHover()

        if time.time() - t > 0.2:
            rand = ri(1, len(colors) - 2)
            while colorIndex == rand:
                rand = ri(1, len(colors) - 2)
            colorIndex = rand
            title.color = colors[colorIndex]
            t = time.time()

        # Title drop animation
        titleY = title.pos[1]
        if titleY < titleEndY:
            titleDropSpeed += 0.5
            title.pos = (title.pos[0], title.pos[1] + titleDropSpeed)
        if titleY > titleEndY and titleDropSpeed != 0:
            if titleDropSpeed > 0:
                titleDropSpeed *= -1
            titleDropSpeed += 3
            title.pos = (title.pos[0], title.pos[1] + titleDropSpeed)
        if titleY > titleEndY + 3:
            titleDropSpeed = 0
            title.pos = (title.pos[0], title.pos[1] + titleDropSpeed)
            
        startButton.draw(dis)
        exitButton.draw(dis)
        title.draw(dis)

        pg.display.update()

        clock.tick(60)

