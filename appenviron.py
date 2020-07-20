#coding=utf8
import os, sys
import pygame

class AppEnv:
    soundsDir = ""
    imagesDir = ""
    
    @staticmethod
    def getMainDir():
        if hasattr(sys, '_MEIPASS' ):
            return os.path.dirname(sys.executable)
        else:
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
    def getDictImageDir():
        if AppEnv.imagesDir == "":
            return os.path.join(AppEnv.getDictDir(),"images")
        else:
            return AppEnv.imagesDir

    @staticmethod
    def getDictSoundDir():
        if AppEnv.soundsDir == "":
            return os.path.join(AppEnv.getDictDir(),"sounds")
        else:
            return AppEnv.soundsDir

    
    @staticmethod
    def loadImage(fileName, colorkey=None):
        fullname = os.path.join(AppEnv.getDataDir(), fileName)
        try:
            if (os.path.exists(fullname)):
                image = pygame.image.load(fullname)
            else:
                fullname = os.path.join(AppEnv.getDictImageDir(),fileName)
                if os.path.exists(fullname): 
                    image = pygame.image.load(fullname)
                else:
                    raise pygame.error
        except pygame.error:
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
            return None
        return sound

    @staticmethod
    def loadCustomSound(name):
        class NoneSound:
            def play(self): pass
        if not pygame.mixer or not pygame.mixer.get_init():
            pygame.mixer.init()
        if not pygame.mixer or not pygame.mixer.get_init():            
            return NoneSound()
        fullname = os.path.join(AppEnv.getDictSoundDir(), name)
        try:
            sound = pygame.mixer.Sound(fullname)
        except pygame.error:
            return None
        return sound

    
    @staticmethod
    def loadIcon(fileName):
        return AppEnv.loadImage(fileName, -1)
