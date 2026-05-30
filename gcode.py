from pathlib import Path
import time
from shape import Shape
from spline import Spline

class GCODE():
    def __init__(self, coordinator):
        self.coordinator = coordinator

    def generate_gcode(self, patterns: list[Shape | Spline], path="",):
        '''generates a gcode file using the points of a pattern as coordinates'''

        offset_x = float(self.coordinator.gcode_offset_x) + 5   #Calculate Offset: 5 for homing point relative to card edge, and the input for correction to homing edge
        offset_y = float(self.coordinator.gcode_offset_y) + 5
        start = f"; Time: {time.time()}"
        start += "M17 ; Enable all stepper motors\n"
        start += "G90 ; Set to Absolute Positioning\n"
        start += "M83 ; Set extruder to relative mode\n"
        start += "G1 Z40 F1200\n"
        start += "M109 R40 ; Cool down Nozzle before Homing\n"
        start += "G28 ; Home all axes\n"
        start += "G1 Z20 F1200 ; Lift nozzle to 20mm quickly for safety\n"
        start += f"G1 X{self.coordinator.gcode_offset_x} Y{self.coordinator.gcode_offset_y} F4800 ; Move over the Homing Point, if set correctly\n"
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
            
            for pat in patterns:
                for p in pat.points:
                    f.write(f"G1 X{p.cartesian[0] + offset_x:.3f} Y{p.cartesian[1] + offset_y:.3f} F4800;\n")
                    f.write("G1 Z0 F4800\n")
                    f.write("G1 Z15 F4800\n")
            f.write(end)

    def save_gcode_offset_file(self, value):
        '''Saves the gcode offset to an txt file'''
        with open("gcode_offset.txt", "w") as f:
            f.write(f"{value[0]}\n")
            f.write(f"{value[1]}\n")

    def read_gcode_offset_from_file(self):
        '''Reads the gcode coordinates from the txt file and displays it in the UI'''
        with open("gcode_offset.txt", "r") as f:
            try:
                x = float(f.readline())
                y = float(f.readline())
            except:
                x, y = (0,0)
        return (x, y)