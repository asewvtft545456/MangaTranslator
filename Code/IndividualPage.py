import cv2
from PyQt5.QtCore import QRunnable, pyqtSignal, QObject
import qimage2ndarray
import numpy as np
from pprint import pprint
from RectangleManipulation import Rectangles
from FileHandling import FileHandler
from Configer import Settings
from Translation import MangaBag


class Worker(QObject):
    result = pyqtSignal(object)
    finished = pyqtSignal()
    progress = pyqtSignal(int)


class SingleTranslate(QRunnable):
    
    def __init__(self, img, mocr, translator, combN, combO, sliderNum, langauge):
        super(SingleTranslate, self).__init__()
        self.imag1 = img
        self.setting = Settings()
        self.handling = FileHandler()
        self.name = translator
        self.shouldCombN = combN
        self.shouldCombO = combO
        self.range = sliderNum
        self.signals = Worker()
        self.directory = self.setting.cropText
        self.portions = 100/3
        self.cnt = 0
        self.mocr = mocr
        self.source = langauge
        self.manga = MangaBag()


    def locateText(self, image):
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

        fontSize, thickness = self.manga.getFontSizeThickness(self.imag1)
        self.img1 = cv2.imread(r"{}".format(self.imag1))
        self.image = cv2.cvtColor(self.img1, cv2.COLOR_BGR2RGB)
        gotten_text = self.locateText(self.image)
        self.cnt += self.portions
        self.signals.progress.emit(self.cnt)
        # pprint(gotten_text)

        finalText = self.manga.get_japanese(self.image, self.mocr, gotten_text, self.directory)
        self.cnt += self.portions
        self.signals.progress.emit(self.cnt)
        # pprint(finalText)

        newList = self.manga.translate(finalText, self.name, self.source)
        self.cnt += self.portions
        self.signals.progress.emit(self.cnt)
        # pprint(newList)
        addNewLine = self.manga.segment(newList)

        final = self.manga.write(self.image, gotten_text, addNewLine, fontSize, thickness)
        myarray = np.array(final)
        image = qimage2ndarray.array2qimage(myarray)
        self.cnt += self.portions
        self.signals.progress.emit(self.cnt)

        self.signals.result.emit(image)
        self.handling.deleteFiles(self.directory)
        self.signals.finished.emit()