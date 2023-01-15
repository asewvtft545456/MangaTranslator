from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtCore import Qt, QPoint, QRect, QRectF, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QPixmap, QColor, QTextOption, QFont, QCursor
from loguru import logger

class Image(QtWidgets.QLabel):

    def __init__(self, parent):
        super(Image, self).__init__(parent=parent)
        self.setPixmap(QtGui.QPixmap(":/newPrefix/whiteBG.jpg"))
        self.img = None
        self.image = QPixmap(":/newPrefix/whiteBG.jpg")
        self.begin = QPoint()
        self.end = QPoint()
        self.flag = False
        self.pages = {}
        self.connectDict = {}
        self.translated = {}
        self.japanese = {}
        self.color = {
            "White" : QColor(255, 255, 255),
            "Black" : QColor(0, 0, 0),
            "Red" : QColor(255, 0, 0),
            "Blue" : QColor(0, 0, 255),
            "Green" : QColor(0, 255, 0)
        }
        self.bg = "White"
        self.textColor = "Red"
        self.fontNum = 6
        self.rect = True
        self.scaledDict = {}
        self.erase = False

    @logger.catch
    def paintEvent(self, event):
        super().paintEvent(event)
        if self.flag and self.img != None:
            if self.erase:
                self.changeCursor()
            else:
                self.setCursor(QCursor(Qt.ArrowCursor))
            qp = QPainter(self)
            qp.setPen(QPen(self.color[self.textColor], 2, Qt.SolidLine))
            if self.rect:
                qp.drawRects(self.pages[self.img])
            if self.connectDict != {} and self.translated != {}:
                for index, words in enumerate(self.translated[self.connectDict[self.img]]):
                    a, b, c, d, = self.pages[self.img][index].getRect()
                    if self.bg != "None":
                        qp.fillRect(self.pages[self.img][index], self.color[self.bg])
                    qp.setFont(QFont("times",self.fontNum));
                    qp.drawText(QRectF(a, b, c, d), words, option=QTextOption())

            if not self.begin.isNull() and not self.end.isNull():
                qp.drawRect(QRect(self.begin, self.end).normalized())
            self.setPixmap(self.image)

    def mousePressEvent(self, event):
        if self.flag and self.img != None:
            if self.erase:
                self.changeCursor()
            else:
                self.setCursor(QCursor(Qt.ArrowCursor))
                self.begin = self.end = event.pos()
                self.update()
            super().mousePressEvent(event)

    @logger.catch
    def mouseMoveEvent(self, event):
        if self.flag and self.img != None:
            if self.erase:
                self.changeCursor()
                self.end = event.pos()
                self.update()
                nL = []
                p1 = self.end.x()
                p2 = self.end.y()
                if self.pages[self.img] != []:
                    for index, rect in enumerate(self.pages[self.img]):
                        x, y, w, h = rect.getRect()
                        if p1 >= x and p1 <= x+w and p2 >= y and p2 <= y+h:
                            nL.append((self.img, index))
                    for img, index in nL:
                        del self.pages[img][index]
            else:
                self.setCursor(QCursor(Qt.ArrowCursor))
                self.end = event.pos()
                self.update()
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.flag and self.img != None:
            if self.erase:
                self.changeCursor()
            else:
                self.setCursor(QCursor(Qt.ArrowCursor))
                r = QRect(self.begin, self.end).normalized()
                self.pages[self.img].append(r)
                self.begin = self.end = QPoint()
                self.update()
            super().mouseReleaseEvent(event)
    
    def changeCursor(self):
        cursor = QPixmap(":/newPrefix/eraser.png")
        cursorScaled = cursor.scaled(QtCore.QSize(35, 35), Qt.KeepAspectRatio)
        currCursor = QCursor(cursorScaled, -1, -1)
        self.setCursor(currCursor)