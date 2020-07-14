#coding=utf8
import os
import pygame
from pygame.compat import geterror

class AppEnv:
    @staticmethod
    def getMainDir():
        return os.path.split(os.path.abspath(__file__))[0]

    @staticmethod
    def getDataDir():
        return os.path.join(AppEnv.getMainDir(), "data")

    @staticmethod
    def getDictDir():
        return os.path.join(AppEnv.getDataDir(), "dictionaries")    
    
    @staticmethod
    def getUserProfile():
        return os.environ['USERPROFILE']
    
    @staticmethod
    def loadImage(fileName, colorkey=None):
        fullname = os.path.join(AppEnv.getDataDir(), fileName)
        try:
            image = pygame.image.load(fullname)
        except pygame.error:
            print ('Невозможно загрузить изображение:', fullname, ", ",str(geterror()))
            return None
        image = image.convert()
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    
    @staticmethod
    def loadSound(name):
        class NoneSound:
            def play(self): pass
        if not pygame.mixer or not pygame.mixer.get_init():
            pygame.mixer.init()
        if not pygame.mixer or not pygame.mixer.get_init():            
            return NoneSound()
        fullname = os.path.join(AppEnv.getDataDir(), name)
        try:
            sound = pygame.mixer.Sound(fullname)
        except pygame.error:
            print ('Невозможно загрузить звук: %s' % fullname)
        return sound
    
    @staticmethod
    def loadIcon(fileName):
        return AppEnv.loadImage(fileName, -1)
