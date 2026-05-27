from dataclasses import dataclass
from point import Point

@dataclass
class SettingsConfig:
    '''Data contract for global pattern settings'''
    num_center_points: int
    center_point_radius: float

@dataclass
class FileConfig:
    '''Data contract for Filesettings'''
    filename: str
    gcode_offset_x: float
    gcode_offset_y: float

@dataclass
class DrawingConfig:
    '''Data contract for drawing settings'''
    draw_points: bool
    draw_lines: bool
    draw_sketch: bool
    draw_coordinates: bool


@dataclass
class ShapeConfig:
    """Data contract for shapes"""
    shape_type: int
    num_shapes: int
    size: float
    hex_color: str
    offset: float
    line_points: int
    center: Point

@dataclass
class SplineConfig:
    """Data contract for complex spline tracks."""
    show_spline: bool
    num_points: int
    start_point: Point
    control_point: Point
    end_point: Point
    center: Point

@dataclass
class PatternConfig:
    """Data contract for patterns."""
    patterns: list[SplineConfig | ShapeConfig]
