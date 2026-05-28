from nicegui import ui
from models.models import SplineConfig
from point import Point

class SplineRow:
    def __init__(self, on_delete_callback):
        """
        Represents a single spline configuration row in the UI.
        :param on_delete_callback: A function to call when the delete button is clicked.
        """
        self.on_delete = on_delete_callback
        
        # We will store the NiceGUI number element instances here to easily read them later
        self.points_ui = []

        # 1. Main outer row wrapper (items-start keeps columns aligned at the top)
        with ui.row().classes('items-center w-full bg-slate-50 p-3 rounded-lg shadow-sm items-start') as self.row:
            
            # Left Column: Coordinates for the 3 points
            with ui.column().classes('items-left bg-slate-50 p-3 rounded-lg shadow-sm'):
                point_labels = ["Start Point", "Control Point", "End Point"]
                
                for i in range(3):
                    ui.label(point_labels[i]).classes('font-semibold text-xs text-slate-500 mt-1')
                    with ui.row().classes('gap-2'):
                        # Generate unique default angles based on your original logic
                        default_angle = (i - 1) * 45
                        
                        angle_input = ui.number(label='Angle', value=default_angle, step=1).classes('w-24')
                        dist_input = ui.number(label='Distance', value=40, min=1, step=1).classes('w-24')
                        
                        # Store references to the active UI elements as a dictionary pair
                        self.points_ui.append({
                            'angle_input': angle_input,
                            'dist_input': dist_input
                        })
            
            # Right Column: Spline settings & controls
            with ui.column().classes('grow h-full bg-slate-50 p-3 rounded-lg shadow-sm items-start gap-4'):
                self.show_spline = ui.switch('Show Spline', value=False)
                self.num_points = ui.number(label="Points", value=2, min=2, step=1).classes('w-24')
                
                # Delete button triggers the parent callback, passing this entire instance
                ui.button(icon='delete', on_click=lambda: self.on_delete(self)).props('flat color=red class=mt-auto')

    def get_config(self):
        """Helper method to extract current UI state into spline config object"""
        return SplineConfig(
            show_spline=bool(self.show_spline.value),
            num_points=int(self.num_points.value),
            start_point=Point.from_polar(angle_degrees=self.points_ui[0]['angle_input'].value,
                                         distance=self.points_ui[0]['dist_input'].value),
            control_point=Point.from_polar(angle_degrees=self.points_ui[1]['angle_input'].value,
                                         distance=self.points_ui[1]['dist_input'].value),
            end_point=Point.from_polar(angle_degrees=self.points_ui[2]['angle_input'].value,
                                         distance=self.points_ui[2]['dist_input'].value),
            center=Point(0,0)
            )
        