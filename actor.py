#coding=utf8
from enum import Enum
import pygame
from appenviron import AppEnv
from appconfig import cfg, Config
from customsprite import SpriteAdv
from flyer import Flyer
from answers import Answer
from questbubble import WordQuestion
from msgmulti import ResultMessage
from servicebuttons import SoundBtn
from imagetip import ImageTip
import dictionaries


class ActorsStatus(Enum):
    Ready = 0
    CastingFlyers = 1
    WaitingForAnswer = 2 


class Actor(SpriteAdv):
    def __init__(self,screen):
        SpriteAdv.__init__(self,screen,"Actor:wizard-a.png")
        self.state = ActorsStatus.Ready 
        self.screen = screen
        self.dic = dictionaries.Dictionaries()        
        self.answered = {}
        self.successed = 0
        self.failed = 0
        self.msg = None
        x = 20
        y = self.screen.get_rect()[3] - x
        self.startPos = (x, y)
        color = self.cfg.fontSettings.palette.get("Interface")
        fontView = self.cfg.getFontByType("Interface font")
        self.result = ResultStr(fontView.font, color, self.screen.get_rect().midbottom)
        self.status = self.dic.loadDict()        
        
        
    def update(self):
        self.rect.bottomleft = self.startPos
        
    def createQuestion(self, deepOfRecursion = 0):
        word = self.dic.getRandomWord()
        question = self.dic.createWordQuestion(word)
        #проверяем, а нет ли в существующих
        existing = self.answered.get(question.word)
        key = question.word
        if not existing:
            self.answered.update({key : question})
            return question;
        elif existing.state < 0:
            self.answered[key] = question
        else:
            if (deepOfRecursion < 5):
                deepOfRecursion += 1
                return self.createQuestion(deepOfRecursion)
        return question
        
    def cast(self):
        #Колдуем: бросаем кучу шариков, если он уже закончил предыдущий цикл бросания флаеров и ожидания ответа
        if (self.state != ActorsStatus.Ready):
            return
        self.state = ActorsStatus.CastingFlyers
        i = 1
        flyers = []
        skins = 'Flyer:ball-a.png,ball-b.png,ball-c.png,ball-d.png,ball-e.png'        
        x = self.startPos[0] + self.image.get_rect().bottomright[0]
        y = self.startPos[1] - self.image.get_rect().height * 3 // 4
        flyersStartPos = (x, y)
        #если еще не добавляли строку статуса - добавим
        if (not (Config.allsprites.has(self.result))):
            Config.allsprites.add(self.result)
        if (Config.allsprites.has(self.msg)):
            Config.allsprites.remove(self.msg)            
        while not (i == cfg.numberOfFlyers):
            flyer = Flyer(self.screen, skins, flyersStartPos)
            flyer.getStarted()
            i = i + 1
            Config.allsprites.add(flyer)
            
        return flyers

    def castAnswers(self):
        if self.state != ActorsStatus.CastingFlyers: 
            return         
        #всего спрайтов на экране, включая флаеры, актора и ответы
        totalSprites = len(Config.allsprites.sprites())
        #выводим варианты ответов, njkmrj когда на экране осталось флаеров меньше, чем вариантов ответа
        if totalSprites > (cfg.numberOfAnswers + 2) or totalSprites == 1: 
            return
        #at first, clear all the answers (question included)
        self.questionAccepted()        
        # сначала вопрос....        
        self.state = ActorsStatus.WaitingForAnswer
        self.question = self.createQuestion()
        quest = WordQuestion(self.screen, self.question.word, self.rect.midtop)
        Config.answers.add(quest)
        # проверим звуки
        if self.question.soundPath:
            buttonSpr = SoundBtn(self.screen, "2notes.png", self.question.soundPath)
            Config.answers.add(buttonSpr)
        # потом ответы
        i = 1
        for translate in self.question.answers:
            Config.answers.add(Answer(self.screen,translate,i))
            i += 1
        Config.answers.update()
        Config.allsprites.add(Config.answers.sprites())
            
    
    def checkUserAnswer(self, mousePos):
        spriteAnswer = self.onAnswerClicked(mousePos)
        if spriteAnswer == None: 
            return
        key = self.question.word
        translate = spriteAnswer.answer
        if translate == self.question.trnslt:
            #если ответ на котором щелкнули, правильный (соответствует переводу)
            if (cfg.sounds):
                soundGood = AppEnv.loadSound(cfg.sounds[0])
                if soundGood:
                    soundGood.play()
            self.questionAccepted()
            if self.question.state == 0:
                #если статус вопроса "новый" - т.е. до этого не было неправильных ответов, увеличим счетчик успешных
                self.answered[key].state = self.question.state 
                self.successed, self.failed = self.question.changeState(True, self.successed, self.failed)
            self.showResult(self.question.state == 1)
            self.state = ActorsStatus.Ready      
        else:
            #ответ неправильный, изменяем вид надписи...
            spriteAnswer.showAnswerBad()
            spriteAnswer.update()
            self.answered[key].state = self.question.state
            self.successed, self.failed = self.question.changeState(False, self.successed, self.failed)            
        self.result.changeState(self.successed, self.failed)  
    
    def showImageTip(self):
        if (self.question.imgPath):
            imageTip = ImageTip(self.screen, self.question.imgPath, (0, 0), 10)
            imageTip.setAppearance(5, 255)
            imageTip.rect.topleft = self.screen.get_rect().topleft
            Config.answers.add(imageTip)
            Config.allsprites.add(imageTip)
    
    def onAnswerClicked(self, mousePos, group = Config.answers):
        pointer = MousePointer(mousePos)
        spriteAnswer = pygame.sprite.spritecollideany(pointer, group)
        className = type(spriteAnswer).__name__
        if className == "Answer":
            return spriteAnswer
        elif className == "NoneType":
            if (group != Config.allsprites):
                self.onAnswerClicked(mousePos, Config.allsprites)
            return 
        elif className == "MsgMulti":
            spriteAnswer.kill()
            return 
        elif className == "SoundBtn":
            #TODO сделать звук, здесь же как в Скрече - графические кнопки: загрузить звук,  рисунок, записать звук
            if AppEnv.loadCustomSound(spriteAnswer.soundPath).play() == None:
                Config.appLog.warning("Невозможно загрузить звуковую подсказку "+spriteAnswer.soundPath)
            return None
        elif className == "Actor":
            if self.state == ActorsStatus.WaitingForAnswer:
                self.showImageTip()
            return None
        else:
            return None
        
        
    def questionAccepted(self):
        Config.allsprites.remove(Config.answers.sprites())
        Config.answers.empty()
    
    def showResult(self, isSuccess=True):
        text = "Клавиша <Пробел> - продолжение, <ESC> - выход"
        if (isSuccess):
            self.showMessage("ПРАВИЛЬНО! "+text, None)
        else:
            self.showMessage("Теперь правильно. "+text, None)
    
    def showMessage(self, text, pos = None):
        if (self.msg != None):
            Config.allsprites.remove(self.msg)
        if pos == None:
            pos = self.rect.topright
        self.msg = ResultMessage(self.screen, text, pos, "chat_bubble_medium_gray.png")
        Config.allsprites.add(self.msg)
        Config.allsprites.update()
        

class MousePointer(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(position, (1, 1))

class ResultStr(pygame.sprite.Sprite):
    def __init__(self, font, color, pos):
        pygame.sprite.Sprite.__init__(self)
        self.position = pos
        self.font = font
        self.successed = 0 
        self.failed = 0
        self.color = color
        
    def changeState(self, succesed, failed):
        self.successed = succesed 
        self.failed = failed
        self.update()

        
    def getPlayState(self):
        return "Количество ответов: правильных - {} неправильных - {}".format(self.successed, self.failed)
        
    
    def update(self):
        label = self.font.render(self.getPlayState(), 1, self.color)
        self.image = label
        self.rect = label.get_rect()
        self.rect.midbottom = self.position