import cv2
from PyQt5.QtCore import QRunnable, pyqtSignal, QObject
import qimage2ndarray
import numpy as np
from pprint import pprint
from RectangleManipulation import *
import langid
from FileHandling import FileHandler
from Configer import Settings
from Translation import MangaBag
from loguru import logger


class Worker(QObject):
    result = pyqtSignal(object)
    stored = pyqtSignal(object)
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    booleans = pyqtSignal(object)
    lang = pyqtSignal(str)


class Translate(QRunnable):
    
    def __init__(self, img, mocr, translator,language, combN=False, combO=False, sliderNum=0):
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
        self.source = None if language == "auto" else language
        self.manga = MangaBag()
        self.ratio = 1

    
    def LocateText(self, image):
        myDict = self.manga.get_text(image)
        if self.shouldCombN and self.shouldCombO:
            bound1 = rectanglesCO(myDict, "c")
            bound2 = combine_rectangles(bound1, self.range)
            overlap1 = rectanglesCO(bound2, "o")
            overlap = combine_overlapping_rectangles(overlap1)
            return overlap
        elif self.shouldCombN and not(self.shouldCombO):
            bound3 = rectanglesCO(myDict, "c")
            bound4 = combine_rectangles(bound3, self.range)
            return bound4
        elif self.shouldCombO and not(self.shouldCombN):
            overlap3 = rectanglesCO(myDict, "o")
            overlap4 = combine_overlapping_rectangles(overlap3)
            return overlap4
        else:
            return myDict


    def run(self):
        finalImg = []
        backup = []
        try:
            for x in self.imag1:
                fontSize, thickness = self.manga.getFontSizeThickness(x)
                self.ratio = self.manga.getRatio(x) + 4
                print(self.ratio)
                self.range *= self.ratio
                self.img1 = cv2.imread(r"{}".format(x))
                self.image = cv2.cvtColor(self.img1, cv2.COLOR_BGR2RGB)
                gotten_text = self.LocateText(self.image)
                # pprint(gotten_text)
                self.cnt += self.portions
                self.signals.progress.emit(self.cnt)

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
                self.cnt += self.portions
                self.signals.progress.emit(self.cnt)
                # pprint(newList)
                addNewLine1 = self.manga.addNewLine(x, newList, gotten_text, cv2.FONT_HERSHEY_DUPLEX, fontSize, thickness)
                

                final = self.manga.write(self.image, gotten_text, addNewLine1, fontSize, thickness)
                myarray = np.array(final)
                image = qimage2ndarray.array2qimage(myarray)
                finalImg.append(image)
                self.cnt += self.portions
                backup.append((x, gotten_text, finalTextcopy))
                self.signals.progress.emit(self.cnt)
        except:
            logger.exception("ERROR")
            self.signals.finished.emit()
        else:
            self.signals.result.emit(finalImg)
            self.signals.stored.emit(backup)
            self.signals.booleans.emit([self.name, self.shouldCombN, self.shouldCombO, self.range])
            self.signals.lang.emit(self.source)
            self.signals.finished.emit()
        finally:
            self.handling.deleteFiles(self.directory)
