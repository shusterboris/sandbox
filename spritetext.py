import pygame
class SpriteText(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def showText(self, text, advFont, color):
        if advFont.RLE:
            text = self.wordReverse(text)
        title = advFont.font.render(self.answer, 1, color)
        self.image = title
        self.rect = title.get_rect()
            
    def wordReverse(self, src):
        #reverse order of letters in the src (RLE)
        lst = list(src) 
        lst.reverse()
        s = ""  
        for letter in lst:  
            s += letter
        return s
