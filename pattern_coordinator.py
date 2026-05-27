from models.models import PatternConfig, DrawingConfig, FileConfig, SettingsConfig
from point import Point

class PatternCoordinator():
    '''exposes functions to the dashboard manipulate patterns '''
    def __init__(self):
        #initialize pattern classes
        #and file classes etc
        pass

    def calculate_and_render(self, pattern_config: PatternConfig, drawing_config: DrawingConfig, settings_config: SettingsConfig):
        pass

    def _calculate(self, config: PatternConfig, settings_config: SettingsConfig):
        pass

    def _render_to_ui(self, drawing_config: DrawingConfig):
        pass

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