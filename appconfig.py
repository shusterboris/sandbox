#coding=utf8
import os, sys
import configparser
import pygame

from appenviron import AppEnv

parser = configparser.ConfigParser()


def readStrKeyValue(sectName,keyName):
    key = None
    try:
        key = parser[sectName][keyName]
    except KeyError as err:
        print("Ошибка при чтении ключа{1} ini-файла: {0}".format(keyName,err))
    return key

def readIntKeyValue(sectName,keyName):
    key = None
    try:
        keyStr = readStrKeyValue(sectName,keyName)
        key = int(keyStr)
    except:
        print("Ошибка при чтении ключа{1} ini-файла: {0}".format(keyName,sys.exc_info()[0]))
    return key
            
#should return position as (x,y) from string with format nnn,nnn
def readPosKeyValue(sectName,keyName):
    key = None
    try:
        keyStr = readStrKeyValue(sectName,keyName)
        if not keyStr: return key;
        coords = keyStr.split(",")
        if not len(coords) == 2:
            Exception("неправильный формат. Ключ должен иметь вид - число, число")
        x = coords[0].strip()
        y = coords[1].strip()
        if not (x.isdigit() and x.isdigit()):
            Exception("как минимум, одно из значений не является числом")
        key = (int(x), int(y))
    except:
        print("Ошибка при чтении ключа{1} ini-файла: {0}".format(keyName,sys.exc_info()[0]))
    return key

#should return position as (x,y) from string with format nnn,nnn
def readRGBKeyValue(sectName,keyName):
    key = None
    try:
        keyStr = readStrKeyValue(sectName,keyName)
        if not keyStr: return key;
        coords = keyStr.split(",")
        if not len(coords) == 2:
            Exception("неправильный формат. Ключ должен иметь вид - число, число")
        r = coords[0].strip()
        g = coords[1].strip()
        b = coords[2].strip()
        if not (r.isdigit() and g.isdigit() and b.isdigit()):
            Exception("как минимум, одно из значений не является числом")
        key = (int(r), int(g), int(b))
    except:
        print("Ошибка при чтении ключа{1} ini-файла: {0}".format(keyName,sys.exc_info()[0]))
    return key


#здесь хранятся общие настройки программы и пользователя
class Config:
    screenResolution = (800, 600);
    allSpritesGrp = None
    fontSize = 36
    #имя файлов и папок словаря, данных, изображений
    dictDefaultFileName = "dictionary.dic"
    dictFileName = ""
    wordsDelimiter = ":"
    straightDictDir = True
    hasRLE = False
    #количество предлагаемых ответов
    numberOfAnswers = 4
    numberOfFlyers = 5
    flyersSpeed = (1, 4)
    #frame per second, freqency of screen's updating
    FPS = 30
    #groups
    answers = pygame.sprite.Group()
    flyers = pygame.sprite.Group()
    allsprites = pygame.sprite.Group()
        
    def __init__(self):
        try:
            mainDir = AppEnv.getMainDir()
            iniFile = os.path.join(mainDir,"app.ini")
            parser.read(iniFile, encoding='utf-8')
            value = readPosKeyValue('Settings','Screen resolution')
            if value:
                self.screenResolution = value
            intValue = readIntKeyValue('Settings','FPS')
            if intValue:
                self.fps = intValue
            intValue = readIntKeyValue('Settings','Number of answers')
            if intValue:
                self.numberOfAnswers = intValue
            intValue = readIntKeyValue('Settings','Number of flyers')
            if intValue:
                self.numberOfFlyers = intValue
            intValue = readIntKeyValue('Fonts','Questions font size')
            if intValue:
                self.fontSize = intValue
            value = readPosKeyValue('Settings','Flyers speed')
            if value:
                self.flyersSpeed = value
            strValue = readStrKeyValue('Settings','Words delimiter')
            if strValue:
                self.wordsDelimiter = strValue 
            strValue = readStrKeyValue('Dictionaries','Direction')
            if strValue:
                self.straightDictDir = (strValue.upper() != 'BACKWARD')
            strValue = readStrKeyValue('Dictionaries','Default dictionary name')
            if strValue:
                self.dictDefaultFileName = strValue
            strValue = readStrKeyValue('Dictionaries','User dictionary name')
            if strValue:
                self.dictFileName = strValue
            if (not self.dictFileName):
                self.dictFileName = self.dictDefaultFileName
            if (not self.dictFileName):
                Exception("Не указан файл словаря")
            pygame.font.init()
            self.fontSettings = FontSettings()
            self.fontSettings.loadFontSettings(AppEnv.getDataDir())
            #if we are changed word and translate - change fonts
            if not self.straightDictDir:
                self.fontSettings.switchFonts()
            self.sounds = self.loadSounds()                       
            if (not self.fontSettings.loadingStatus):
                Exception("Не загружены один или более шрифтов")            
        except:
            print("Работа невозможна из-за ошибок в настройках: %s"%str(sys.exc_info()))

    def _loadPlainBackground(self, screen):
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill((250, 250, 250))
        return background
    
    def loadBackground(self, screen):
        try:
            bckgrFileName = readStrKeyValue('Skins','Background')
            if bckgrFileName:
                background = AppEnv.loadImage(bckgrFileName, -1)
                if not background:
                    return self._loadPlainBackground(screen)
                screenWidth = screen.get_rect()[2]
                screenHeight = screen.get_rect()[3]
                #если размер картинки равен размеру экрана программы - больше ничего не делаем            
                if (background.get_rect()[2] == screenWidth) and (background.get_rect()[3] == screenHeight): 
                    return background
                #если размеры разные - пытаемся подогнать
                background = pygame.transform.scale(background, (screenWidth, screenHeight))
                return background
            else:
                return self._loadPlainBackground(screen)
        except:
            print("Ошибка {} при загрузке фона {}".format(bckgrFileName, sys.exc_info()[0]))
            return self._loadPlainBackground(screen)
        
    def getFontByType(self, fontType):
        result = self.fontSettings.fonts
        return result.get(fontType)
    
    def getPaletteByType(self, typeName):
        return self.fontSettings.palette.get(typeName)
    
    #получает из настроек имя графический файлов, использующихся как скины для спрайта 
    def getSpriteSkins(self, key, defaultKey):
        skins = readStrKeyValue("Skins", key)
        if skins:
            return skins
        else:
            return defaultKey
        
    def loadSounds(self):
        soundOnStr = readStrKeyValue("Sounds", "Sound on")
        if not soundOnStr:
            soundOn = False
        else:
            if (soundOnStr.lower() == "true"):
                soundOn = True
            else:
                soundOn = False
        if not soundOn:
            return None
        try:
            nameOfGoodSnd = readStrKeyValue("Sounds", "Sound good")
            nameOfBadSnd = readStrKeyValue("Sounds", "Sound bad")
            if (nameOfGoodSnd and nameOfGoodSnd):
                return nameOfGoodSnd, nameOfBadSnd 
        except:    
            return None
            

