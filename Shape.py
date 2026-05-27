import math
from point import Point
from models.models import ShapeConfig


class Shape():
    '''implement functions to generate shapes'''
    def __init__(self, config: ShapeConfig):
        self.config = config
        self._points: list[Point] = []

    def generate(self):
        '''calls the _calculate function with specified number of corners, a specified number of times with an angle offset'''  
        angle = 0
        step = 360 / self.config.num_shapes
        for _ in range(self.config.num_shapes):     #calls calc_shape multiple times
            points_tmp = self._calculate(angle=angle, num_points=self.config.shape_type, center=self.config.center)
            if self.config.line_points != 0: #if there should be points genereted on each line, it gets calculated here
                points_tmp = self._generate_points_on_shape(points=points_tmp, num_points=self.config.line_points)
            self._points.append(points_tmp)

            angle += step   

    def _calculate(self, center, angle=0, num_points=1):
        '''calculates shape points around a center point. the number of points can be specified'''
        points = []
        if num_points == 1:
            points.append(center)
            return points
        
        points.append(self._new_point(center, (self.config.size/2)*self.config.offset, 90+angle))
        rotation_angle = -360/num_points/2 + angle
        for _ in range(num_points - 1):
            points.append(self._new_point(points[-1], self.config.size*math.sin(math.pi/num_points), rotation_angle))
            rotation_angle -= 360/num_points
        return points
    
    def _generate_points_on_shape(self, points, num_points):
        """
        Generates a list of Point objects evenly spaced between each two points in the given points list
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
    
    def _new_point(self, start_point, length, angle_degrees):
        '''calculates a new Point with a given startpoint lenght and and angle in degrees'''
        x1, y1 = start_point.cartesian
        
        angle_radians = math.radians(angle_degrees)
        
        dx = length * math.cos(angle_radians)
        dy = length * math.sin(angle_radians)
        
        x2 = x1 + dx
        y2 = y1 + dy
        
        return Point(x2, y2)
    
    @property
    def points(self):
        return self._points