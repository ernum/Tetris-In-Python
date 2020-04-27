import pygame as pg

fontPath = "../fonts/VCR_OSD_MONO_1.ttf"

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
        self.rend = self.font.render(text,True,color)
        self.center = center
        self.textSize = self.rend.get_rect().size
        self.pos = (self.center[0] - self.textSize[0]/2, self.center[1]-self.textSize[1]/2)

    def recalcPos(self):
        self.pos = (self.center[0] - self.textSize[0]/2, self.center[1]-self.textSize[1]/2)

    def draw(self,dis):
        dis.blit(self.rend,self.pos)

def exit():
    raise SystemExit

def start():
    global started
    started = True

started = False

def titlePage(dis):
    w,h = dis.get_rect().size
    titleFontSize = 100
    titleStartY = -titleFontSize
    titleDropSpeed = 5

    buttonWidth = 100
    buttonHeight = 50
    buttonFontSize = 30

    buttonHoverColor = (200,200,200)

    titleEndY = (h-buttonHeight)/2 - buttonHeight*1.5 - titleFontSize/2
    title = Text("TETRIS",(255,255,255),titleFontSize,(w/2,titleStartY))

    startButton = Button(((w-buttonWidth)/2-buttonWidth*0.6,(h-buttonHeight)/2, buttonWidth, buttonHeight),(255,255,255),0,(100,100,100),"START",buttonFontSize,(0,0,0),start,buttonHoverColor)
    exitButton = Button(((w-buttonWidth)/2+buttonWidth*0.6,(h-buttonHeight)/2, buttonWidth, buttonHeight),(255,255,255),0,(100,100,100),"EXIT",buttonFontSize,(0,0,0),exit, buttonHoverColor)


    clock = pg.time.Clock()

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


        titleY = title.pos[1]
        if titleY < titleEndY:
            title.pos = (title.pos[0],title.pos[1]+titleDropSpeed)

        startButton.draw(dis)
        exitButton.draw(dis)
        title.draw(dis)

        pg.display.update()

        clock.tick(60)

