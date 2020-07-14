#coding=utf8
from customsprite import SpriteAdv
from appconfig import cfg


class ActorsReplica(SpriteAdv):
    vertAlign = 1 #вертикальный отступ - множитель высоты шрифта
    horAlign = 1 #горизонтальный отступ - множитель ширины шрифта

    def __init__(self,screen, prompt, startPos, nameOfSkin = 'chat_bubble_sq_mid.png'):
        SpriteAdv.__init__(self,screen, nameOfSkin)        
        self.screen = screen
        self.prompt = prompt
        self.startPos = startPos
        self.cfg = cfg
       
        
    def update(self):
        self.rect.bottomleft = self.startPos
        
    def centerTextPos(self, textSurf, lineNo = 1, lineNumbers = 1):
        spriteRect = self.image.get_rect()
        textRect = textSurf.get_rect()
        textWidth = textRect[2]
        textHeight = textRect[3]
        y = spriteRect.centery + textHeight // 2
        x = spriteRect.centerx - textWidth // 2
        return (x, y)
                                  
    def arrangeImageSize(self, textSurf, font):
        # высота реплики это: высота шрифта, отступы сверху и снизу и высота хвостика, примерно равная половине высоты шрифта
        vert_size = font.get_height() * (1.5 + ActorsReplica.vertAlign*2)
        # ширина реплики - это ширина текста плюч двойная ширина буквы с каждой стороны
        textWidth = textSurf.get_rect()[2]
        hor_size = textWidth + 2 * ActorsReplica.horAlign * 2 * font.get_height()
        return (int(hor_size), int(vert_size))
          
