from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRunnable, pyqtSignal, QObject, QRectF, QPointF
import numpy as np
from TranslateManga import Translate
import cv2
from pprint import pprint
from deep_translator import MyMemoryTranslator
import deepl
import langid
from FileHandling import FileHandler
from Configer import Settings
from loguru import logger
from PIL import Image
import ast
from Translation import MangaBag
try:
    import translators.server as ts
except ModuleNotFoundError:
    import translators as ts

class Worker(QObject):
    result = pyqtSignal(object)
    finished = pyqtSignal()
    progress = pyqtSignal(int)

class ManualTranslation(QRunnable):
    def __init__(self, dictionary, mocr, translator, language, width, height, retranslate=False):
        super(ManualTranslation, self).__init__()
        self.manualRect = dictionary
        self.mocr = mocr
        self.translator = translator
        self.width = width
        self.height = height
        self.source = None if language == "auto" else language
        self.dictionary = {}
        self.signals = Worker()
        self.portions = (100)/3
        self.cnt = 0
        self.handling = FileHandler()
        self.setting = Settings()
        self.retrans = retranslate
        self.scaleDict = {}
        self.cohere = MangaBag()

    def scaleRect(self, img1, width, height, scalelist):
        scaleDict = scalelist[:]
        imageToPredict = cv2.imread(img1, 3)
        targetSizeX = width
        targetSizeY = height
        y_ = imageToPredict.shape[0]
        x_ = imageToPredict.shape[1]

        x_scale = targetSizeX / x_
        y_scale = targetSizeY / y_
        img = cv2.resize(imageToPredict, (targetSizeX, targetSizeY))
        img = np.array(img)

        for index, value in enumerate(scaleDict):
            x, y, w, h = value.getRect()
            (origLeft, origTop, origRight, origBottom) = (x, y, x+w, y+h)

            x = int(np.round(origLeft * x_scale))
            y = int(np.round(origTop * y_scale))
            xmax = int(np.round(origRight * x_scale))
            ymax = int(np.round(origBottom * y_scale))
            scaleDict[index] = (x, y, xmax, ymax)
        return scaleDict
        
    def crop(self, formatted):
        formattedDict = formatted.copy()
        newDict = {}
        num = 0
        page = 0
        for img in formattedDict:
            newList = []
            pix = QPixmap(img)
            canvas = pix.scaled(self.width, self.height)
            name1 = f"Translated\\manaul{page}.jpg"
            canvas.save(name1)
            formattedDict[img] = self.scaleRect(name1, pix.width(), pix.height(), formattedDict[img])
            self.dictionary[img] = name1
            newDict[name1] = newList
            page += 1

        self.scaleDict = formattedDict.copy()
        for key in self.scaleDict:
            newList = self.scaleDict[key][:]
            for index, value in enumerate(newList):
                x1, y1, x2, y2 = value
                newList[index] = QRectF(QPointF(x1, y1), QPointF(x2, y2))
            self.scaleDict[key] = newList

        for imx in formattedDict:
            for x in formattedDict[imx]:
                try:
                    name = f"cropText\\manualRect{num}.jpg"
                    image = cv2.imread(imx)
                    x1, y1, x2, y2 = x
                    crop = image[y1:y2, x1:x2]
                    cv2.imwrite(name, crop)
                except:
                    continue
                newDict[self.dictionary[imx]].append(name)
                num += 1

        return newDict
    
    def get_text(self, mocr, diction):
        dict1 = {}
        for x in diction:
            list1 = []
            for y in diction[x]:
                try:
                    img = Image.open(y)
                    text = mocr(img)
                    list1.append(text)
                except:
                    text = " "
                    list1.append(text)
                    # logger.exception("Failed OCR!")
                    logger.info(f"{x} -> {y}")
            dict1[x] = list1
        return dict1

    
    def translate(self, original, name, langauge):
        newDict = {}
        if original == {}:
            return {}
        source = langauge
        # print(source)
        if name == "DeepL":
            for key in original:
                h = []
                for jap in original[key]:
                    t = deepl.translate(source_language="JA", target_language="EN", text=jap)
                    h.append(t)
                newDict[key] = h
                if self.retrans:
                    self.cnt += self.portions
                    self.signals.progress.emit(self.cnt)
        elif name == "MyMemory":
            for key in original:
                h = []
                for jap in original[key]:
                    t = MyMemoryTranslator(source="ja", target='en').translate(jap)
                    h.append(t)
                newDict[key] = h
                if self.retrans:
                    self.cnt += self.portions
                    self.signals.progress.emit(self.cnt)
        elif name == "Google":
            for key in original:
                h = []
                for jap in original[key]:
                    t = str(ts.google(jap))
                    h.append(t)
                newDict[key] = h
                if self.retrans:
                    self.cnt += self.portions
                    self.signals.progress.emit(self.cnt)
        elif name == "Bing":
            for key in original:
                h = []
                for jap in original[key]:
                    t = str(ts.bing(jap))
                    h.append(t)
                newDict[key] = h
                if self.retrans:
                    self.cnt += self.portions
                    self.signals.progress.emit(self.cnt)
        elif name == "Youdao":
            for key in original:
                h = []
                for jap in original[key]:
                    t = str(ts.youdao(jap))
                    h.append(t)
                newDict[key] = h
                if self.retrans:
                    self.cnt += self.portions
                    self.signals.progress.emit(self.cnt)
        elif name == "Cohere":
            for key in original:
                newDict[key] = self.manaul_cohere(original[key])
            if self.retrans:
                    self.cnt += self.portions
                    self.signals.progress.emit(self.cnt)
        return newDict
    
    def manaul_cohere(self, need_translate):
        
        counter = 1
        japanese_text = {}
        for jap in need_translate:
            japanese_text[f'image{counter}'] = jap
            counter += 1

        translation_request = f"""
                    translate the following japanese text, extracted from a manga, with as much context as you can gather from the other japanese text
                    and from any other context you can gather.
                    Return in the format you received with the english translation:
                    {japanese_text}
                    DO NOT ADD ANY ELSE. ONLY RETURN THE FORMAT I ASKED YOU TO.
                    MAKE SURE THE NUMBER OF LINES OF YOUR OUTPUT IS EQUAL TO THE INPUT I GIVE YOU.
                    Make sure the output is in the correct syntax so it can be converted to a dictionary using ast.literal_eval().
                    Make sure it won't cause a keyError. I want the key of the return dictionalry to have double quotes in stead of single quotes.
                    """

        result = self.cohere.call_cohere(translation_request)
        try:
            final = ast.literal_eval(result)
            # print(final)
        except SyntaxError:
            logger.error("SYNTAX ERROR!!!")
            final = {}
            for key in japanese_text:
                context = f"""
                Use the following extracted from a manga as context to translate a sentence.
                context:
                japanese text :{japanese_text}\n
                Sentence to translate: {japanese_text[key]}
                RETURN only the translated sentence nothing else.
                """
                final[key] = self.call_cohere(context)


        if len(final) < len(japanese_text):
            logger.error("KEY ERROR!!!")
            for jt in japanese_text:
                if jt not in final:
                    fix_key = f"""
                    Translate the following line to english.
                    sentence to translate: {japanese_text[jt]}
                    use the text below as context to help you translate:
                    {final}
                    Return only the translated sentence. nothing else
                    """
                    final[jt] = self.call_cohere(fix_key)

                    
        array = []
        for key, value in final.items():
            array.append(value)
        return array
        


    
    def formatDict(self):
        num = 0
        listDict = {}
        for x in self.manualRect:
            newDict = {}
            for value in self.manualRect[x]:
                a, b, c, d = value.getRect()
                newDict[f"image{num}"] = [(a, b), (c, d)]
                num += 1
            listDict[x] = newDict
        return listDict
    
    @logger.catch
    def run(self):
        if self.retrans:
            # pprint(self.manualRect)
            if self.source == None and self.manualRect != {}:
                for x in list(self.manualRect.values()):
                    if x != []:
                        self.source = langid.classify(x[0])[0]
                        break
            translated = self.translate(self.manualRect, self.translator, self.source)
            # pprint(translated)
            self.signals.result.emit(translated)
            self.signals.finished.emit()
        else:
            try:
                cropText = self.crop(self.manualRect)
                self.cnt += self.portions
                self.signals.progress.emit(self.cnt)

                # pprint(self.dictionary)
                pprint(cropText)
                japanese = self.get_text(self.mocr, cropText)
                self.cnt += self.portions
                self.signals.progress.emit(self.cnt)

                pprint(japanese)
                if self.source == None and japanese != {}:
                    for x in list(japanese.values()):
                        if x != []:
                            self.source = langid.classify(x[0])[0]
                            break
                translated = self.translate(japanese, self.translator, self.source)
                pprint(translated)
            except:
                self.signals.result.emit("ERROR")
                self.signals.finished.emit()
            else:
                self.cnt += self.portions
                self.signals.progress.emit(self.cnt)
                self.handling.deleteFiles(self.setting.cropText)
                self.signals.result.emit((self.dictionary, translated, japanese, self.scaleDict))
                self.signals.finished.emit()