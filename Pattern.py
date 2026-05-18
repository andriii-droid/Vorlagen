from reportlab.lib.pagesizes import A6
from reportlab.lib import colors
import math


class Pattern:
    def __init__(self, shape="rect", num_shapes=1, size=100, can=None, circles=False, lines=False, col='#000000', offset=1, sketch=False):
        self.shape = shape
        self.num_shapes = num_shapes
        self.size = size
        self.c = can
        self.width, self.height = A6
        self.center = (self.width / 2 , self.height / 2)
        self.circles = circles
        self.lines = lines
        self.col = col
        self.offset = offset
        self.sketch = sketch

        self.generate_shape()
        if self.circles:
            self.c.circle(*self.center, r=3, stroke=0, fill=1)


    def generate_shape(self):
        self.c.setFillColor(self.col)
        angle = 0
        step = 360 / self.num_shapes
        for _ in range(self.num_shapes):
            if angle == 0 and self.sketch:
                self.c.setLineWidth(1)
                self.c.setStrokeColor(colors.red)
            else:
                self.c.setLineWidth(.2)
                self.c.setStrokeColor(self.col)

            if self.shape == "rect":
                self.draw_square(angle)
            elif self.shape == "tri":
                self.draw_triangle(angle)
            elif self.shape == "pent":
                self.draw_pentagon(angle)
            elif self.shape == "line":
                self.draw_line(angle)
            else:
                print(f"No Shape with the Name: {self.shape}")
                break
                
            angle += step   

    def draw_line(self, angle=0):
        points = []
        points.append(self.new_point(self.center, (self.size/2)*self.offset, 90+angle))
        if self.circles:
            self.c.circle(*points[-1], r=1, stroke=0, fill=1) 
        rotation_angle = angle + 270
        for _ in range(1):
            points.append(self.new_point(points[-1], self.size, rotation_angle))
            if self.circles:
                self.c.circle(*points[-1], r=1, stroke=0, fill=1)
            if self.lines or (self.sketch and angle==0):
                self.c.line(*points[-2], *points[-1])
            rotation_angle += 180
        if self.lines or (self.sketch and angle==0):
            self.c.line(*points[0], *points[-1])     

    def draw_square(self, angle=0):
        points = []
        points.append(self.new_point(self.center, (self.size/2)*self.offset, 225+angle))
        if self.circles:
            self.c.circle(*points[-1], r=1, stroke=0, fill=1) 
        rotation_angle = angle
        for _ in range(3):
            points.append(self.new_point(points[-1], self.size/2*2**0.5, rotation_angle))
            if self.circles:
                self.c.circle(*points[-1], r=1, stroke=0, fill=1)
            if self.lines or (self.sketch and angle==0):
                self.c.line(*points[-2], *points[-1])
            rotation_angle += 90
        if self.lines or (self.sketch and angle==0):
            self.c.line(*points[0], *points[-1])

    def draw_triangle(self, angle=0):
        points = []
        points.append(self.new_point(self.center, (self.size/2)*self.offset, 210+angle))
        if self.circles:
            self.c.circle(*points[-1], r=1, stroke=0, fill=1) 
        rotation_angle = angle
        for _ in range(2):
            points.append(self.new_point(points[-1], self.size*3/2/3**0.5, rotation_angle))
            if self.circles:
                self.c.circle(*points[-1], r=1, stroke=0, fill=1)
            if self.lines or (self.sketch and angle==0):
                self.c.line(*points[-2], *points[-1])
            rotation_angle += 120
        if self.lines or (self.sketch and angle==0):
            self.c.line(*points[0], *points[-1])

    def draw_pentagon(self, angle=0):
        points = []
        points.append(self.new_point(self.center, (self.size/2)*self.offset, 234+angle))
        if self.circles:
            self.c.circle(*points[-1], r=1, stroke=0, fill=1) 
        rotation_angle = angle
        for _ in range(4):
            points.append(self.new_point(points[-1], self.size*0.5877852523, rotation_angle))
            if self.circles:
                self.c.circle(*points[-1], r=1, stroke=0, fill=1)
            if self.lines or (self.sketch and angle==0):
                self.c.line(*points[-2], *points[-1])
            rotation_angle += 72
        if self.lines or (self.sketch and angle==0):
            self.c.line(*points[0], *points[-1])


    def new_point(self, start_point, length, angle_degrees):
        x1, y1 = start_point
        
        angle_radians = math.radians(angle_degrees)
        
        dx = length * math.cos(angle_radians)
        dy = length * math.sin(angle_radians)
        
        x2 = x1 + dx
        y2 = y1 + dy
        
        return (x2, y2)