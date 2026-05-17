import random
from reportlab.lib.pagesizes import A6
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import math
from pathlib import Path

class Pattern:
    def __init__(self, filename="output", shape="rect", num_shapes=1, size=100, can=None):
        self.shape = shape
        self.num_shapes = num_shapes
        self.size = size
        self.c = can
        self.width, self.height = A6
        self.center = (self.width / 2 , self.height / 2)
        self.generate_shape()
        self.c.circle(*self.center, r=3, stroke=0, fill=1)


    def generate_shape(self):
        self.c.setFillColor(colors.black)
        self.c.setStrokeColor(colors.royalblue)
        self.c.setLineWidth(.2)
        angle = 0
        step = 360 / self.num_shapes
        for _ in range(self.num_shapes):
            if self.shape == "rect":
                self.draw_square(angle)
            elif self.shape == "tri":
                self.draw_triangle(angle)
            else:
                print(f"No Shape with the Name: {self.shape}")
                break
                
            angle += step        

    def draw_square(self, angle=0):
        points = []
        points.append(self.new_point(self.center, self.size/2, 225+angle))
        self.c.circle(*points[-1], r=1, stroke=0, fill=1) 
        rotation_angle = angle
        for _ in range(3):
            points.append(self.new_point(points[-1], self.size/2*2**0.5, rotation_angle))
            self.c.circle(*points[-1], r=1, stroke=0, fill=1)
            self.c.line(*points[-2], *points[-1])
            rotation_angle += 90
        self.c.line(*points[0], *points[-1])

    def draw_triangle(self, angle=0):
        points = []
        points.append(self.new_point(self.center, self.size/2, 210+angle))
        self.c.circle(*points[-1], r=1, stroke=0, fill=1) 
        rotation_angle = angle
        for _ in range(2):
            points.append(self.new_point(points[-1], self.size*3/2/3**0.5, rotation_angle))
            self.c.circle(*points[-1], r=1, stroke=0, fill=1)
            self.c.line(*points[-2], *points[-1])
            rotation_angle += 120
        self.c.line(*points[0], *points[-1])


    def new_point(self, start_point, length, angle_degrees):
        x1, y1 = start_point
        
        angle_radians = math.radians(angle_degrees)
        
        dx = length * math.cos(angle_radians)
        dy = length * math.sin(angle_radians)
        
        x2 = x1 + dx
        y2 = y1 + dy
        
        return (x2, y2)

if __name__ == "__main__":
    num_patterns = int(input("Number of Patterns: "))
    filename = input("Filename: ")
    if filename == "":
        filename = "output"
    filename = str(Path(filename).with_suffix(".pdf"))
    c = canvas.Canvas(filename, pagesize=A6)
    for _ in range(num_patterns):
        num_shapes = int(input("Number of Shapes: "))
        shape = input("Shape: \nrect\ntri\n")
        size = int(input("Size: "))
        Pattern(filename=filename, num_shapes=num_shapes, size=size, shape=shape, can=c)
    c.showPage()
    c.save()
    