#coding=utf8
import random
import pygame
from appenviron import AppEnv
from appconfig import cfg

#implements standarsds functionality of sprite plus load skins from file
class SpriteAdv(pygame.sprite.Sprite):
    skins = [];
    #load all images
    def loadImages(self,fileNames):
        images = []
        for fileName in fileNames:
            image = AppEnv.loadImage(fileName, -1)
            images.append(image)
        return images

    def loadSound(self,name):
        return AppEnv.loadSound(name)

    #choose one skin from loaded files, parameter skin is number of
    #file from list. If once the one is getting, if more - it's getting by No
    #if No greater then total - it's getting last one, if less then 0 - rendom
    #None (default, i.e parameter absent) - first one
    def setSkin(self, skin = None, transparency = None):
        if len(self.skins) == 0:
            font = pygame.font.Font(None, 36)            
            title = font.render(self.answer, 1, (10, 10, 10))
            self.image = title
        elif len(self.skins) == 1:
            self.image = self.images[0]
            self.imageNum = 0
        else:
            if skin == None:
                self.image = self.images[0]
                self.imageNum = 0                
            elif not skin < 0:
                if (skin > len(self.skins) - 1):
                    skin = len(self.skins) - 1
                self.image = self.images[skin]
            else:
                self.imageNum = random.randrange(0,len(self.images)-1)
                self.image = self.images[self.imageNum]
        if not transparency == None:
            if (transparency < 0):
                transparency = 0
            if (transparency > 255):
                transparency = 255
            self.image.set_alpha(transparency)
            
    def _parseSkins(self, src):
        if not src.find(":") != -1:
            return src
        else:
            parts = src.split(":")
            return self.cfg.getSpriteSkins(parts[0], parts[1])

    def wordReverse(self, src):
        #reverse order of letters in the src (RLE)
        lst = list(src) 
        lst.reverse()
        s = ""  
        for letter in lst:  
            s += letter
        return s

    def __init__(self, screen, skinsFileNames):
        pygame.sprite.Sprite.__init__(self)
        self.cfg = cfg
        skinsFileNames = self._parseSkins(skinsFileNames) 
        fileNames = skinsFileNames.split(',')
        self.skins = fileNames
        self.images = self.loadImages(fileNames)
        self.setSkin(0)
        self.screen = screen
        self.rect = self.image.get_rect()         
        self.rect.bottomright = self.screen.get_rect().bottomright