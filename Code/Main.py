from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog, QShortcut
from PyQt5.QtGui import QPixmap
import sys
from PyQt5 import QtWidgets
from mainApp import Ui_MainWindow
from Canvas import Image
from PyQt5.QtCore import QThreadPool, pyqtSignal, Qt, QPoint, QRect, QRectF, QEventLoop
from TranslateManga import Translate
from DownloadTweet import Twitter
from Retranslate import Retranslate
from PIL import ImageQt
import img2pdf
from Configer import Settings
from FileHandling import FileHandler
from settingsGUI import Ui_Form
from manga_ocr import MangaOcr
from IndividualPage import SingleTranslate
from PyQt5.QtGui import QPixmap, QColor, QTextOption, QFont, QPen
from loguru import logger
from ManualTranslation import ManualTranslation
from loguru import logger
from pprint import pprint

class interact(QtWidgets.QMainWindow, Ui_MainWindow):
    active = pyqtSignal()

    def __init__(self):
        super(interact, self).__init__()
        self.setupUi(self)
        self.resize(970, 940)
        self.appMod()
        self.stylesheet1()
        self.buttonConnections()
        self.widgetSizes()
        self.setting = Settings()
        self.handling = FileHandler()
        self.thread = QThreadPool()
        self.index = 0
        self.newIndex = 0
        self.translatedFiles = []
        self.files = []
        self.isClicked = False
        self.shownSetting = False
        self.setButton.setCheckable(True)
        self.bar.setValue(0)
        self.bar.setFormat("Translating....")
        self.bar.setGeometry(self.width()//2-65, self.height()//2, 200, 30)
        self.bar.setVisible(False)
        self.bar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.fontsize.setMaximum(15)
        self.translator = "Bing"
        self.range = 0
        self.combineN = False
        self.rangeSlider.setEnabled(False)
        self.combineO = True
        self.changeTranslation = []
        self.checkthing = []
        self.single = False
        self.ocr = MangaOcr()
        self.orgLanguage = None
        self.clearButton.hide()
        self.saveButton.hide()
        self.editRect.hide()
        self.clearButton.clicked.connect(self.clear)
        self.im.adjustSize()
        self.shownWidget = False
        self.searchwidget.hide()
        self.recycle = {}
        self.num = -1
        self.isSort = False
        self.widget_2.hide()
        self.advanceSettings1()

    
    def appMod(self):
        self.settings.hide()
        self.setWindowTitle("MangaTranslator")
        self.setWindowIcon(QtGui.QIcon("Icons\\translation.png"))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Icons\\arrow.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.leftArrow.setIcon(icon1)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Icons\\settings.png"),QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.setButton.setIcon(icon)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Icons\\arrow1.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.rightArrow.setIcon(icon2)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("Icons\\download.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton.setIcon(icon3)
        self.translateOptions.addItem('Youdao')
        self.translateOptions.addItem('MyMemory')
        self.bGcolor.addItem("None")
        self.Form = QtWidgets.QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(self.Form)
        self.Form.setAttribute(Qt.WA_DeleteOnClose)
        self.Form.setMinimumSize(QtCore.QSize(720, 415))
        self.im = Image(self.imageWidget)
        self.im.setScaledContents(True)
        self.on1 = False
        self.on2 = False
        QShortcut(QtCore.Qt.Key_Right, self, self.moveRight)
        QShortcut(QtCore.Qt.Key_Left, self, self.moveLeft)
    
    def widgetSizes(self):
        self.imageWidget.setMaximumSize(QtCore.QSize(900,800))
        self.settings.setMaximumSize(QtCore.QSize(290, 11111))
        self.settings.setMinimumSize(QtCore.QSize(290, 340))
        self.translate.setMinimumSize(QtCore.QSize(130, 40))
        self.upload.setMinimumSize(QtCore.QSize(130, 40))
        self.saveButton.setMinimumSize(QtCore.QSize(130, 40))
        self.editRect.setMinimumSize(QtCore.QSize(400, 70))
        self.undoButton.setMinimumSize(QtCore.QSize(100, 50))
        self.redoButton.setMinimumSize(QtCore.QSize(100, 50))
        self.eraseButton.setMinimumSize(QtCore.QSize(100, 50))
        self.undoButton.setIconSize(QtCore.QSize(30, 30))
        self.redoButton.setIconSize(QtCore.QSize(30, 30))
        self.eraseButton.setIconSize(QtCore.QSize(30, 30))
        self.widget.setMinimumSize(QtCore.QSize(100, 250))
        self.widget.setMaximumSize(QtCore.QSize(100, 250))
        self.ui.saveSet.setMinimumSize(QtCore.QSize(100, 30))
        self.ui.label_4.setText("Twitter")
        

    def buttonConnections(self):
        self.upload.clicked.connect(self.upload1)
        self.rightArrow.clicked.connect(self.moveRight)
        self.leftArrow.clicked.connect(self.moveLeft)
        self.translate.clicked.connect(self.translate1)
        self.translate.clicked.connect(self.showProgress)
        self.setButton.clicked.connect(self.showSet)
        self.setButton.clicked.connect(self.showSettings)
        self.pushButton.clicked.connect(self.linkUpload)
        self.advanced.clicked.connect(self.advanceSettings)
        self.ui.saveSet.clicked.connect(self.getInfo)
        self.translateOptions.currentTextChanged.connect(self.choosenTranslator)
        self.Textcolor.currentTextChanged.connect(self.textColors)
        self.bGcolor.currentTextChanged.connect(self.backgroundColor)
        self.rangeSlider.valueChanged.connect(self.chooseRange)
        self.fontsize.valueChanged.connect(self.chooseFontNumber)
        self.combineNeighbors.stateChanged.connect(self.showCombN)
        self.combineOverLap.stateChanged.connect(self.showCombO)
        self.singlePtranslate.stateChanged.connect(self.getCurr)
        self.saveButton.clicked.connect(self.saveImages)
        self.horizontalLayout.addWidget(self.im)
        self.manualButton.clicked.connect(self.changeToManual)
        self.automaticButton.clicked.connect(self.changeToAutomatic)
        self.sortButton.stateChanged.connect(self.sortFile)
        self.removeRect.stateChanged.connect(self.removeRectangle)
        self.pushButton_2.clicked.connect(self.showSearch)
        self.undoButton.clicked.connect(self.undo)
        self.redoButton.clicked.connect(self.redo)
        self.eraseButton.clicked.connect(self.startErase)
        

    def stylesheet1(self):
        self.bar.setStyleSheet("QProgressBar\n"
                          "{\n"
                          "border: solid grey;\n"
                          "border-radius: 15px;\n"
                          "background-color: white;\n"
                          "color:black;\n"
                          "}\n"
                          "QProgressBar::chunk"
                          "{\n"
                          "background-color: #05B8CC;\n"
                          "border-radius:15px;\n"
                          "}\n")
        self.automaticButton.setStyleSheet("QPushButton{\n"
                            "height:50;\n"
                            "width: 50;\n"
                            "border-radius: 15px;\n"
                            "background-color: QLinearGradient( x1: 0, y1: 0,\n"
                            "                             x2: 1, y2: 0, \n"
                            "                          stop: 0 #fa71cd, \n"
                            "                          stop: 1 #c471f5);\n"
                            "}\n"
                            "QPushButton:hover:!pressed\n"
                            "{\n"
                            "background-color: QLinearGradient( x1: 0, y1: 0,\n"
                            "                             x2: 1, y2: 0, \n"
                            "                          stop: 0 #fa71cd, \n"
                            "                          stop: 1 #c471f5);\n"
                            "}")
        self.manualButton.setStyleSheet("QPushButton{\n"
                            "height:50;\n"
                            "width: 50;\n"
                            "border-radius: 15px;\n"
                            "background-color: rgb(82, 82, 82);\n"
                            "color: rgb(255, 255, 255);\n"
                            "}\n"
                            "QPushButton:hover:!pressed\n"
                            "{\n"
                            "background-color: QLinearGradient( x1: 0, y1: 0,\n"
                            "                             x2: 1, y2: 0, \n"
                            "                          stop: 0 #fa71cd, \n"
                            "                          stop: 1 #c471f5);\n"
                            "}")
        self.advanced.setStyleSheet("QPushButton{\n"
                            "height:30;\n"
                            "width: 111;\n"
                            "border-radius: 5px;\n"
                            "background-color: rgb(82, 82, 82);\n"
                            "color: rgb(255, 255, 255);\n"
                            "}\n"
                            "QPushButton:hover:!pressed\n"
                            "{\n"
                            "background-color: QLinearGradient( x1: 0, y1: 0,\n"
                            "                             x2: 1, y2: 0, \n"
                            "                          stop: 0 #fa71cd, \n"
                            "                          stop: 1 #c471f5);\n"
                            "}")
        
        

    def changeToManual(self):
        self.im.flag = True
        self.drawOnPages()
        self.AutoWidget.hide()
        self.ManualWidget.show()
        self.editRect.show()
        self.settings.show()
        self.widget_2.hide()
        self.manualButton.setStyleSheet("QPushButton{\n"
                        "height:50;\n"
                        "width: 50;\n"
                        "border-radius: 15px;\n"
                        "background-color: QLinearGradient( x1: 0, y1: 0,\n"
                        "                             x2: 1, y2: 0, \n"
                        "                          stop: 0 #fa71cd, \n"
                        "                          stop: 1 #c471f5);\n"
                        "}\n"
                        "QPushButton:hover:!pressed\n"
                        "{\n"
                        "background-color: QLinearGradient( x1: 0, y1: 0,\n"
                        "                             x2: 1, y2: 0, \n"
                        "                          stop: 0 #fa71cd, \n"
                        "                          stop: 1 #c471f5);\n"
                        "}")
        self.automaticButton.setStyleSheet("QPushButton{\n"
                        "height:50;\n"
                        "width: 50;\n"
                        "border-radius: 15px;\n"
                        "background-color: rgb(82, 82, 82);\n"
                        "color: rgb(255, 255, 255);\n"
                        "}\n"
                        "QPushButton:hover:!pressed\n"
                        "{\n"
                        "background-color: QLinearGradient( x1: 0, y1: 0,\n"
                        "                             x2: 1, y2: 0, \n"
                        "                          stop: 0 #fa71cd, \n"
                        "                          stop: 1 #c471f5);\n"
                        "}")
        if self.on1:
            self.settings.hide()
            self.on1= False
        else:
            self.on1 = True
            self.on2 = False
            self.shownSetting = False

    def changeToAutomatic(self):
        self.im.flag = False
        self.ManualWidget.hide()
        self.AutoWidget.show()
        self.editRect.hide()
        self.settings.show()
        self.widget_2.hide()
        self.automaticButton.setStyleSheet("QPushButton{\n"
                                "height:50;\n"
                                "width: 50;\n"
                                "border-radius: 15px;\n"
                                "background-color: QLinearGradient( x1: 0, y1: 0,\n"
                                "                             x2: 1, y2: 0, \n"
                                "                          stop: 0 #fa71cd, \n"
                                "                          stop: 1 #c471f5);\n"
                                "}\n"
                                "QPushButton:hover:!pressed\n"
                                "{\n"
                                "background-color: QLinearGradient( x1: 0, y1: 0,\n"
                                "                             x2: 1, y2: 0, \n"
                                "                          stop: 0 #fa71cd, \n"
                                "                          stop: 1 #c471f5);\n"
                                "}")
        self.manualButton.setStyleSheet("QPushButton{\n"
                                "height:50;\n"
                                "width: 50;\n"
                                "border-radius: 15px;\n"
                                "background-color: rgb(82, 82, 82);\n"
                                "color: rgb(255, 255, 255);\n"
                                "}\n"
                                "QPushButton:hover:!pressed\n"
                                "{\n"
                                "background-color: QLinearGradient( x1: 0, y1: 0,\n"
                                "                             x2: 1, y2: 0, \n"
                                "                          stop: 0 #fa71cd, \n"
                                "                          stop: 1 #c471f5);\n"
                                "}")
        if self.translatedFiles != []:
            self.showImage()
        if self.on2:
            self.settings.hide()
            self.on2= False
        else:
            self.on2 = True
            self.on1 = False
            self.shownSetting = False

    def advanceSettings1(self):
        self.ui.translatePath.setText(str(self.setting.Translated))
        self.ui.cropPath.setText(str(self.setting.cropText))
        self.ui.deeplKey.setText(str(self.setting.downLoad))
        self.ui.consumerKey.setText(str(self.setting.consumer_key))
        self.ui.consumerSecret.setText(str(self.setting.consumer_secret))
        self.ui.accessToken.setText(str(self.setting.access_token))
        self.ui.accessTokenSecret.setText(str(self.setting.access_token_secret))
        self.ui.bearerToken.setText(str(self.setting.bearer_token))

    def advanceSettings(self):
        self.ui.translatePath.setText(str(self.setting.Translated))
        self.ui.cropPath.setText(str(self.setting.cropText))
        self.ui.deeplKey.setText(str(self.setting.downLoad))
        self.ui.consumerKey.setText(str(self.setting.consumer_key))
        self.ui.consumerSecret.setText(str(self.setting.consumer_secret))
        self.ui.accessToken.setText(str(self.setting.access_token))
        self.ui.accessTokenSecret.setText(str(self.setting.access_token_secret))
        self.ui.bearerToken.setText(str(self.setting.bearer_token))

        self.Form.show()
        
    def getInfo(self):
        save = self.ui.translatePath.text()
        crop = self.ui.cropPath.text()
        download = self.ui.deeplKey.text()
        consumer_key = self.ui.consumerKey.text()
        consumer_secret = self.ui.consumerSecret.text()
        access_token = self.ui.accessToken.text()
        access_token_secret = self.ui.accessTokenSecret.text()
        bearer_token = self.ui.bearerToken.text()
        if save != self.setting.Translated:
            self.setting.updateSetting("Paths", "Translated", save)
            self.ui.translatePath.setText(save)

        if crop != self.setting.cropText:
            self.setting.updateSetting("Paths", "cropText", crop)
            self.ui.cropPath.setText(crop)

        if download != self.setting.downLoad:
            self.setting.updateSetting("Paths", "Download", download) 
            self.ui.deeplKey.setText(download)

        if consumer_key != self.setting.consumer_key:
            self.setting.updateSetting("Twitter", "Consumer key", consumer_key)
            self.ui.consumerKey.setText(consumer_key)

        if consumer_secret != self.setting.consumer_secret:
            self.setting.updateSetting("Twitter", "Consumer secret", consumer_secret)
            self.ui.consumerSecret.setText(consumer_secret)

        if access_token != self.setting.access_token:
            self.setting.updateSetting("Twitter", "Access token", access_token)
            self.ui.accessToken.setText(access_token)

        if access_token_secret != self.setting.access_token_secret:
            self.setting.updateSetting("Twitter", "Access token secret", access_token_secret)
            self.ui.accessTokenSecret.setText(access_token_secret)

        if bearer_token != self.setting.bearer_token:
            if "%" in bearer_token:
                bearer_token = str(bearer_token.split("%"))
                self.setting.updateSetting("Twitter", "Bearer token", bearer_token)
                self.ui.bearerToken.setText(bearer_token)
    
    def sortFile(self, n):
        if n and self.files != []:
            self.files.sort()
            self.showImage()
        self.isSort = True
    
    def removeRectangle(self, n):
        if n:
            self.im.rect = False
        else:
            self.im.rect = True

    def changeTrans(self, n):
        self.changeTranslation = n

    def changeCheckThing(self, n):
        self.checkthing = n
    
    def showSet(self):
        self.settings.show()
        self.widget_2.show()
        self.AutoWidget.hide()
        self.ManualWidget.hide()

    def showSettings(self):
        if self.shownSetting:
            self.settings.hide()
            self.shownSetting= False
        else:
            self.shownSetting = True
            self.on1 = False
            self.on2 = False

    def showSearch(self):
        self.searchwidget.show()
        
        if self.shownWidget:
            self.searchwidget.hide()
            self.shownWidget = False
        else:
            self.shownWidget = True

    def startErase(self):
        if self.im.erase:
            self.im.erase = False
            self.eraseButton.setStyleSheet("QPushButton{\n"
                                            "border:none;\n"
                                            "width:150px;\n"
                                            "height:50px;\n"
                                            "border-radius:5px;\n"
                                            "}\n"
                                            "QPushButton:hover:!pressed{\n"
                                            "border:1px solid rgb(170, 0, 255);\n"
                                            "}\n"
                                            "\n"
                                            "")
        else:
            self.im.erase = True
            self.eraseButton.setStyleSheet("QPushButton{\n"
                                            "width:150px;\n"
                                            "height:50px;\n"
                                            "border-radius:5px;\n"
                                            "border:2px solid rgb(170, 0, 255);\n"
                                            "}\n"
                                            "QPushButton:hover:!pressed{\n"
                                            "border:1px solid rgb(170, 0, 255);\n"
                                            "}\n"
                                            "\n"
                                            "")

    def choosenTranslator(self, i):
        self.translator = i
    
    def backgroundColor(self, i):
        self.im.bg = i
    
    def orgLang(self, i):
        self.orgLanguage = i

    def textColors(self, i):
        self.im.textColor = i

    def chooseRange(self, i):
        self.range = i
        self.rangeLabel.setText(f"Range: {self.range}px")
    
    def chooseFontNumber(self, i):
        self.im.fontNum = i
        self.label_4.setText(f"Font Size: {self.im.fontNum}")

    def showCombN (self, i):
        if i == 0:
            self.combineN = False
            self.rangeSlider.setEnabled(False)
        else:
            self.combineN = True
            self.rangeSlider.setEnabled(True)

    def showCombO (self, i):
        if i == 0:
            self.combineO = False
        else:
            self.combineO = True

    def getCurr(self, i):
        if i != 0:
            self.single = True
        else:
            self.single = False

    def clear(self):
        self.im.pages.clear()
        self.im.connectDict.clear()
        self.im.translated.clear()
        self.im.japanese.clear()
        self.files.clear()
        self.recycle.clear()
        self.num = -1
        self.index = 0
        self.im.img = None
        self.im.setPixmap(QPixmap("Icons\pure-white-background-85a2a7fd.jpg"))

    def undo(self):
        lastRect = self.im.img
        if self.im.pages != {} and self.im.pages[lastRect] != []:
            if lastRect not in self.recycle:
                self.recycle[lastRect] = [self.im.pages[lastRect][-1]]
            else:
                self.recycle[lastRect].append(self.im.pages[lastRect][-1])
            if self.im.pages[lastRect] != []:
                del self.im.pages[lastRect][-1]
    
    def redo(self):
        lastRect = self.im.img
        if  self.recycle != {} and self.recycle[lastRect] != []:
            self.im.pages[lastRect].append(self.recycle[lastRect][self.num])
            self.num -= -1
        
    def linkUpload(self):
        if self.files != [] and self.isClicked:
            self.isClicked = False
            self.index = 0
            self.changeTranslation.clear()
        if self.setting.downLoad == "":
            directory = QFileDialog.getExistingDirectory(self, 'Select a directory')
            self.setting.updateSetting("Paths", "Download", directory)
            self.setting.getUpdateInfo()
            self.ui.deeplKey.setText(directory)
        try:
            if self.setting.consumer_key == "None" or self.setting.consumer_secret == "None" or self.setting.access_token == "None" or self.setting.access_token_secret == "None" or self.setting.bearer_token == "None":
                self.Form.show()
                loop = QEventLoop()
                self.Form.destroyed.connect(loop.quit)
                loop.exec()
                print("finished")
            self.setting.getUpdateInfo()
            link = self.linkBar.text()
            twitter = Twitter()
            images = twitter.getImageUrl(link)
            self.files = twitter.download(images)
            if self.files != []:
                self.im.img = self.files[0]
            self.showImage()
            self.linkBar.clear()
        except:
            logger.exception("Not Downloadable")



    def upload1(self):
        filenames, _ =  QFileDialog.getOpenFileNames(
            None,
            "QFileDialog.getOpenFileNames()",
            "",
            "Image files (*.jpg *.png)"
        )
        if filenames != []:
            if self.files != [] and self.isClicked:
                self.files.clear()
                self.index = 0
                self.isClicked = False
                self.im.pages.clear()
                self.im.japanese.clear()
                self.im.translated.clear()
                self.im.connectDict.clear()
                self.recycle.clear()
                self.num = -1
                self.handling.deleteFiles(self.setting.Translated)
            for file in filenames:
                self.files.append(file)
            if self.files != []:
                self.im.img = self.files[0]
                if self.isSort:
                    self.files.sort()
                self.showImage()
            if self.isClicked == False:
                self.translatedFiles.clear()
                self.saveButton.hide()
                self.changeTranslation.clear()
                self.newIndex = 0

    def saveImages(self):
        if self.translatedFiles == [] and not self.im.flag:
            pass
        elif self.translatedFiles != [] and not self.im.flag:
            filename = QFileDialog.getSaveFileName(self, 'Save File')
            imgDirectory = []
            num = 0
            for img in self.translatedFiles:
                image = ImageQt.fromqimage(img)
                imgName = f"Translated\img{num}.jpg"
                imgDirectory.append(imgName)
                image.save(imgName)
                num += 1
            with open((filename[0]+".pdf"), "wb") as f:
                f.write(img2pdf.convert(imgDirectory))
        else:
            filename = QFileDialog.getSaveFileName(self, 'Save File')
            imgDirectory = []
            pageCopy = self.im.scaledDict
            nums = 0
            for img in pageCopy:
                try:
                    num = 0
                    pix = QPixmap(img)
                    qp = QtGui.QPainter(pix)
                    qp.setPen(QPen(self.im.color[self.im.textColor], 2, Qt.SolidLine))
                    qp.drawPixmap(pix.rect(), pix)
                    qp.drawRects(self.im.scaledDict[img])
                    for index, words in enumerate(self.im.translated[self.im.connectDict[img]]):
                        qp.fillRect(self.im.scaledDict[img][index], self.im.color[self.im.bg])
                        qp.setFont(QFont("times",self.im.fontNum * 2))
                        qp.drawText(self.im.scaledDict[img][index], words, option=QTextOption())
                    imName = f"Translated\Truetrans{nums}.jpg"
                    imgDirectory.append(imName)
                    pix.save(imName)
                    nums += 1
                    qp.end()
                except:
                    logger.exception("Something went wrong!")
            with open((filename[0]+".pdf"), "wb") as f:
                f.write(img2pdf.convert(imgDirectory))

    def moveRight(self):
        if self.isClicked and not self.im.flag:
            if self.newIndex >= len(self.translatedFiles)-1:
                self.newIndex = len(self.translatedFiles)-1
            else:
                self.newIndex += 1
        else:
            if self.index >= len(self.files)-1:
                self.index = len(self.files)-1
            else:
                self.index += 1
        if self.files != []:
            self.showImage()
            self.drawOnPages()
        
    def moveLeft(self):
        if self.isClicked and not self.im.flag:
            if self.newIndex <= 0:
                self.newIndex = 0
            else:
                self.newIndex -= 1
        else:
            if self.index <= 0:
                self.index = 0
            else:
                self.index -= 1
        if self.files != []:
            self.showImage()
            self.drawOnPages()

    def drawOnPages(self):
        if self.im.flag and self.files != []:
            currentP = self.files[self.index]
            if currentP not in self.im.pages:
                self.im.img = currentP
                self.im.pages[currentP] = []
            else:
                self.im.img = currentP

    @logger.catch
    def showImage(self):
        if self.isClicked:
            if not self.im.flag:
                self.saveButton.show()
                im = self.translatedFiles[self.newIndex]
                pix = QPixmap(im)
                self.im.setPixmap(pix)
            else:
                self.drawOnPages()
                im = self.files[self.index]
                pix = QPixmap(im)
                self.im.image = pix
                self.saveButton.show()
        else:
            pix = QPixmap(self.files[self.index])
            self.im.image = pix
            size = pix.size()
            self.clearButton.show()
            if size.width() > size.height():
                self.imageWidget.setMaximumSize(QtCore.QSize(990,680))
            else:
                self.imageWidget.setMaximumSize(QtCore.QSize(700,800))
            if not self.im.flag:
                self.im.setPixmap(self.im.image)
            self.drawOnPages()

    def afterThread(self, translated):
        self.isClicked = True
        self.translatedFiles = translated
        self.index = 0
        self.newIndex = 0
        QtCore.QTimer.singleShot(0, self.showImage)
        print("THREAD COMPLETE!")

    def singleAfterThread(self, page):
        self.translatedFiles[self.newIndex] = page
        QtCore.QTimer.singleShot(0, self.showImage)
        print("THREAD COMPLETE!")

    def manualAfterThread(self, e):
        self.isClicked = True
        QtCore.QTimer.singleShot(0, self.showImage)
        self.im.connectDict = e[0]
        self.im.translated = e[1]
        self.im.japanese = e[2]
        self.im.scaledDict = e[3]
        self.index = 0
        self.newIndex = 0
        print("THREAD COMPLETE!")
    
    def manualRetranslate(self, e):
        self.im.translated = e
        print("THREAD COMPLETE!")
    
    def changeProgress(self, status):
        self.bar.setValue(status)

    def showProgress(self):
        if self.files != []:
            self.bar.setVisible(True)
            self.translate.setEnabled(False)

    def hideProgress(self):
        self.bar.setVisible(False)
        self.bar.setValue(0)
        self.translate.setEnabled(True)


    def translate1(self):
        self.clearButton.hide()
        if self.files == []:
            pass
        elif self.im.flag and self.im.connectDict == {} and self.im.translated == {}:
            logger.info("Manual Translation")
            print(self.im.pages)
            self.worker = ManualTranslation(self.im.pages, self.ocr, self.translator, self.im.width(), self.im.height())
            self.worker.signals.result.connect(self.manualAfterThread)
            self.worker.signals.finished.connect(self.hideProgress)
            self.worker.signals.progress.connect(self.changeProgress)
            self.thread.start(self.worker)
        elif self.im.flag and self.im.connectDict != {} and self.im.translated != {}:
            self.worker = ManualTranslation(self.im.japanese, self.ocr, self.translator, self.im.width(), self.im.height(), True)
            self.worker.signals.result.connect(self.manualRetranslate)
            self.worker.signals.finished.connect(self.hideProgress)
            self.worker.signals.progress.connect(self.changeProgress)
            self.thread.start(self.worker)
        elif self.single and self.isClicked:
            logger.info("Translating current page!")
            self.worker = SingleTranslate(self.files[self.newIndex], self.ocr, self.translator, self.combineN, self.combineO, self.range, self.orgLanguage)
            self.worker.signals.result.connect(self.singleAfterThread)
            self.worker.signals.finished.connect(self.hideProgress)
            self.worker.signals.progress.connect(self.changeProgress)
            self.thread.start(self.worker)

        elif self.checkthing != [] and self.changeTranslation != [] and self.checkthing[1] == self.combineN and self.checkthing[2] == self.combineO and self.checkthing[3] == self.range:
            logger.info(f"Using {self.translator}!")
            self.worker = Retranslate(self.changeTranslation, self.translator, self.orgLanguage)
            self.worker.signals.result.connect(self.afterThread)
            self.worker.signals.finished.connect(self.hideProgress)
            self.worker.signals.progress.connect(self.changeProgress)
            self.thread.start(self.worker)
        else:
            logger.info("Manga Translation")
            self.worker = Translate(self.files, self.ocr, self.translator, self.combineN, self.combineO, self.range)
            self.worker.signals.result.connect(self.afterThread)
            self.worker.signals.stored.connect(self.changeTrans)
            self.worker.signals.booleans.connect(self.changeCheckThing)
            self.worker.signals.finished.connect(self.hideProgress)
            self.worker.signals.progress.connect(self.changeProgress)
            self.worker.signals.lang.connect(self.orgLang)
            self.thread.start(self.worker)


if __name__ == "__main__":
    import sys
    app =QtWidgets.QApplication(sys.argv)
    w = interact()
    w.show()
    sys.exit(app.exec())
