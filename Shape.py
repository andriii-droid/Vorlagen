from Pattern import Pattern 
import math
from reportlab.lib.pagesizes import A6
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from Point import Point

class Shape():
    def __init__(self, pattern, center_radius=0):
        self.pattern = pattern
        self.size = center_radius
        self.offset = 1

    def generate_shape(self, shape="rect", num_shapes=1,  col='#000000',  size=100, offset=1, line_points=0):
        self.col = col
        self.size = size
        self.offset = offset
        self.pattern.c.setFillColor(col)
        angle = 0
        step = 360 / num_shapes
        for _ in range(num_shapes):
            if angle == 0 and self.pattern.sketch:
                self.pattern.c.setLineWidth(1)
                self.pattern.c.setStrokeColor(colors.red)
            else:
                self.pattern.c.setLineWidth(.2)
                self.pattern.c.setStrokeColor(col)

            points = self.calc_shape(angle=angle, num_points=shape, center=self.pattern.center)
            if line_points:
                points = self.generate_points_on_shape(points=points, num_points=line_points)

            self.pattern.draw_points(points)
            self.pattern.draw_lines(points, angle, line_points)

            angle += step   

    def calc_shape(self, center, angle=0, num_points=1):
        points = []
        points.append(self.new_point(center, (self.size/2)*self.offset, 90+angle))
        rotation_angle = -360/num_points/2 + angle
        for _ in range(num_points - 1):
            points.append(self.new_point(points[-1], self.size*math.sin(math.pi/num_points), rotation_angle)) #TODO
            rotation_angle -= 360/num_points
        return points
    
    def generate_points_on_shape(self, points, num_points):
        """
        Generates a list of (x, y) coordinates evenly spaced between each two points in the given points list
        """
        new_points = []
        for p1, p2 in zip(points, points[1:]+[points[0]]):
            new_points.append(p1)
            for i in range(num_points+1)[1:]:
                t = i / (num_points + 1)
                x1, y1 = p1.cartesian
                x2, y2 = p2.cartesian
                x = x1 + t * (x2 - x1)
                y = y1 + t * (y2 - y1)
                new_points.append(Point(x,y))
        return new_points
    
    def new_point(self, start_point, length, angle_degrees):
        x1, y1 = start_point.cartesian
        
        angle_radians = math.radians(angle_degrees)
        
        dx = length * math.cos(angle_radians)
        dy = length * math.sin(angle_radians)
        
        x2 = x1 + dx
        y2 = y1 + dy
        
        return Point(x2, y2)