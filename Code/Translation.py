import cv2
import math
from deep_translator import MyMemoryTranslator
from loguru import logger
import time
import deepl
import os
import easyocr
from PIL import Image
from addText import add_text_to_image
try:
    import translators.server as ts
except ModuleNotFoundError:
    import translators as ts

class MangaBag:

    def chronos(func):
        def get_time(*args, **kawrgs):
            start = time.time()
            x = func(*args, **kawrgs)
            end = time.time()
            name = ""
            if "get_text" in str(func):
                name = "EasyOcr"
            elif "get_japanese" in str(func):
                name = "MangaOcr"
            else:
                name = "Translator"
            logger.info("{} took {} seconds".format(name, (end-start)))
            return x
        return get_time
    
    def getFontSizeThickness(self,img):
        FONT_SCALE = 6e-4  # Adjust for larger font size in all images
        THICKNESS_SCALE = 5e-4  # Adjust for larger thickness in all images

        img = cv2.imread(img)
        height, width, _ = img.shape

        font_scale = min(width, height) * FONT_SCALE
        thickness = math.ceil(min(width, height) * THICKNESS_SCALE)
        return (font_scale, thickness)
    
    def get_japanese(self, image, mocr, diction, direct):
        if diction == {}:
            return {}
        newList = {}
        et = {}
        ts = {}
        directory = direct
        tt = []
        for x in diction:
            cropped_image = image[abs(diction[x][0][1]):abs(diction[x][1][1]), abs(diction[x][0][0]):abs(diction[x][1][0])]
            try:
                cv2.imwrite(os.path.join(directory, str(x)+'.jpg'), cropped_image)
            except:
                logger.exception("Failed cropping!")
            et[str(x)] = os.path.join(directory, str(x)+'.jpg')
        for root, dirs, files in os.walk(directory):
            for x in files:
                try:
                    img = Image.open((root+"\\"+ x).strip())
                    text = mocr(img)
                    ts[(root+"\\"+ x).strip()] = text
                except:
                    logger.exception("File Mystery")
        mg = et.items()
        tg = ts.items()
        for coor, direct in mg:
            for dir1, jap in tg:
                if direct == dir1:
                    newList[coor] = jap
        return newList

    def get_text(self, image):
        reader = easyocr.Reader(['ja'], gpu=False) 
        result = reader.readtext(image, paragraph=True, x_ths=.01, y_ths=.01)
        myDict = {}
        num = 0
        for (bbox, text) in result: 
            (tl, tr, br, bl) = bbox
            tl = (int(tl[0]), int(tl[1]))
            tr = (int(tr[0]), int(tr[1]))
            br = (int(br[0]), int(br[1]))
            bl = (int(bl[0]), int(bl[1]))
            if tl[0] < 0 or tl[1] < 0:
                tl = (abs(tl[0]), abs(tl[1]))
            if br[0] < 0 or br[1] <0:
                br = (abs(br[0]), abs(br[1]))
            myDict[f"image{num}"] = ([tl , br ])
            num += 1
        secDic = myDict.copy()
        dupKey = []
        for rect in myDict: 
            for key in secDic:
                b = secDic[key]
                if myDict[rect] == b:
                    continue
                else:
                    if myDict[rect][0][0] >= b[0][0] and myDict[rect][0][1] >= b[0][1] and myDict[rect][1][0]<= b[1][0] and myDict[rect][1][1] <= b[1][1]:
                        dupKey.append(rect)
        for x in dupKey:
            try:
                del myDict[x]
            except:
                continue
        return myDict
    
    def translate(self, original, name, langauge):
        if original == {}:
            return {}
        source = langauge
        # print(source)
        try:
            if name == "DeepL":
                for key in original:
                    try:
                        original[key] = deepl.translate(source_language=source.upper(), target_language="EN", text=original[key])
                    except:
                        original[key] = MyMemoryTranslator(source=source, target='en').translate(original[key])
                return original
            elif name == "MyMemory":
                for key in original:
                    try:
                        original[key] = MyMemoryTranslator(source=source, target='en').translate(original[key])
                    except:
                        original[key] = deepl.translate(source_language=source.upper(), target_language="EN", text=original[key])
                return original
            elif name == "Google":
                for jap in original:
                    try:
                        original[jap] = str(ts.google(original[jap]))
                    except:
                        original[jap] = str(ts.bing(original[jap]))
                return original
            elif name == "Bing":
                for jap in original:
                    try:
                        original[jap] = str(ts.bing(original[jap]))
                    except:
                        original[key] = deepl.translate(source_language=source.upper(), target_language="EN", text=original[key])
                return original
            elif name == "Youdao":
                for jap in original:
                    try:
                        original[jap] = str(ts.youdao(original[jap]))
                    except:
                        original[key] = deepl.translate(source_language=source.upper(), target_language="EN", text=original[key])
                    time.sleep(5)
                return original
        except ConnectionError:
                return "ConnectionError"
    
    def segment(self, list1):
        if list1 == {}:
            return {}
        for line in list1:
            newL= list(str(list1[line]))
            s = ''
            count = 0
            if newL.count(" ")  > 3:
                for x in range(len(newL)):
                        if newL[x] == " ":
                            count += 1
                        if count == 2:
                            newL[x] = "\n"
                            count = 0
                        s += newL[x]
            else:
                for x in range(len(newL)):
                        if newL[x] == " ":
                            newL[x] = "\n"
                            count = 0
                        s += newL[x]
            list1[line] = s
        return list1
    
    def write(self, img, dict1, list1, font, thick):
        if dict1 == {}:
            return img
        for value in dict1:
            try:
                cv2.rectangle(img, dict1[value][0], dict1[value][1], (0, 255, 255), 2)
                image = add_text_to_image(
                    img,
                    list1[value],
                    font_color_rgb=(255, 0, 0),
                    top_left_xy=(dict1[value][0][0], dict1[value][0][1]),
                    font_scale= font,
                    font_face=cv2.FONT_HERSHEY_DUPLEX,
                    bg_color_rgb=(255, 255, 255),
                    font_thickness=thick
                    )
            except:
                logger.exception("Mystery")
                continue
        return image