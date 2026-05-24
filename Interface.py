from nicegui import ui, app
import time

from pathlib import Path
from Pattern import Pattern
from Shape import Shape
from Spline import Spline
from Point import Point



class Interface():
    '''Creates the UI Components of the application'''
    def __init__(self):
        # Create a local directory to save PDFs if it doesn't exist
        # NiceGUI needs a static folder to serve local files safely to the browser
        self.static_dir = Path("./static")
        self.static_dir.mkdir(exist_ok=True)

        # Tell NiceGUI to serve files from the '/static' folder at the URL path '/download'
        app.add_static_files('/download', str(self.static_dir))


        self.current_pdf_path = None
        self.saved = False
        self.patterns_list = []
        self.splines_list = []

        # --- UI Layout ---
        ui.query('body').classes('bg-slate-100')

        # Main layout split into a 2-column grid (Left: Controls, Right: PDF Viewer)
        with ui.grid(columns='1fr 1fr').classes('w-full max-w-6xl mx-auto my-10 gap-6 p-4'):
            
            # LEFT COLUMN: Controls Card
            with ui.card().classes('p-6 shadow-lg rounded-xl bg-white h-fit'):
                ui.label('PDF Pattern Generator').classes('text-2xl font-bold text-slate-800 mb-2')
                
                self.filename_input = ui.input(label='Filename', placeholder='output', suffix='.pdf').classes('w-full mb-4')
                self.cord = ui.switch('Coordinates', value=False)
                
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


                patterns_container = ui.column().classes('w-full gap-3 mb-6')
                with patterns_container:
                    self.add_spline_row() # Initial default row
                    
                ui.button('Generate & View PDF', icon='picture_as_pdf', on_click=self.generate_pdf).classes('w-full py-2 text-lg').props('color=primary')

            # RIGHT COLUMN: Dynamic PDF Viewer Card
            # It starts hidden and reveals itself the first time you click "Generate"
            with ui.card().classes('p-4 shadow-lg rounded-xl bg-white h-[860px]') as self.pdf_viewer:
                self.pdf_viewer.set_visibility(False) 
                ui.label('PDF Preview').classes('text-lg font-bold text-slate-700 mb-2')
                with ui.row():
                    ui.button('Delete PDF', icon='delete_forever', on_click=self.delete_current_pdf).props('flat color=red size=md')
                    ui.button('Save PDF', icon='save', on_click=self.save_current_pdf).props('flat color=green size=md')

                
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

    def generate_pdf(self):
        if not self.saved:
            self.delete_current_pdf()
            saved = False

        raw_filename = self.filename_input.value.strip() or "output"
        
        pdf_path = self.static_dir / Path(raw_filename).with_suffix(".pdf")
        
        if not self.patterns_list and not self.splines_list:
            ui.notify("Please add at least one pattern or spline.", type='warning')
            return

        try:
            page = Pattern(filename=str(pdf_path), 
                            circles=int(self.circles.value),
                            lines=int(self.lines.value),
                            sketch=int(self.sketch.value),
                            cord=int(self.cord.value))
            shape = Shape(page, center_radius=int(self.radius.value))
            spline = Spline(page)
            center_points = shape.calc_shape(page.center, num_points=int(self.num_center_points.value))
            for cp in center_points:
                page.center = cp
                for p in self.patterns_list:
                    shape.generate_shape(
                        num_shapes=int(p['num_shapes'].value),
                        size=int(p['size'].value),
                        shape=int(p['shape'].value),
                        col=p['hex'],
                        offset=float(p['offset'].value),
                        line_points=int(p['line_points'].value))
                for s in self.splines_list:
                    spline.generate_spline(
                        spline=int(s['spline'].value),
                        num_points=int(s['num_points'].value),
                        start_point=(Point.from_polar(int(s['start_point'][0].value), int(s['start_point'][1].value))),
                        control_point=(Point.from_polar(int(s['control_point'][0].value), int(s['control_point'][1].value))),
                        end_point=(Point.from_polar(int(s['end_point'][0].value), int(s['end_point'][1].value))))
                    
            page.savePDF()
            
            ui.notify(f"Generated {pdf_path.name}!", type='positive')
            self.current_pdf_path = pdf_path
            
            # --- Update the PDF Viewer Section ---
            # We point the iframe source to the local route we mapped earlier + a timestamp to force refresh
            self.pdf_viewer.set_visibility(True)
            self.pdf_frame.props(f'src="/download/{pdf_path.name}?t={time.time()}"')
        
        except Exception as e:
            ui.notify(f"Error: {str(e)}", type='negative')

    def delete_current_pdf(self):
        if self.current_pdf_path and self.current_pdf_path.exists():
            try:
                # 1. Clear iframe source so the browser releases the file lock
                self.pdf_frame.props('src=""')
                
                # 2. Delete file from local storage
                self.current_pdf_path.unlink()
                ui.notify(f"Deleted {self.current_pdf_path.name} successfully.", type='positive')
                
                # 3. Clean up UI state
                self.current_pdf_path = None
                self.pdf_viewer.set_visibility(False)
            except Exception as e:
                ui.notify(f"Could not delete file: {str(e)}", type='negative')
        else:
            ui.notify("No generated file found to delete.", type='warning')

    def save_current_pdf(self):
        ui.notify(f"Saved {self.current_pdf_path.name} successfully.", type='positive')
        self.pdf_viewer.set_visibility(False)
        self.filename_input.value = ""

        self.current_pdf_path = None
        self.saved = True
        

