import cv2
from PyQt5.QtCore import QRunnable, pyqtSignal, QObject
import qimage2ndarray
import numpy as np
from pprint import pprint
from RectangleManipulation import *
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
        self.manga = MangaBag()
        self.name = translator
        self.shouldCombN = combN
        self.shouldCombO = combO
        self.range = sliderNum * self.manga.getRatio(self.imag1) + 4
        self.signals = Worker()
        self.directory = self.setting.cropText
        self.portions = 100/3
        self.cnt = 0
        self.mocr = mocr
        self.source = langauge


    def locateText(self, image):
        myDict = self.manga.get_text(image)
        if self.shouldCombN and self.shouldCombO:
            bound1 = rectanglesCO(myDict, "c")
            bound2 = combine_rectangles(bound1, self.range)
            overlap1 = rectanglesCO(bound2, "o")
            overlap = combine_overlapping_rectangles(overlap1)
            return overlap
        elif self.shouldCombN and not(self.shouldCombO):
            bound1 = rectanglesCO(myDict, "c")
            bound2 = combine_rectangles(bound1, self.range)
            return bound2
        elif self.shouldCombO and not(self.shouldCombN):
            overlap1 = rectanglesCO(bound2, "o")
            overlap2 = combine_overlapping_rectangles(overlap1)
            return overlap2
        else:
            return myDict

    def run(self):
        try:
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
            addNewLine1 = self.manga.addNewLine(self.imag1, newList, gotten_text, cv2.FONT_HERSHEY_DUPLEX, fontSize, thickness)

            final = self.manga.write(self.image, gotten_text, addNewLine1, fontSize, thickness)
            myarray = np.array(final)
            image = qimage2ndarray.array2qimage(myarray)
            self.cnt += self.portions
            self.signals.progress.emit(self.cnt)
        except:
            self.signals.finished.emit()
        else:
            self.signals.result.emit(image)
            self.signals.finished.emit()
        finally:
            self.handling.deleteFiles(self.directory)