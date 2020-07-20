#coding=utf8
import sys
import pygame            
from actor import Actor
from appconfig import cfg, Config, logger
from appenviron import AppEnv
from msgmulti import MsgMulti

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')


def main():
    #Initialize Everything
    logger.info("Запуск программы")
    pygame.init()    
    #it's surface
    mode = cfg.screenResolution
    screen = pygame.display.set_mode(mode)
    pygame.display.set_caption(" ")
    icon = AppEnv.loadImage("hatul_gold.png", -1)
    pygame.display.set_icon(icon)
    pygame.mouse.set_visible(1)
    
#Create The Backgound - now white surface
    logger.info("Загрузка фона")
    background = cfg.loadBackground(screen)

#Display The Background
    screen.fill([255,255,255])
    screen.blit(background, (0, 0))
    pygame.display.flip()

#Prepare Game Objects
    clock = pygame.time.Clock()
    try:
        #who casts new word's choice
        initialized = True
        actor = Actor(screen)
        logger.info("Актор инициализирован")
        actor.setAppearance(5, 255)
        Config.allsprites.add(actor, actor.result)
        initalMsgPos = screen.get_rect().midtop
        if actor.status != "":
            initialized = False
            msg = MsgMulti(screen, actor.status + ". Нажмите <ESC> - для выхода", initalMsgPos, 'board.png')
        else:
            msg = MsgMulti(screen, "Нажмите клавишу <Пробел> для запуска, <ESC> - для выхода. Щелкните мышкой по этой надписи, чтобы начать", initalMsgPos, 'board.png')
        Config.allsprites.add(actor, msg)
        
            
    #Main Loop
        going = True
        while going:
            clock.tick(cfg.FPS)
    
            #Handle Input Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    going = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    going = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if (Config.allsprites.has(msg)):
                        msg.kill()
                    if initialized:
                        actor.cast()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    actor.checkUserAnswer(pygame.mouse.get_pos())
    
            actor.castAnswers()
            Config.allsprites.update()
            #Draw Everything
            screen.fill([255,255,255])
            screen.blit(background, (0, 0))
            Config.allsprites.draw(screen)
            pygame.display.flip()
    except:
        logger.fatal(str(sys.exc_info()))
    else:
        pass #close all here
    pygame.quit()

#Game Over

#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
