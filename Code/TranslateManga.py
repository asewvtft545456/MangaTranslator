import cv2
from PyQt5.QtCore import QRunnable, pyqtSignal, QObject
import qimage2ndarray
import numpy as np
from pprint import pprint
from RectangleManipulation import Rectangles
import langid
from FileHandling import FileHandler
from Configer import Settings
from Translation import MangaBag


class Worker(QObject):
    result = pyqtSignal(object)
    stored = pyqtSignal(object)
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    booleans = pyqtSignal(object)
    lang = pyqtSignal(str)


class Translate(QRunnable):
    
    def __init__(self, img, mocr, translator, combN=False, combO=False, sliderNum=0):
        super(Translate, self).__init__()
        self.imag1 = img
        self.setting = Settings()
        self.handling = FileHandler()
        self.name = translator
        self.shouldCombN = combN
        self.shouldCombO = combO
        self.range = sliderNum
        self.signals = Worker()
        self.directory = self.setting.cropText
        self.portions = (100 / len(self.imag1))/3
        self.cnt = 0
        self.mocr = mocr
        self.source = None
        self.manga = MangaBag()

    def LocateText(self, image):
        myDict = self.manga.get_text(image)
        rect = Rectangles()
        if self.shouldCombN and self.shouldCombO:
            bounding = rect.neighborRect(myDict, self.range)
            overlap = rect.combineOverlap(bounding)
            return overlap
        elif self.shouldCombN and not(self.shouldCombO):
            bounding1 = rect.neighborRect(myDict, self.range)
            return bounding1
        elif self.shouldCombO and not(self.shouldCombN):
            overlap1 = rect.combineOverlap(myDict)
            return overlap1
        else:
            return myDict


    def run(self):
        finalImg = []
        backup = []
        for x in self.imag1:
            # print(x)
            fontSize, thickness = self.manga.getFontSizeThickness(x)
            self.img1 = cv2.imread(r"{}".format(x))
            self.image = cv2.cvtColor(self.img1, cv2.COLOR_BGR2RGB)
            gotten_text = self.LocateText(self.image)
            self.cnt += self.portions
            self.signals.progress.emit(self.cnt)
            # pprint(gotten_text)

            finalText = self.manga.get_japanese(self.image, self.mocr, gotten_text, self.directory)
            self.cnt += self.portions
            self.signals.progress.emit(self.cnt)
            finalTextcopy = finalText.copy()
            # pprint(finalText)

            if self.source == None and finalText != {}:
                for y in list(finalText.values()):
                    if y != []:
                        self.source = langid.classify(y[0])[0]
                        break

            newList = self.manga.translate(finalText, self.name, self.source)
            if newList == "ConnectionError":
                break
            self.cnt += self.portions
            self.signals.progress.emit(self.cnt)
            # pprint(newList)
            addNewLine = self.manga.segment(newList)
            stripDict = {}
            for key in addNewLine:
                stripDict[key.strip()] = addNewLine[key]

            final = self.manga.write(self.image, gotten_text, stripDict, fontSize, thickness)
            myarray = np.array(final)
            image = qimage2ndarray.array2qimage(myarray)
            finalImg.append(image)
            self.cnt += self.portions
            backup.append((x, gotten_text, finalTextcopy))
            self.signals.progress.emit(self.cnt)
        self.signals.result.emit(finalImg)
        self.signals.stored.emit(backup)
        self.signals.booleans.emit([self.name, self.shouldCombN, self.shouldCombO, self.range])
        self.signals.lang.emit(self.source)
        self.handling.deleteFiles(self.directory)
        self.signals.finished.emit()
