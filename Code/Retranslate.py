from PyQt5.QtCore import QRunnable, pyqtSignal, QObject
import qimage2ndarray
import numpy as np
import cv2
from pprint import pprint
from loguru import logger
from Translation import MangaBag

class ReWorker(QObject):
    result = pyqtSignal(object)
    finished = pyqtSignal()
    progress = pyqtSignal(int)

class Retranslate(QRunnable):
    def __init__(self, storedList, translator, langauge):
        super(Retranslate, self).__init__()
        self.preList = storedList
        self.translator = translator
        self.signals = ReWorker()
        self.portions = (100 / len(self.preList))/3
        self.cnt = 0
        self.source = langauge
        self.manga = MangaBag()

    def run (self):
        newImg = []
        for image, rectangles, japanese in self.preList:
            if japanese == {}:
                newImg.append(image)
                continue

            fontSize, thickness = self.manga.getFontSizeThickness(image)
            img1 = cv2.imread(r"{}".format(image))
            cvImage = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
            self.cnt += self.portions
            self.signals.progress.emit(self.cnt)
            
            copyJapanese = japanese.copy()
            
            newTranslate = self.manga.translate(copyJapanese, self.translator, self.source)
            addNewLine = self.manga.segment(newTranslate)
            self.cnt += self.portions
            self.signals.progress.emit(self.cnt)

            final = self.manga.write(cvImage, rectangles, addNewLine, fontSize, thickness)
            self.cnt += self.portions
            self.signals.progress.emit(self.cnt)

            myarray = np.array(final)
            image1 = qimage2ndarray.array2qimage(myarray)
            newImg.append(image1)
        self.signals.result.emit(newImg)
        self.signals.finished.emit()