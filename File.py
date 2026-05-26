from nicegui import ui, app
from Pattern import Pattern
from Shape import Shape
from Spline import Spline
from Point import Point
from pathlib import Path
import time
import tempfile

class File():
    '''Implements Functions to save the Patterns as a file'''
    def __init__(self, Interface):
        '''Initializes a tmp directory'''
        self.current_pdf_path = None
        self.I = Interface
        TMP_DIR = tempfile.gettempdir()
        app.add_static_files('/tmp_download', TMP_DIR)
        self.page = None
        self.conversion_fac = 25.4/72


    def generate_pdf(self, path=None):
        '''Generates it as a pdf, depending on par "path" to a tmp directory or to the static directory in the project'''
        self.save_gcode_offset_file()
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
            self.I.len = round(self.page.length * self.conversion_fac /1000*1.1, 2) #multiply by 1.1 to account slack
            self.page.savePDF()
            if path is None:
                ui.notify(f"Generated {pdf_path.name}!", type='positive')
            self.current_pdf_path = pdf_path
            
            if path is None:
                self.I.pdf_viewer.set_visibility(True)
                self.I.pdf_frame.props(f'src="/tmp_download/{pdf_path.name}?t={time.time()}"')     
            else:
                self.I.pdf_viewer.set_visibility(False)
        except Exception as e:
            ui.notify(f"Error: {str(e)}", type='negative')

    def save_current_pdf(self, path):
        '''Sets pdf viewer invisible, and calls generate_pdf with path parameter'''
        self.I.pdf_viewer.set_visibility(False)
        self.I.filename_input.value = ""

        self.current_pdf_path = None
        self.generate_pdf(path=path)

    def generate_gcode(self, path=""):
        '''generates a gcode file using the points of a pattern as coordinates'''
        self.save_gcode_offset_file()
        offset_x = float(self.I.gcode_x.value) + 5   #Calculate Offset: 5 for homing point relative to card edge, and the input for correction to homing edge
        offset_y = float(self.I.gcode_y.value) + 5
        start = f"; Time: {time.time()}"
        start += "M17 ; Enable all stepper motors\n"
        start += "G90 ; Set to Absolute Positioning\n"
        start += "M83 ; Set extruder to relative mode\n"
        start += "G1 Z40 F1200\n"
        start += "M109 R40 ; Cool down Nozzle before Homing\n"
        start += "G28 ; Home all axes\n"
        start += "G1 Z20 F1200 ; Lift nozzle to 20mm quickly for safety\n"
        start += f"G1 X{self.I.gcode_x.value} Y{self.I.gcode_y.value} F4800 ; Move over the Homing Point, if set correctly\n"
        start += "M117 Attention Required! ; Display message on the screen\n"
        start += "M0 Click to Resume ; Stop print, wait for LCD button press\n"
        end = "G1 Z40 F1200 ; Lift nozzle safely up to 20mm when done\n"
        end += "G1 X0 Y200 F4800 ; Present the bed (pushes bed forward, moves X to 0)\n"
        end += "M84 ; Disable stepper motors\n"

        static_dir = Path("./gcode")
        static_dir.mkdir(exist_ok=True)

        if path == "":
            path = "output.gcode"

        file_name = Path(path.strip()).with_suffix(".gcode").name
        output_path = static_dir / file_name

        with open(output_path, "w") as f:
            f.write(start)
            flat_points = [item for sublist in self.page.points for item in sublist]
            for p in flat_points:
                f.write(f"G1 X{p.cartesian[0]*self.conversion_fac + offset_x:.3f} Y{p.cartesian[1]*self.conversion_fac + offset_y:.3f} F4800;\n")
                f.write("G1 Z0 F4800\n")
                f.write("G1 Z15 F4800\n")
            f.write(end)
        ui.notify(f"Generated {output_path.name}!", type='positive')

    def save_gcode_offset_file(self):
        '''Saves the gcode offset to an txt file'''
        with open("gcode_offset.txt", "w") as f:
            f.write(f"{self.I.gcode_x.value}\n")
            f.write(f"{self.I.gcode_y.value}\n")

    def read_gcode_offset_from_file(self):
        '''Reads the gcode coordinates from the txt file and displays it in the UI'''
        with open("gcode_offset.txt", "r") as f:
            x = float(f.readline())
            y = float(f.readline())
        return (x, y)

