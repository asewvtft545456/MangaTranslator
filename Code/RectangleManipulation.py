
class Rectangles:

    def combineOverlap(self, rectDict):
        secDic = rectDict.copy()
        delete = []
        trueDel = []
        for rect in rectDict:
            x1 = rectDict[rect][0][0]
            y1 = rectDict[rect][0][1]
            x2 = rectDict[rect][1][0]
            y2 = rectDict[rect][1][1]
            if rect in delete:
                continue
            for key in secDic:
                bx1 = secDic[key][0][0]
                by1 = secDic[key][0][1]
                bx2 = secDic[key][1][0]
                by2 = secDic[key][1][1]
                if rect == key:
                    continue
                else:
                    if x1 < bx2 and x2 > bx1 and y1 < by2 and y2 > by1:
                        # print(rect, "\t", key)
                        rectDict[rect] = self.combineBoundingBox((x1, y1, x2, y2), (bx1, by1, bx2, by2))
                        delete.append(key)
                        delete.append(rect)
                        trueDel.append((rect, key))
        # print(trueDel)
        for x, y in trueDel:
            try:
                if abs(rectDict[x][0][0]-rectDict[x][1][0]) > abs(rectDict[y][0][0]-rectDict[y][1][0]) or abs(rectDict[x][0][1]-rectDict[x][1][1]) > abs(rectDict[y][0][1]-rectDict[y][1][1]):
                    del rectDict[y]
                else:
                    del rectDict[x]
            except:
                continue
        return rectDict

    def neighborRect(self, rectDict, num):
        secDic = rectDict.copy()
        delete = []
        trueDel = []
        rangeNum = num
        for rect in rectDict:
            x1 = rectDict[rect][0][0]
            y1 = rectDict[rect][0][1]
            x2 = rectDict[rect][1][0]
            y2 = rectDict[rect][1][1]
            if rect in delete:
                continue
            for key in secDic:
                bx1 = secDic[key][0][0]
                by1 = secDic[key][0][1]
                bx2 = secDic[key][1][0]
                by2 = secDic[key][1][1]
                if rect == key:
                    continue
                else:
                    if x1 < bx2 and x2 < bx1 and abs(x2-bx1)<rangeNum and y1 < by2 and y2 > by1:
                        # print("x2-bx1=" + str(x2-bx1))
                        # print(rect)
                        rectDict[rect] = self.combineNeighboringBox((x1, y1, x2, y2), (bx1, by1, bx2, by2))
                        delete.append(key)
                        delete.append(rect)
                        trueDel.append((rect, key))
                    elif x1 < bx2 and x2 > bx1 and y1 < by2 and y2 < by1 and abs(y2-by1) < rangeNum:
                        # print("y2-by1= "+ str(y2-by1))
                        # print(rect)
                        rectDict[rect] = self.combineNeighboringBox((x1, y1, x2, y2), (bx1, by1, bx2, by2))
                        delete.append(key)
                        delete.append(rect)
                        trueDel.append((rect, key))
                    elif x1 > bx2 and abs(x1 - bx2)< rangeNum and x2 > bx1 and y1 < by2 and y2 > by1:
                        # print("x1 - bx2= "+str(x1 - bx2))
                        # print(rect)
                        rectDict[rect] = self.combineNeighboringBox((x1, y1, x2, y2), (bx1, by1, bx2, by2))
                        delete.append(key)
                        delete.append(rect)
                        trueDel.append((rect, key))
                    elif x1 < bx2 and x2 > bx1 and y1 > by2 and abs(y1 - by2) < rangeNum and y2 > by1:
                        # print("y1-by2= " + str(y1 - by2))
                        # print(rect)
                        rectDict[rect] = self.combineNeighboringBox((x1, y1, x2, y2), (bx1, by1, bx2, by2))
                        delete.append(key)
                        delete.append(rect)
                        trueDel.append((rect, key))
        # print(trueDel)
        for x, y in trueDel:
            try:
                if abs(rectDict[x][0][0]-rectDict[x][1][0]) > abs(rectDict[y][0][0]-rectDict[y][1][0]) or abs(rectDict[x][0][1]-rectDict[x][1][1]) > abs(rectDict[y][0][1]-rectDict[y][1][1]):
                    del rectDict[y]
                else:
                    del rectDict[x]
            except:
                continue
        return rectDict

    def combineBoundingBox(self, box1, box2):
        x = min(box1[0], box2[0])
        y = min(box1[1], box2[1])
        w = max(box2[0] + box2[2] - box1[0], box1[0] + box1[2] - box2[0])
        h = max(box1[1] + box1[3], box2[1] + box2[3]) - y #max(box1[3], box2[3])
        return [(x, y), (w, h)]


    def combineNeighboringBox(self, box1, box2):
        x = min(box1[0], box2[0])
        y = min(box1[1], box2[1])
        w = max(box1[2], box2[2])
        h = max(box1[3], box2[3])
        return [(x, y), (w, h)]
        



