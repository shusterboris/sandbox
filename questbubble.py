#coding=utf8
import pygame
from actorsreplica import ActorsReplica
from appconfig import cfg


class WordQuestion(ActorsReplica):
    vertAlign = 0.5 #вертикальный отступ - множитель высоты шрифта
    horAlign = 1 #горизонтальный отступ - множитель ширины шрифта

    def __init__(self,screen, prompt, startPos):
        ActorsReplica.__init__(self,screen,startPos,'chat_bubble_small_gray.png')        
        self.screen = screen
        self.prompt = prompt
        self.startPos = startPos
        self.showQuestion()
        self.cfg = cfg      
        
    def showQuestion(self):        
        advFont = self.cfg.fontSettings.fonts.get("Questions font")
        font = advFont.font
        color = self.cfg.fontSettings.palette.get("Answer")
        prompt = self.prompt
        if (advFont.RLE):
            prompt = self.wordReverse(self.prompt)
        textSurf = font.render(prompt, 1, color)
        newSize = self.arrangeImageSize(textSurf, font)
        newImage = pygame.transform.scale(self.image, newSize)
        self.image = newImage
        self.rect = self.image.get_rect()
        horOffset = font.get_height() * 2 * ActorsReplica.horAlign
        vertOffset = font.get_height() * ActorsReplica.vertAlign
        self.image.blit(textSurf, (horOffset, vertOffset))

