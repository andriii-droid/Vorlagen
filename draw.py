from models.models import PatternConfig, DrawingConfig, ShapeConfig, SplineConfig
from point import Point
from shape import Shape
from spline import Spline



class Draw():
    def __init__(self):
        self._canvas_width_in_mm = 105
        self._canvas_height_in_mm = 148
        self._center_point = Point(self._canvas_width_in_mm / 2, self._canvas_height_in_mm / 2)
        self._scale_factor = 1

    def set_canvas_dim(self, dim):
        self._scale_factor = dim[0] / self._canvas_width_in_mm

    def draw_points(self, pat: Shape | Spline):
        content = ""
        for p in pat.points:
            x = p.x + self._center_point.x
            y = p.y + self._center_point.y
            content += f'''<circle cx="{x*self._scale_factor}" cy="{y*self._scale_factor}" r="1" fill="black" />'''
        return content
    
    def draw_shape_lines(self, shape: Shape, shape_type):
        content = ""
        point_list = [shape.points[i:i + shape_type] for i in range(0, len(shape.points), shape_type)]
        for point_shape in point_list:
            for count, (p1, p2) in enumerate(zip(point_shape, point_shape[1:]+[point_shape[0]])):
                x1 = p1.x + self._center_point.x
                y1 = p1.y + self._center_point.y    # TODO
                x2 = p2.x + self._center_point.x
                y2 = p2.y + self._center_point.y
                content += f'''<line x1="{x1*self._scale_factor}" y1="{y1*self._scale_factor}" 
                x2="{x2*self._scale_factor}" y2="{y2*self._scale_factor}" fill="none" stroke="{shape.config.hex_color}" stroke-width=".2" />'''
        return content