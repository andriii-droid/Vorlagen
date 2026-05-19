from reportlab.lib.pagesizes import A6
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import math
from Point import Point


class Pattern:
    def __init__(self, filename='output', circles=False, lines=False, sketch=False):
        self.circles = circles
        self.lines = lines
        self.sketch = sketch
        self.c = canvas.Canvas(filename, pagesize=A6)
        self.width, self.height = A6
        self.center = Point(self.width / 2 , self.height / 2)


        if self.circles:
            self.c.circle(*self.center.cartesian, r=3, stroke=0, fill=1)

    def savePDF(self):
        self.c.showPage()
        self.c.save()

    def draw_points(self, points):
        for p1, p2 in zip(points, points[1:]+[points[0]]):
            if self.circles:
                self.c.circle(*p1.cartesian, r=1, stroke=0, fill=1)

    def draw_lines(self, points, angle, offset):
        for count, (p1, p2) in enumerate(zip(points, points[offset+2:]+points[0:offset+2])):
            if self.lines or(self.sketch and angle == 0 and not (offset)) or (self.sketch and offset and count == 0):
                self.c.line(*p1.cartesian, *p2.cartesian)
