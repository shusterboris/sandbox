#coding=utf8
import os, sys, random
from enum import Enum
from appenviron import AppEnv
from appconfig import Config, cfg

class Dictionaries:
    def __init__(self):
        self.words = []       
        self.cfg = cfg
        self.dictFileName = os.path.join(AppEnv.getDictDir(), self.cfg.dictFileName)
        self.defDictFileName = os.path.join(AppEnv.getDictDir(), self.cfg.dictDefaultFileName)
    
    def __repr__(self):
        result = "Dictionary [name]="+self.name+", [size]="+str(len(self.words))
        result += str(self.words)
        return result

        
    #разбирает строку справочника.Возвращает кортеж WordRecord и код ошибки
    def fetchLine(self, rec):
        #в файле в каждой строке: слово, перевод, транскрипция, мэм-ассоциация 
        #для улучшения запоминания, имя графического файла с изображением
        #имя файла со звуком
        #разделены точкой с запятой. два первых обязательные, остальные - нет
                
        rec = rec.strip()
        if not (rec): #строка пустая
            return None, ''
        parts = rec.split(self.cfg.wordsDelimiter)
        if len(parts) < 2:
            #строка содержит только 1 слово, т.е. нет перевода или нет разделителей
            return None, 'Неверная строка в словаре'
        if len(parts) == 2:
            return WordRecord(parts[0],parts[1]), ''
        elif len(parts) == 3:
            return WordRecord(parts[0],parts[1], parts[2]), ''
        elif len(parts) == 4:
            return WordRecord(parts[0],parts[1], parts[2], parts[3]), ''
        elif len(parts) == 5:
            return WordRecord(parts[0],parts[1], parts[2], parts[3], parts[4]), ''
        elif len(parts) == 6:
            return WordRecord(parts[0],parts[1], parts[2], parts[3], parts[4], parts[5]), ''
        else:
            #строка содержит больше слов, разделенных ";" чем положено - ошибка
            return None, 'Слишком много частей в строке словаря'
        
    #загружает файл со словами, разбирает слова и составляет словарь в виде списка
    def loadDictFromFile(self,fullName):
        #dictionary presets: does it use RLE alphabets and direction of translation
        if not os.path.isfile(fullName):
            return "Неправильное имя файла: "+fullName
        elif not os.path.exists(fullName):
            return "Не существует файла с именем: "+fullName
            
        try:
            result = True
            i = 0            
            f = open(fullName, "r", encoding="utf-8")
            for line in f:
                #result is WordRecord: word, translate and so on
                result = self.fetchLine(line)
                wordRec = result[0]
                if not (wordRec == None):
                    #добавляем строку в список слов
                    if not self.cfg.straightDictDir:
                        wordRec.switchWordAndTranslate()
                    self.words.append(wordRec)
                else:  
                    #если это первая строка файла и в ней одиночное слово - это название
                    #в остальных случаях просто пропускаем эту строку
                    error = result[1]
                    if (i == 0 and error == 'Неверная строка в словаре'):
                        self.name = line;
                i =+ 1
            if (len(self.words) != 0):
                return ""
            else:
                return "Cловарь %s указанный в настройках пустой или неправильно заполнен"%self.dictFileName 
        except OSError as err:
            return "Ошибка при работе с файлом: {0}".format(err)
        except:
            return "Ошибка:", sys.exc_info()[0]
        else:
            f.close()

    #для каждого словаря создает подпаки длях ранения звуковых и графических файлов
    def _checkOrCreateDictionarySubfolders(self, dictName):
        nameWithoutExt = os.path.splitext(dictName)
        pureName = os.path.split(nameWithoutExt[0])
        folderName = os.path.join(AppEnv.getDictDir(), pureName[1])
        try:
            if not (os.path.exists(folderName) and os.path.isdir(folderName)):
                os.mkdir(folderName) 
            soundsFolder = os.path.join(folderName, "sounds")
            if not (os.path.exists(soundsFolder) and os.path.isdir(soundsFolder)):
                os.mkdir(soundsFolder) 
            imagesFolder = os.path.join(folderName, "images")
            if not (os.path.exists(imagesFolder) and os.path.isdir(imagesFolder)):
                os.mkdir(imagesFolder) 
            AppEnv.soundsDir = soundsFolder
            AppEnv.imagesDir = imagesFolder
        except:
            AppEnv.soundsDir = ""
            AppEnv.imagesDir = ""
            Config.appLog.warning("Невозможно создать папку для пользовательского словаря. "+str(sys.exc_info()))
            
    def loadDict(self):
        result = self.loadDictFromFile(self.dictFileName)
        if result == "":
            self._checkOrCreateDictionarySubfolders(self.dictFileName)
            return "";
        result = self.loadDictFromFile(self.defDictFileName) 
        if result == "":
            self._checkOrCreateDictionarySubfolders(self.defDictFileName)
            return ""
        else:
            return "Не удалось прочитать ни один словарь указанный в настройках"
                  
    
    def getRandomWord(self):
        ind = random.randint(0, len(self.words) - 1)
        return self.words[ind]

    def createWordQuestion(self, wordRec):
        question = WordQuestion(wordRec,self)
        return question
        
