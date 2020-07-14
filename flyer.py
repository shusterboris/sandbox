import pygame
from customsprite import SpriteAdv
import random, math

FPS = 60

class Flyer(SpriteAdv):

    def _inflate(self):
        perc = random.randrange(40,100)/100        
        i=0
        
        for img in self.scins:
            decX = int(perc*img.get_rect().size[0])
            decY = int(perc*img.get_rect().size[1])
            self.images[i].transform.scale(img, (decX, decY))
            i = i + 1

    def __init__(self, screen, skins, position = (80, 700)):
        SpriteAdv.__init__(self, screen, skins)
        transparency = random.randint(50,255)
        super().setSkin(-1, transparency)
        scr = pygame.display.get_surface()
        self.curPos = position        
        self.rect.center = self.curPos
        self.area = scr.get_rect()
        self.screen = screen
        self.id = random.randint(1000,9999)
        self.endPos = (-1, -1)
        
    def __repr__(self):
        return "Flyer [id]="+str(self.id)+", [start pos]="+str(self.rect.center)+" , [final pos]=" + str(self.endPos)+", [skin]: #"+str(self.imageNum)
        
        
    def update(self):
        newpos = self.rect.move(self.xRate, self.yRate)
        self.rect = newpos
        if (newpos[0] > self.screen.get_width()):
            self.kill()
        return newpos
        
    def getStarted(self):
        #Устанавливаем вид, скорость и направление движения        
        #максимальные позиции, с учетом размера экрана
        maxPos = self.screen.get_rect().bottomright
        if self.endPos[0] == -1: #если конечная точка не задана - вычисляем случайно
            #конечное значение точки полета по вертикали - от 60% до 100% экрана
            randomEndX = random.randrange(int(maxPos[0]*0.9), int(maxPos[0]))
            randomEndY = random.randrange(0, int(maxPos[1]*0.4))
            self.endPos = (randomEndX, randomEndY)
        #длительность полета в секундах
        flyDuration = random.randrange(2,4)/2
        #смещение точки старта в случайном порядке на 10% от заданной по умолчанию
        #random offset from starting point
        offset = random.randint(0,self.rect.width * 20 // 100)
        self.curPos = (self.curPos[0]+offset, self.curPos[1]+offset)
        self.rect.center = self.curPos
        
        #дистанция от начальной до конечной точки в пикселях, горизонталь        
        xDistanse = math.fabs(self.endPos[0] - self.curPos[0])
        #дистанция от начальной до конечной точки в пикселях, вертикаль
        yDistanse = math.fabs(self.endPos[1] - self.curPos[1])
        self.xRate = xDistanse / (FPS * flyDuration)
        self.yRate = -1 * yDistanse / (FPS * flyDuration)
        #print("Started:"+repr(self))
    
    def setFinalPosition(self, position):
        if not (position[0] == -1 or position[1] == -1):
            self.endPos = position

