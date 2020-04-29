import pygame as pg
fontPath = "../fonts/VCR_OSD_MONO_1.ttf"
volumeImage = pg.image.load("../images/volume.png")

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

class VolumeController:
    def __init__(self,rect,mutePos,muteRad):
        self.x, self.y, self.w, self.h = rect
        self.val = 0.5
        self.valFrom = 0
        self.valTo = 1
        self.mutePos = mutePos
        self.sqrMuteRad = muteRad**2
        self.drawPos = (mutePos[0]-muteRad,mutePos[1]-muteRad)
        self.muted = False
        self.volumeImage = pg.transform.scale(volumeImage,(muteRad*2,muteRad*2))
        self.crossLength = muteRad
        self.crossPositions = [(self.mutePos[0]-self.crossLength/2, self.mutePos[1]-self.crossLength/2),
                               (self.mutePos[0]+self.crossLength/2, self.mutePos[1]+self.crossLength/2),
                               (self.mutePos[0]-self.crossLength/2, self.mutePos[1]+self.crossLength/2),
                               (self.mutePos[0]+self.crossLength/2, self.mutePos[1]-self.crossLength/2)]
        self.crossWidth = 3


    def draw(self,dis):
        pg.draw.rect(dis,(255,255,255),(self.x,self.y,self.w,self.h),2)
        sliderH = (self.val-self.valFrom)/(self.valTo-self.valFrom) * self.h
        pg.draw.rect(dis,(255,255,255),(self.x,self.y+self.h-sliderH,self.w,sliderH))
        dis.blit(self.volumeImage,self.drawPos)

        if self.muted:
            pg.draw.line(dis,(255,0,0),self.crossPositions[0],self.crossPositions[1], self.crossWidth)
            pg.draw.line(dis,(255,0,0),self.crossPositions[2],self.crossPositions[3], self.crossWidth)


    def sliderInside(self,pos):
        x, y = pos
        return x >= self.x and x <= self.x + self.w and y >= self.y and y <= self.y + self.h

    def buttonInside(self,pos):
        return sqrDistance(pos,self.mutePos) <= self.sqrMuteRad

    def update(self):
        p = pg.mouse.get_pos()
        if self.sliderInside(p):
            newVal = (self.y+self.h-p[1]) / self.h
            self.val = newVal
            return True
        return False

    def click(self):
        if self.muted:
            pg.mixer.music.unpause()
        else:
            pg.mixer.music.pause()
        self.muted = not self.muted

def sqrDistance(p1,p2):
    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2