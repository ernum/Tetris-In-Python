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

class Slider:
    def __init__(self,rect,vertical, valFrom, valTo, valStart):
        self.x, self.y, self.w, self.h = rect
        self.vertical = vertical
        self.val = valStart
        self.valFrom = valFrom
        self.valTo = valTo

    def draw(self,dis):
        if self.vertical:
            pg.draw.rect(dis,(255,255,255),(self.x,self.y,self.w,self.h),2)
            sliderH = (self.val-self.valFrom)/(self.valTo-self.valFrom) * self.h
            pg.draw.rect(dis,(255,255,255),(self.x,self.y+self.h-sliderH,self.w,sliderH))
        else:
            pg.draw.rect(dis,(255,255,255),(self.x,self.y,self.w,self.h),2)
            sliderW = (self.val-self.valFrom)/(self.valTo-self.valFrom) * self.w
            pg.draw.rect(dis,(255,255,255),(self.x,self.y,sliderW,self.h))

    def isInside(self,pos):
        x, y = pos
        return x >= self.x and x <= self.x + self.w and y >= self.y and y <= self.y + self.h

    def update(self):
        p = pg.mouse.get_pos()
        if self.isInside(p):
            if self.vertical:
                newVal = (self.y+self.h-p[1]) / self.h
                self.val = newVal
            else:
                newVal = (p[0]-(self.x)) / self.w
                self.val = newVal
            return True
        return False

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

def sqrDistance(p1,p2):
    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2

def titlePage(dis):
    pg.display.set_caption("TETRIS")
    icon = pg.image.load("../images/tetrisIcon2.png")
    volumeImage = pg.image.load("../images/volume.png")

    pg.display.set_icon(icon)

    w,h = dis.get_rect().size
    titleFontSize = 100
    titleStartY = -titleFontSize
    titleDropSpeed = 1

    buttonWidth = 100
    buttonHeight = 50
    buttonFontSize = 30

    sliderWidth = 20
    sliderHeight = 60
    sliderMargin = 20
    sliderRect = (w-sliderWidth-sliderMargin,h-sliderHeight-sliderMargin,sliderWidth,sliderHeight)

    volumeIconW = 40
    volumeIconPos = (sliderRect[0]-volumeIconW-10,sliderRect[1] + sliderRect[3]//2 - volumeIconW//2)
    crossWidth = 5
    crossLength = volumeIconW/2

    muted = False
    muteClickRadius = volumeIconW/2
    sqrMuteClickRadius = muteClickRadius**2

    volumeSlider = Slider(sliderRect,True,0,1,0.5)
    volumeImage = pg.transform.scale(volumeImage,(volumeIconW,volumeIconW))

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

            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                if startButton.isInside(pg.mouse.get_pos()):
                    startButton.click()
                if exitButton.isInside(pg.mouse.get_pos()):
                    exitButton.click()

                if sqrDistance(pg.mouse.get_pos(),[i + volumeIconW/2 for i in volumeIconPos]) <= sqrMuteClickRadius:
                    if muted:
                        pg.mixer.music.unpause()
                    else:
                        pg.mixer.music.pause()
                    muted = not muted

        if startButton.isInside(pg.mouse.get_pos()):
            startButton.hover()
        else:
            startButton.noHover()

        if exitButton.isInside(pg.mouse.get_pos()):
            exitButton.hover()
        else:
            exitButton.noHover()

        if pg.mouse.get_pressed()[0]:
            if volumeSlider.update():
                pg.mixer.music.set_volume(volumeSlider.val)

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
        volumeSlider.draw(dis)
        dis.blit(volumeImage,volumeIconPos)

        if muted:
            pg.draw.line(dis,(255,0,0),[i + (volumeIconW-crossLength)/2 for i in volumeIconPos],[i + crossLength + (volumeIconW-crossLength)/2 for i in volumeIconPos],crossWidth)
            pg.draw.line(dis,(255,0,0),(volumeIconPos[0]+crossLength + (volumeIconW-crossLength)/2,volumeIconPos[1] + (volumeIconW-crossLength)/2),(volumeIconPos[0] + (volumeIconW-crossLength)/2,volumeIconPos[1] + crossLength + (volumeIconW-crossLength)/2),crossWidth)


        pg.display.update()

        clock.tick(60)

