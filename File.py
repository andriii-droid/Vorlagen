from nicegui import ui, app
from Pattern import Pattern
from Shape import Shape
from Spline import Spline
from Point import Point
from pathlib import Path
import time
import os
import tempfile
import webbrowser

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
            page = Pattern(filename=str(pdf_path), 
                            circles=int(self.I.circles.value),
                            lines=int(self.I.lines.value),
                            sketch=int(self.I.sketch.value),
                            cord=int(self.I.cord.value))
            shape = Shape(page, center_radius=int(self.I.radius.value))
            spline = Spline(page)
            center_points = shape.calc_shape(page.center, num_points=int(self.I.num_center_points.value))
            for cp in center_points:
                page.center = cp
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
                    
            page.savePDF()
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

    def delete_current_pdf(self):
        if self.current_pdf_path and self.current_pdf_path.exists():
            try:
                # 1. Clear iframe source so the browser releases the file lock
                self.I.pdf_frame.props('src=""')
                
                # 2. Delete file from local storage
                self.current_pdf_path.unlink()
                ui.notify(f"Deleted {self.current_pdf_path.name} successfully.", type='positive')
                
                # 3. Clean up UI state
                self.current_pdf_path = None
                self.I.pdf_viewer.set_visibility(False)
            except Exception as e:
                ui.notify(f"Could not delete file: {str(e)}", type='negative')
        else:
            ui.notify("No generated file found to delete.", type='warning')

    def save_current_pdf(self, path):
        self.I.pdf_viewer.set_visibility(False)
        self.I.filename_input.value = ""

        self.current_pdf_path = None
        self.generate_pdf(path=path)
        

