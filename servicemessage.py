#coding=utf8
import pygame
from actorsreplica import ActorsReplica

class ServiceMessage(ActorsReplica):

    def __init__(self,screen, prompt, startPos):
        ActorsReplica.__init__(self,screen, prompt, startPos, 'chat_bubble_sq_navi.png')
        self.prompt = prompt
        self.startPos = startPos               
        self.showMessage()
                
    def showMessage(self):        
        advFont = self.cfg.fontSettings.fonts.get("Interface font")
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

