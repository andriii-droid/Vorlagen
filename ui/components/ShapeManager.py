from ui.components.PatternRow import PatternRow
from nicegui import ui, app

class ShapeManagerPage:
    def __init__(self):
        # Store instances of PatternRow objects rather than dictionaries
        self.patterns_list: list[PatternRow] = []

    def build(self):
        ui.button('Add Shape', icon='add', on_click=self.add_row).props('outline size=sm color=primary')


        self.container = ui.column().classes('w-full gap-2')

    def add_row(self):
        with self.container:
            # Create a new row, and pass our delete method as the callback
            new_row = PatternRow(on_delete_callback=self.remove_row)
            self.patterns_list.append(new_row)

    def remove_row(self, row_instance: PatternRow):
        """Triggered by the child row."""
        # 1. Remove the HTML elements from the browser screen
        self.container.remove(row_instance.row)
        # 2. Remove the row object from our tracking list
        self.patterns_list.remove(row_instance)

    def process_all_patterns(self):
        """Example: Grab data from all rows when a 'Submit' button is clicked."""
        for row in self.patterns_list:
            data = row.get_data()
            print(f"Processing shape {data['shape']} with color {data['hex']}")