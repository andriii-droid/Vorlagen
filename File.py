from nicegui import ui, app
from Pattern import Pattern
from Shape import Shape
from Spline import Spline
from Point import Point
from pathlib import Path
import time
import tempfile

class File():
    def __init__(self, Interface):
        self.current_pdf_path = None
        self.I = Interface
        self.TMP_DIR = tempfile.gettempdir()
        app.add_static_files('/tmp_download', self.TMP_DIR)

    def generate_pdf(self, path=None):
        if path is None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                pdf_path = Path(tmp.name)
        else:
            static_dir = Path("./static")
            static_dir.mkdir(exist_ok=True)
            try:
                pdf_path = static_dir / Path(path.strip()).with_suffix(".pdf")
            except Exception as e:
                pdf_path = static_dir / Path("output").with_suffix(".pdf")
                ui.notify(f"No filename provided", type='warning')
            ui.notify(f"Saved {pdf_path.name} successfully.", type='positive')

                
        if not self.I.patterns_list and not self.I.splines_list:
            ui.notify("Please add at least one pattern or spline.", type='warning')
            return

        try:
            self.page = Pattern(filename=str(pdf_path), 
                            circles=int(self.I.circles.value),
                            lines=int(self.I.lines.value),
                            sketch=int(self.I.sketch.value),
                            cord=int(self.I.cord.value))
            shape = Shape(self.page, center_radius=int(self.I.radius.value))
            spline = Spline(self.page)
            center_points = shape.calc_shape(self.page.center, num_points=int(self.I.num_center_points.value))
            for cp in center_points:
                self.page.center = cp
                for p in self.I.patterns_list:
                    shape.generate_shape(
                        num_shapes=int(p['num_shapes'].value),
                        size=int(p['size'].value),
                        shape=int(p['shape'].value),
                        col=p['hex'],
                        offset=float(p['offset'].value),
                        line_points=int(p['line_points'].value))
                for s in self.I.splines_list:
                    spline.generate_spline(
                        spline=int(s['spline'].value),
                        num_points=int(s['num_points'].value),
                        start_point=(Point.from_polar(int(s['start_point'][0].value), int(s['start_point'][1].value))),
                        control_point=(Point.from_polar(int(s['control_point'][0].value), int(s['control_point'][1].value))),
                        end_point=(Point.from_polar(int(s['end_point'][0].value), int(s['end_point'][1].value))))
                    
            self.page.savePDF()
            if path is None:
                ui.notify(f"Generated {pdf_path.name}!", type='positive')
            self.current_pdf_path = pdf_path
            
            # --- Update the PDF Viewer Section ---
            # We point the iframe source to the local route we mapped earlier + a timestamp to force refresh
            if path is None:
                self.I.pdf_viewer.set_visibility(True)
                self.I.pdf_frame.props(f'src="/tmp_download/{pdf_path.name}?t={time.time()}"')     
            else:
                self.I.pdf_viewer.set_visibility(False)
        except Exception as e:
            ui.notify(f"Error: {str(e)}", type='negative')

    def save_current_pdf(self, path):
        self.I.pdf_viewer.set_visibility(False)
        self.I.filename_input.value = ""

        self.current_pdf_path = None
        self.generate_pdf(path=path)

    def generate_gcode(self):
        '''generates a gcode file using the points as coordinates'''
        start = "M17 ; Enable all stepper motors\n"
        start += "G90 ; Set to Absolute Positioning\n"
        start += "M83 ; Set extruder to relative mode\n"
        start += "G1 Z40 F1200\n"
        start += "M109 R40 ; Cool down Nozzle before Homing\n"
        start += "G28 ; Home all axes\n"
        start += "G1 Z20 F1200 ; Lift nozzle to 20mm quickly for safety\n"
        start += f"G1 X{offset_x} Y{offset_y} F4800 ; Move over the Homing Point, if set correctly\n"
        end = "G1 Z20 F1200 ; Lift nozzle safely up to 20mm when done\n"
        end += "G1 X0 Y200 F4800 ; Present the bed (pushes bed forward, moves X to 0)\n"
        end += "M84 ; Disable stepper motors\n"
        conversion_fac = 25.4/72
        offset_x = int(self.I.gcode_x.value) + 10   #Calculate Offset: 10 for homing point relative to card edge, and the input for correction to homing edge
        offset_y = int(self.I.gcode_y.value) + 10
        with open("myGCode.gcode", "w") as f:
            f.write(start)
            for p in self.page.points:
                f.write(f"G1 X{p.cartesian[0]*conversion_fac + offset_x} Y{p.cartesian[1]*conversion_fac + offset_y} F1200;\n")
                f.write("G1 Z15 F1200\n")
                f.write("G1 Z20 F1200\n" \
                "")
            f.write(end)

                

