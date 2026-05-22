from reportlab.lib.pagesizes import A6
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from Point import Point


class Pattern:
    '''implemets Functions to draw Points and Lines and creates a canvas'''
    def __init__(self, filename='output', circles=False, lines=False, sketch=False, cord=False):
        '''Creates a Pattern Instance, which creates a pdf canvas'''
        self.circles = circles
        self.lines = lines
        self.sketch = sketch
        self.c = canvas.Canvas(filename, pagesize=A6)
        self.width, self.height = A6
        self.center = Point(self.width / 2 , self.height / 2)

        self.draw_points([self.center], r=2) #Draw the Center Point

        #Draw lines on the Edge of PDF
        self.draw_lines([Point(0,0), Point(self.width, 0), Point(self.width, self.height), Point(0, self.height)],
                         angle=0, offset=-1)
        if cord:    #Draw coordinate System
            self.c.setLineWidth(.05)
            self.c.setStrokeColor(colors.gray)
            self.c.circle(*self.center.cartesian, r=50, stroke=1, fill=0)
            self.c.circle(*self.center.cartesian, r=100, stroke=1, fill=0)
            self.c.circle(*self.center.cartesian, r=25, stroke=1, fill=0)
            startx = Point(x=0, y=self.center.cartesian[1])
            endx = Point(x=self.width, y=self.center.cartesian[1])
            self.c.line(*startx.cartesian, *endx.cartesian)
            starty = Point(x=self.center.cartesian[0], y=0)
            endy = Point(x=self.center.cartesian[0], y=self.height)
            self.c.line(*starty.cartesian, *endy.cartesian)

    def savePDF(self):
        '''Saves the PDF'''
        self.c.showPage()
        self.c.save()

    def draw_points(self, points, r=1):
        '''Draws the given Points onto the PDF'''
        for p1 in points:
            if self.circles:
                self.c.circle(*p1.cartesian, r=r, stroke=0, fill=1)

    def draw_lines(self, points, angle, offset):
        '''Draws Lines between the given Points
        if offset = -1 the Lines are drawn between zhe consecutive points in the array,
        otherwise offset+1 Points in the array gets skipped'''
        for count, (p1, p2) in enumerate(zip(points, points[offset+2:]+points[0:offset+2])):
            if self.lines or(self.sketch and angle == 0 and not (offset)) or (self.sketch and offset and count == 0):
                self.c.setLineWidth(.2)
                self.c.line(*p1.cartesian, *p2.cartesian)