class FontView(pygame.font.Font):
    def __init__(self, label = None, size = 36):
        self.label = label
        self.size = size
        self.color = (10, 10, 10)
        self.colorFail = (230, 230, 230)
        self.colorUi = self.color
        self.RLE = False 
        self.font = pygame.font.SysFont("Serif", self.size)
        
    def loadFont(self, dataDir):
        self.font = self.getFont(dataDir)
    
    def getFont(self, dataDir):
        intValue = readIntKeyValue("Fonts", self.label + " size")
        if intValue:
            self.size = intValue
        defaultFont = pygame.font.SysFont("Serif", self.size)
        strValue = readStrKeyValue('Fonts',self.label)
        if not strValue:
            return defaultFont
        if strValue.endswith("RLE"):
            self.RLE = True
            strValue =strValue.replace("RLE","").strip()
        if not strValue.endswith(".ttf"):
            strValue = strValue + ".ttf"
        font_path = os.path.join(dataDir, "fonts")
        font_path = os.path.join(font_path, strValue)
        if not (os.path.isfile(font_path)):
            print("Неправильный маршрут или имя файла шрифта %s"%font_path)
            return defaultFont
        if not (os.path.exists(font_path)):
            print("Файл шрифта не существует (%s) "%font_path)
            return defaultFont
        try:
            font = pygame.font.Font(font_path, self.size)
            return font
        except:
            print("Ошибка при загрузке шрифта (%s) "%strValue)
            return defaultFont


#определяет набор шоифтов, соответственно, для родного языка, изучаемого языка и интерфейса пользователя        
class FontSettings:
    loadingStatus = True
    palette = {}     
        
    def __loadPalette(self):
        color = readRGBKeyValue("Fonts", "Color answer")
        if color:
            self.color = color
        colorFail = readRGBKeyValue("Fonts", "Color wrong answer")
        if colorFail:
            self.colorFail = colorFail
        colorUi = readRGBKeyValue("Fonts", "Color interface")
        if colorUi:
            self.colorUi = colorUi
        self.palette.update({"Answer" : self.color})
        self.palette.update({"Bad answer" : self.colorFail})
        self.palette.update({"Interface" : self.colorUi})
        
    def loadFontSettings(self, dataDir):        
        self.__loadPalette()
        curFontView = FontView("Questions font")
        curFontView.loadFont(dataDir)
        if (curFontView.font == None):
            self.loadingStatus = False
            return
        self.fonts.update({"Questions font" : curFontView})

        curFontView = FontView("Answers font")
        curFontView.loadFont(dataDir)
        if (curFontView.font == None):
            self.loadingStatus = False
            return
        self.fonts.update({"Answers font" : curFontView})
        
        curFontView = FontView("Interface font")
        curFontView.loadFont(dataDir)
        if (curFontView == None):
            self.loadingStatus = False
            return
        self.fonts.update({"Interface font" : curFontView})

    def switchFonts(self):
        temp = self.fonts.get("Questions font")
        self.fonts.update({"Questions font" : self.fonts.get("Answers font")})
        self.fonts.update({"Answers font" : temp})

    def __init__(self):
        self.fonts = {}
        defaultFont = FontView()
        self.fonts.update({"Questions font" : defaultFont})
        self.fonts.update({"Answers font" : defaultFont})
        self.fonts.update({"Interface font" : defaultFont})
        self.palette.update({"Answer" : (10, 10, 10)})
        self.palette.update({"Bad answer" : (230, 230, 230)})
        self.palette.update({"Interface" : (10, 10, 10)})


global cfg 
cfg = Config()