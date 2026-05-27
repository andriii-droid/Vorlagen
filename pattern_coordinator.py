from models.models import PatternConfig, DrawingConfig, FileConfig, SettingsConfig, ShapeConfig, SplineConfig
from point import Point
from shape import Shape
from spline import Spline

class PatternCoordinator():
    '''exposes functions to the dashboard manipulate patterns '''
    def __init__(self):
        self.patterns: list[Shape | Spline] = []
        pass

    def calculate_and_render(self, pattern_config: PatternConfig, drawing_config: DrawingConfig, settings_config: SettingsConfig):
        '''calculates and then draws the patterns to the ui'''
        self._calculate(pattern_config=pattern_config, settings_config=settings_config)
        self._render_to_ui(drawing_config=drawing_config, pattern_config=pattern_config)

    def _calculate(self, pattern_config: PatternConfig, settings_config: SettingsConfig):
        self.patterns = []
        for pattern in pattern_config.patterns:
            if isinstance(pattern, ShapeConfig):
                s = Shape(pattern)
                s.generate()
                self.patterns.append(s)
            elif isinstance(pattern, SplineConfig):
                s = Spline(pattern)
                s.generate()
                self.patterns.append(s)

    def _render_to_ui(self, drawing_config: DrawingConfig, pattern_config: PatternConfig):
        print(self.patterns)

    def export_to_pdf(self, file_config: FileConfig):
        pass

    def export_to_gcode(self, file_config: FileConfig):
        pass

    def optimize(self):
        pass

    @property
    def gcode_offset_x(self):
        return 0

    @property
    def gcode_offset_y(self):
        return 0
    
    @property
    def string_length(self):
        return 0