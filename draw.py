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
            x = (p.x + self._center_point.x) * self._scale_factor
            y = (p.y + self._center_point.y) * self._scale_factor
            content += f'''<circle cx="{x}" cy="{y}" r="1" fill="black" />'''
        return content
    
    def draw_lines(self, drawing_config: DrawingConfig, pat: Shape | Spline):
        pass
    
    def draw_shape_lines(self, shape: Shape, sketch=False):
        if sketch:
            col = "#ff0000"
            stroke_width = 0.8
            points = shape.sketch_points
        else:
            col = shape.config.hex_color
            stroke_width = 0.2
            points = shape.points

        content = ""
        point_lists = [points[i:i + shape.config.shape_type] for i in range(0, len(points), shape.config.shape_type)]
        for point_shape in point_lists:
            for (p1, p2) in zip(point_shape, point_shape[1:]+[point_shape[0]]):
                p1 = (p1 + self._center_point) * self._scale_factor
                p2 = (p2 + self._center_point)  * self._scale_factor
                content += f'''<line x1="{p1.x}" y1="{p1.y}" 
                x2="{p2.x}" y2="{p2.y}" fill="none" stroke="{col}" stroke-width="{stroke_width}" />'''
        return content
    
    def draw_lines_between_line_points(self, shape: Shape, sketch=False):
        content = ""
        for (p1, p2) in zip(shape.points, shape.points[shape.config.line_points+2:]+shape.points[0:shape.config.line_points+2]):
            p1 = (p1 + self._center_point) * self._scale_factor
            p2 = (p2 + self._center_point)  * self._scale_factor
            content += f'''<line x1="{p1.x}" y1="{p1.y}" 
            x2="{p2.x}" y2="{p2.y}" fill="none" stroke="{shape.config.hex_color}" stroke-width=".2" />'''
        return content
