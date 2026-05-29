from models.models import PatternConfig, DrawingConfig, FileConfig, SettingsConfig, ShapeConfig, SplineConfig
from point import Point
from shape import Shape
from spline import Spline
from gcode import GCODE
from draw import Draw

class PatternCoordinator():
    '''exposes functions to the dashboard manipulate patterns '''
    def __init__(self):
        self.patterns: list[Shape | Spline] = []
        self.gcode = GCODE(self)
        self.draw = Draw()
        self._canvas_content = ''''''
        self._gcode_offset_x = (0,0)

    def calculate_and_render(self, pattern_config: PatternConfig, 
                             drawing_config: DrawingConfig, 
                             settings_config: SettingsConfig):
        '''calculates and then draws the patterns to the ui'''
        self._calculate(pattern_config=pattern_config, settings_config=settings_config)
        self._render_to_ui(drawing_config=drawing_config)

    def _calculate(self, pattern_config: PatternConfig, 
                   settings_config: SettingsConfig):
        '''calculates the specified patterns and stores the patterns'''
        self.patterns = []

        #create center points
        c = Shape(ShapeConfig(
            shape_type=int(settings_config.num_center_points),
            num_shapes=1,
            size=float(settings_config.center_point_radius),
            hex_color="", 
            offset=1,
            line_points=0,
            center=Point(0,0) 
            ))
        c.generate()
        center_points = c.points

        #for each center point create one pattern
        for cp in center_points:
            for pattern in pattern_config.patterns:
                pattern.center = cp
                if isinstance(pattern, ShapeConfig):
                    s = Shape(pattern)
                    s.generate()
                    self.patterns.append(s)
                elif isinstance(pattern, SplineConfig):
                    s = Spline(pattern)
                    s.generate()
                    self.patterns.append(s)
                

    def _render_to_ui(self, drawing_config: DrawingConfig):
        '''draws points and lines to the ui'''
        self._canvas_content = ''''''
        if drawing_config.draw_points: #Draws Points if configured
            for pat in self.patterns:
                self._canvas_content += self.draw.draw_points(pat)

        for pat in self.patterns:
            self._canvas_content += self.draw.draw_lines(drawing_config, pat)


    def export_to_pdf(self, file_config: FileConfig):
        pass

    def export_to_gcode(self, file_config: FileConfig):
        self.gcode.generate_gcode(file_config.filename)

    def optimize(self):
        pass

    @property
    def gcode_offset(self):
        return self._gcode_offset
    
    @gcode_offset.setter
    def gcode_offset(self, value):
        self._gcode_offset = value

    @property
    def gcode_offset_x(self):
        print(self._gcode_offset)
        return self._gcode_offset[0]
    
    @property
    def gcode_offset_y(self):
        return self._gcode_offset[1]
    
    @property
    def string_length(self):
        return 0
    
    @property
    def canvas_content(self):
        return self._canvas_content

    def canvas_dimensions(self, dim):
        self._canvas_dim = (dim['width'], dim['height'])
        self.draw.set_canvas_dim(self._canvas_dim)