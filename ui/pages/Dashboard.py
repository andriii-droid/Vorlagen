from nicegui import ui, events
from ui.components.pattern_manager import PatternManagerPage
from pattern_coordinator import PatternCoordinator
from models.models import SettingsConfig, FileConfig, DrawingConfig
import urllib.parse

class DashboardPage():
    '''handles the dashboard'''
    def __init__(self):
        self.pattern_page = PatternManagerPage()
        self.coordinator = PatternCoordinator()

    def build(self):
        '''builds the dashboard'''
        ui.query('body').classes('bg-slate-100')

        # Main layout split into a 2-column grid (Left: Controls, Right: PDF Viewer)
        with ui.grid(columns='1fr 1fr').classes('w-full max-w-6xl mx-auto my-10 gap-6 p-4'):
    
    # LEFT COLUMN: Controls Card
            with ui.card().classes('p-6 shadow-lg rounded-xl bg-white h-fit'):
                ui.label('Pattern Generator').classes('text-2xl font-bold text-slate-800 mb-2')
                
                self.filename_input = ui.input(label='Filename', placeholder='output', suffix='.pdf/.gcode').classes('w-full mb-4')
                with ui.row().classes('w-full justify-between items-center mb-2'):
                    self.cord = ui.switch('Coordinates', value=False)
                    self.gcode_x = ui.number(label='GCODE X Offset', value=self.coordinator.gcode_offset_x, min=0, step=0.1, on_change=lambda e: setattr(self.coordinator, 'gcode_offset', (e.value, self.gcode_y.value))).classes('w-24')
                    self.gcode_y = ui.number(label='GCODE Y Offset', value=self.coordinator.gcode_offset_y, min=0, step=0.1, on_change=lambda e: setattr(self.coordinator, 'gcode_offset', (self.gcode_x.value, e.value))).classes('w-24')
                
                ui.separator().classes('my-2')
                with ui.row().classes('w-full justify-between items-center mb-2'):
                    ui.label('Center').classes('text-lg font-semibold text-slate-700')
                    self.num_center_points = ui.number(label='Points', value=1, min=1, step=1).classes('w-24')
                    self.radius = ui.slider(min=0, max=100, step=1, value=0).classes('w-32 intermediate-class')
                    ui.label().bind_text_from(self.radius, 'value').classes('w-12 text-right')
                ui.separator().classes('my-2')

                with ui.row().classes('w-full justify-between items-center mb-2'):
                    ui.label('Patterns').classes('text-lg font-semibold text-slate-700')
                    self.points = ui.switch('Points', value=True)
                    self.lines = ui.switch('Lines', value=True)
                    self.sketch = ui.switch('Sketch', value=False)
                ui.separator().classes('my-2')
                
                with ui.row().classes('w-full items-left mb-2'):
                    self.pattern_page.build()
                    
                # Updated Action: Generates data AND triggers the UI refresh
                ui.button('Generate Pattern', icon='picture_as_pdf', 
                        on_click=lambda: self.coordinator.calculate_and_render(pattern_config=self.pattern_page.get_config(),
                                                                               drawing_config=self.get_drawing_config(),
                                                                               settings_config=self.get_settings_config())
                        ).classes('w-full py-2 text-lg').props('color=primary')

                        # RIGHT COLUMN: Preview Card
            with ui.card().classes('p-6 shadow-lg rounded-xl bg-white h-[860px] items-center'):
                
                # Header and Actions row
                with ui.row().classes('w-full justify-between items-center mb-4'):
                    ui.label('Preview').classes('text-2xl font-bold text-slate-800')
                    with ui.row().classes('gap-2'):
                        ui.button('Save PDF', icon='save',
                                on_click=lambda: self.coordinator.export_to_pdf(file_config=self.get_file_config())
                                ).props('flat color=green size=md')
                        ui.button('Save GCODE', icon='playlist_add',
                                on_click=lambda: self.coordinator.export_to_gcode(file_config=self.get_file_config())
                                ).props('flat color=blue size=md')                

                raw_svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 105 148" width="100%"></svg>'
                blank_bg = f'data:image/svg+xml;utf8,{urllib.parse.quote(raw_svg)}'
                    
                # 2. Assign the click function directly to on_mouse
                ii = ui.interactive_image(
                    blank_bg, 
                    cross=False).classes('h-full w-auto max-h-[700px] object-contain shadow-md rounded-lg bg-white')
                ii.on('loaded', lambda e: self.coordinator.canvas_dimensions(e.args))
                ii.bind_content_from(self.coordinator, 'canvas_content')

    def get_drawing_config(self):
        '''collects drawing config data'''
        return DrawingConfig(
            draw_points=bool(self.points.value),
            draw_lines=bool(self.lines.value),
            draw_sketch=bool(self.sketch.value),
            draw_coordinates=bool(self.cord.value)
        )

    def get_file_config(self):
        '''collects file config data'''
        return FileConfig(
            filename=self.filename_input,
            gcode_offset_x=float(self.gcode_x.value),
            gcode_offset_y=float(self.gcode_y.value)
        )
    
    def get_settings_config(self):
        '''collects setting config data'''
        return SettingsConfig(
            num_center_points=int(self.num_center_points.value),
            center_point_radius=float(self.radius.value)
        )