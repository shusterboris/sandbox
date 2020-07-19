#coding=utf8
import random
import pygame
from appconfig import cfg, Config
from appenviron import AppEnv
from spritetext import SpriteText
from msgmulti import ResultMessage

class Answer(SpriteText):
    answer = ""
    
    def __init__(self, screen, userAnswer, order):
        #call Sprite intializer
        SpriteText.__init__(self)
        self.screen = screen
        self.font = cfg.getFontByType("Answers font")
        #draw text, return surface
        self.answer = userAnswer
        self.showAnswerGood()
        self.id = random.randint(1000,9999)
        self.endPos = (-1, -1)
        self.order = order
        self.badSound = None
        self.mistakeSprite = None
       
    
    def playSoundError(self):
        if not self.badSound:
            sounds = cfg.sounds
            if sounds:
                self.badSound = AppEnv.loadSound(sounds[1])
        if (self.badSound):
            self.badSound.play()
        
    def showAnswerGood(self):
        #initialize title
        self.showText(self.answer, self.font, cfg.getPaletteByType("Answer"))        
        
    def showAnswerBad(self):
        self.showText(self.answer, self.font, cfg.getPaletteByType("Bad answer"))
        self.playSoundError()   
        if not Config.answers.has(self.mistakeSprite):
            self.mistakeSprite = ResultMessage(self.screen, "Неправильно. Выберите другой вариант", (200,200),"chat_bubble_medium_gray.png")
            Config.answers.add(self.mistakeSprite)
            Config.allsprites.add(self.mistakeSprite)

    def processErrorAnswer(self):
        #self.image = pygame.transform.flip(self.image, True, True)
        pygame.sprite.Sprite.kill(self)

    def __repr__(self):
        return "Answer [id]="+str(self.id)+", [start pos]="+str(self.rect.center)+" , [final pos]=" + str(self.endPos)+" "+self.answer
    
    def getStarted(self):
        self._determineEndPosition()
           
    def _determineEndPosition(self):
        rightBottom = self.screen.get_rect()
        vertInterval = rightBottom[3] // 2 // (cfg.numberOfAnswers + 1)
        self.endPos = (rightBottom[2] * (100 - 20) // 100, vertInterval * self.order)
        return self.endPos
            
    def update(self):
        self._determineEndPosition()
        self.rect.center = self.endPos