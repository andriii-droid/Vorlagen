from reportlab.lib.pagesizes import A6
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import math


class Pattern:
    def __init__(self, filename='output', circles=False, lines=False, sketch=False):
        self.circles = circles
        self.lines = lines
        self.sketch = sketch
        self.c = canvas.Canvas(filename, pagesize=A6)
        self.width, self.height = A6
        self.center = (self.width / 2 , self.height / 2)

        if self.circles:
            self.c.circle(*self.center, r=3, stroke=0, fill=1)

    def generate_shape(self, shape="rect", num_shapes=1,  col='#000000',  size=100, offset=1):
        self.col = col
        self.size = size
        self.offset = offset
        self.c.setFillColor(col)
        angle = 0
        step = 360 / num_shapes
        for _ in range(num_shapes):
            if angle == 0 and self.sketch:
                self.c.setLineWidth(1)
                self.c.setStrokeColor(colors.red)
            else:
                self.c.setLineWidth(.2)
                self.c.setStrokeColor(col)

            if shape == "rect":
                self.draw_square(angle)
            elif shape == "tri":
                self.draw_triangle(angle)
            elif shape == "pent":
                self.draw_pentagon(angle)
            elif shape == "line":
                self.draw_line(angle)
            elif shape == "shape":
                self.make_shape(angle=angle, center=self.center)
            else:
                print(f"No Shape with the Name: {self.shape}")
                break
                
            angle += step   

    def savePDF(self):
        self.c.showPage()
        self.c.save()

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
    
    def make_shape(self, center, angle=0, num_points=1):
        points = []
        points.append(self.new_point(center, (self.size/2)*self.offset, 90+angle))
        if self.circles:
            self.c.circle(*points[-1], r=1, stroke=0, fill=1) 
        rotation_angle = -360/num_points/2 + angle
        for _ in range(num_points - 1):
            points.append(self.new_point(points[-1], self.size*math.sin(math.pi/num_points), rotation_angle)) #TODO
            if self.circles:
                self.c.circle(*points[-1], r=1, stroke=0, fill=1)
            if self.lines or (self.sketch and angle==0):
                self.c.line(*points[-2], *points[-1])
            rotation_angle -= 360/num_points
        if self.lines or (self.sketch and angle==0):
            self.c.line(*points[0], *points[-1])

        return points