from nicegui import ui, app
from pathlib import Path
from File import File


class Interface():
    '''Creates the UI Components of the application'''
    def __init__(self):
 
        self.patterns_list = []
        self.splines_list = []
        f = File(self)

        # --- UI Layout ---
        ui.query('body').classes('bg-slate-100')

        # Main layout split into a 2-column grid (Left: Controls, Right: PDF Viewer)
        with ui.grid(columns='1fr 1fr').classes('w-full max-w-6xl mx-auto my-10 gap-6 p-4'):
            
            # LEFT COLUMN: Controls Card
            with ui.card().classes('p-6 shadow-lg rounded-xl bg-white h-fit'):
                ui.label('PDF Pattern Generator').classes('text-2xl font-bold text-slate-800 mb-2')
                
                self.filename_input = ui.input(label='Filename', placeholder='output', suffix='.pdf/.gcode').classes('w-full mb-4')
                with ui.row().classes('w-full justify-between items-center mb-2'):
                    self.cord = ui.switch('Coordinates', value=False)
                    self.gcode_x = ui.number(label='GCODE X Offset', value=10.5, min=0, step=0.01).classes('w-24')
                    self.gcode_y = ui.number(label='GCODE Y Offset', value=23.5, min=0, step=0.01).classes('w-24')
                
                ui.separator().classes('my-2')
                with ui.row().classes('w-full justify-between items-center mb-2'):
                    ui.label('Center').classes('text-lg font-semibold text-slate-700')
                    self.num_center_points = ui.number(label='Points', value=1, min=1, step=1).classes('w-24')
                    self.radius = ui.slider(min=0, max=100, step=1, value=1).classes('w-32 intermediate-class')
                    ui.label().bind_text_from(self.radius, 'value').classes('w-12 text-right')
                ui.separator().classes('my-2')

                
                with ui.row().classes('w-full justify-between items-center mb-2'):
                    ui.label('Patterns').classes('text-lg font-semibold text-slate-700')
                    self.circles = ui.switch('Points', value=True)
                    self.lines = ui.switch('Lines', value=True)
                    self.sketch = ui.switch('Sketch', value=False)
                ui.separator().classes('my-2')
                with ui.row().classes('w-full items-left mb-2'):
                    ui.button('Add Shape', icon='add', on_click=self.add_pattern_row).props('outline size=sm color=primary')
                    ui.button('Add Spline', icon='add', on_click=self.add_spline_row).props('outline size=sm color=primary')


                self.patterns_container = ui.column().classes('w-full gap-3 mb-6')
                with self.patterns_container:
                    self.add_pattern_row() # Initial default row
                    
                ui.button('Generate & View PDF', icon='picture_as_pdf', on_click=f.generate_pdf).classes('w-full py-2 text-lg').props('color=primary')

            # RIGHT COLUMN: Dynamic PDF Viewer Card
            # It starts hidden and reveals itself the first time you click "Generate"
            with ui.card().classes('p-4 shadow-lg rounded-xl bg-white h-[860px]') as self.pdf_viewer:
                self.pdf_viewer.set_visibility(False) 
                ui.label('PDF Preview').classes('text-lg font-bold text-slate-700 mb-2')
                with ui.row():
                    ui.button('Save PDF', icon='save', on_click=lambda: f.save_current_pdf(path=self.filename_input.value)).props('flat color=green size=md')
                    ui.button('Generate GCODE', on_click=lambda: f.generate_gcode(path=self.filename_input.value)).props('flat color=blue size=md')
                
                # Native HTML iframe configured to fill the card space completely
                self.pdf_frame = ui.element('iframe').classes('w-full h-full border-none rounded-lg')

        # Start NiceGUI
        ui.run(title="Pattern Generator & Viewer")

    def add_pattern_row(self):
        pattern_data = {'row': None, 'shape': None, 'num_shapes': None, 'size': None, 'hex': '#000000','line_points': None}

        shape_options = {
        0: 'Spline',
        2: 'Line',
        3: 'Triangle',
        4: 'Square',
        5: 'Pentagon'
        }

        def handle_type_change(e):
            if e.value == 'line':
                line_points.value = -1
                num_shapes.value = 20
            if e.value == 'dotted':
                line_points.value = 5
                num_shapes.value = 1

        with ui.row().classes('items-center w-full bg-slate-50 p-3 rounded-lg shadow-sm') as row:
            shape = ui.select(label='Shape', options=shape_options, value=3).classes('w-28')
            num_shapes = ui.number(label='Number', value=20, min=1, step=1).classes('w-24')
            size = ui.number(label='Size', value=200, min=1).classes('w-24')
            with ui.button(icon='colorize') as button:
                color = ui.color_picker(on_pick=lambda e: (button.style(f'background-color: {e.color} !important;'), 
                                                        pattern_data.update({'hex': e.color})))
            offset = ui.slider(min=0, max=1, step=0.01, value=1).classes('w-32')
            ui.label().bind_text_from(offset, 'value').classes('w-6')
            line_type = ui.select(label="Linetype", options=['line', 'dotted'], value='line').classes('w-26').on_value_change(handle_type_change)
            line_points = ui.number(label="Points", value=-1, min=-1, step=1).classes('w-24') \
                .bind_visibility_from(line_type, 'value', backward=lambda v: v == 'dotted') 
            ui.button(icon='delete', on_click=lambda: self.remove_pattern_row(row, pattern_data)).props('flat color=red')

        pattern_data.update({'row': row, 'shape': shape, 'num_shapes': num_shapes, 'size': size, 'offset': offset, 'line_points': line_points})
        self.patterns_list.append(pattern_data)

    def add_spline_row(self):
        spline_data = {'row': None, 'spline': None, 'num_points': None, 'start_point': None, 'control_point': None, 'end_point': None}
        points = []

        with ui.row().classes('items-center w-full bg-slate-50 p-3 rounded-lg shadow-sm items-start') as row:
            with ui.column().classes('items-left bg-slate-50 p-3 rounded-lg shadow-sm'):
                for i in range(3):
                    ui.label(f"Point {i+1}")
                    with ui.row():
                        angle = ui.number(label='Angle', value=(i-1)*45, step=1).classes('w-24')
                        dist = ui.number(label='Distance', value=100, min=1, step=1).classes('w-24')
                        points.append((angle, dist))
            with ui.column().classes('grow h-full bg-slate-50 p-3 rounded-lg shadow-sm items-start'):
                spline = ui.switch('Show Spline', value=False)
                num_points = ui.number(label="Points", value=2, min=2, step=1).classes('w-24')
                ui.button(icon='delete', on_click=lambda: self.remove_splines_row(row, spline_data)).props('flat color=red')

                
        spline_data.update({'row': row, 'spline': spline, 'num_points': num_points,
                            'start_point': points[0], 'control_point': points[1], 'end_point': points[2]})
        self.splines_list.append(spline_data)

    def remove_pattern_row(self, row_element, pattern_data):
        self.patterns_container.remove(row_element)
        self.patterns_list.remove(pattern_data)

    def remove_splines_row(self, row_element, pattern_data):
        self.patterns_container.remove(row_element)
        self.splines_list.remove(pattern_data)