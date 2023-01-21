import math 
from pprint import pprint
        
class Overlap:
    def __init__(self, x1, y1, x2, y2, id):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.id = id
        
    def combine(self, other):
        x1 = min(self.x1, other.x1)
        y1 = min(self.y1, other.y1)
        x2 = max(self.x2, other.x2)
        y2 = max(self.y2, other.y2)
        id = self.id + "-" + other.id
        return Overlap(x1, y1, x2, y2, id)
    
    def is_overlap(self, other):
        if (self.x1 < other.x2) and (self.x2 > other.x1) and (self.y1 < other.y2) and (self.y2 > other.y1):
            return True
        else:
            return False

def combine_overlapping_rectangles(rectangles):
    combined_rectangles = {}
    for id, rectangle in rectangles.items():
        combined = False
        for other_id, other_rectangle in combined_rectangles.items():
            if rectangle.is_overlap(other_rectangle):
                new_rectangle = rectangle.combine(other_rectangle)
                combined_rectangles.pop(other_id)
                combined_rectangles[new_rectangle.id] = new_rectangle
                combined = True
                break
        if not combined:
            combined_rectangles[rectangle.id] = rectangle
    return reFormat(combined_rectangles)

class Combine:
    def __init__(self, x1, y1, x2, y2, id):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.id = id

    def distance_to(self, other):
        x_distance = abs(self.x1 - other.x1)
        y_distance = abs(self.y1 - other.y1)
        return math.sqrt(x_distance**2 + y_distance**2)

    def combine(self, other):
        x1 = min(self.x1, other.x1)
        y1 = min(self.y1, other.y1)
        x2 = max(self.x2, other.x2)
        y2 = max(self.y2, other.y2)
        id = self.id + "-" + other.id
        return Combine(x1, y1, x2, y2, id)

def combine_rectangles(rectangles, distance_threshold):
    combined_rectangles = {}
    for id, rectangle in rectangles.items():
        combined = False
        for other_id, other_rectangle in combined_rectangles.items():
            if rectangle.distance_to(other_rectangle) < distance_threshold:
                new_rectangle = rectangle.combine(other_rectangle)
                combined_rectangles.pop(other_id)
                combined_rectangles[new_rectangle.id] = new_rectangle
                combined = True
                break
        if not combined:
            combined_rectangles[rectangle.id] = rectangle
    return reFormat(combined_rectangles)

def reFormat(dictionary):
    newformat = {}
    for z in dictionary:
        newformat[z] = [(dictionary[z].x1, dictionary[z].y1), (dictionary[z].x2, dictionary[z].y2)]
    return newformat

def rectanglesCO(newDt, s):
    newM = {}
    for name in newDt:
        m = newDt[name]
        if s == 'c':
            newM[name] = Combine(m[0][0], m[0][1], m[1][0], m[1][1], name)
        else:
            newM[name] = Overlap(m[0][0], m[0][1], m[1][0], m[1][1], name)
    return newM