#запись словаря
class WordRecord:
    #настройки: прямой порядок слово-перевод, слово справа налево, перевод справа налево
    settings = {False, False, False}
    def __init__(self, word, trnslt, trnscr='', mem='', imgPath='', soundPath=''):
        #trnslt = self._wordReverse(trnslt)
        self.word = word
        self.trnslt = trnslt
        self.trnscr = trnscr
        self.mem = mem
        self.imgPath = imgPath
        self.label = trnslt
        self.soundPath = soundPath
    
    def __repr__(self):
        result = "WordRecord [word]="+self.word+", [translate]="+self.trnslt
        if (self.trnscr): result += (", [transcription]=" + self.trnscr)
        if (self.mem): result += (", [transcription]=" + self.mem)
        if (self.imgPath): result += (", [transcription]=" + self.imgPath)
        return result
    
    def switchWordAndTranslate(self):
        temp = self.word
        self.word = self.trnslt
        self.trnslt = temp
        
    def getWord(self):        
        return self.word
    
    def getTranslation(self):
        return self.trnslt
    
    def getTranslationView(self):
        return self.trnslt
    
#состояние выученности слова    
class WordLearningStatus(Enum):
    New = 0
    NeverAsk = 10000 

#очередной вопрос: слово и варианты ответов
class WordQuestion(WordRecord):
    
    def __init__(self, wordRec, dictionary):
        #TODO хорошо бы сделать уменьшение статуса с течением времени
        WordRecord.__init__(self, wordRec.word, wordRec.trnslt, wordRec.trnscr, wordRec.mem, wordRec.imgPath, wordRec.soundPath)
        #статус выученности: 0 - новый, каждый верный ответ увеличивает статус на 1, неверный уменьшает
        #TODO пока не вычисляется
        self.learningState = 0;
        #статус в текущем сеансе (для определения кол-ва правильных/неправильных ответов). 0=новый, 1=правильныйб -1=неправильный
        self.state = 0
        self.answers = {wordRec.trnslt}
        self.dictionary = dictionary
        #добавляем в возможные варианты ответов уникальные значения
        while not len(self.answers) > (self.dictionary.cfg.numberOfAnswers - 1):
            current = self.dictionary.getRandomWord()            
            self.answers.add(current.trnslt)
            
    def __repr__(self):
        result = "WordQuestion: [state]="+str(self.state)+ " ,[word] = " + self.word
        result += ", [translate] = " + self.trnslt + ", " + str(self.answers) 
        return result
    
    def _loadSound(self):
        if WordRecord.sound:
            return None
        return AppEnv.loadSound(self.soundPath)
    
    def _loadImageTip(self):
        if not self.imgPath:
            return None
        return AppEnv.loadImage(self.imgPath, -1)
    
    def changeState(self, isSuccess, successed, failed):
        #только если успешный ответ получен в первой попытке, увеличиваем счетчик успешных и присваиваем стаус "успешно"
        if isSuccess:            
            if (self.state == 0):
                successed += 1
                self.state = 1
        else:
            #если попытка не успешно, ставим статус, но число неуспешных увеличивает только первый неправильный ответ 
            if (self.state == 0):
                failed += 1
            self.state = -1
        return successed, failed
    
@staticmethod     
def wordReverse(src):
    #reverse order of letters in the src (RLE)
    lst = list(src) 
    lst.reverse()
    s = ""  
    for letter in lst:  
        s += letter
    return s
