
from nicegui import ui, app
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A6
from pathlib import Path
from Pattern import Pattern


# Create a local directory to save PDFs if it doesn't exist
# NiceGUI needs a static folder to serve local files safely to the browser
static_dir = Path("./static")
static_dir.mkdir(exist_ok=True)

# Tell NiceGUI to serve files from the '/static' folder at the URL path '/download'
app.add_static_files('/download', str(static_dir))

patterns_list = []
current_pdf_path = None
saved = False

def add_pattern_row():
    pattern_data = {'row': None, 'shape': None, 'num_shapes': None, 'size': None, 'hex': '#000000'}

    with ui.row().classes('items-center w-full bg-slate-50 p-3 rounded-lg shadow-sm') as row:
        shape = ui.select(label='Shape', options=['rect', 'tri', 'pent', 'line'], value='rect').classes('w-28')
        num_shapes = ui.number(label='Number', value=20, min=1, step=1).classes('w-24')
        size = ui.number(label='Size', value=200, min=1).classes('w-24')
        ui.button(icon='delete', on_click=lambda: remove_pattern_row(row, pattern_data)).props('flat color=red')
        with ui.button(icon='colorize') as button:
            color = ui.color_picker(on_pick=lambda e: (button.style(f'background-color: {e.color} !important;'), 
                                                       pattern_data.update({'hex': e.color})))
        offset = ui.slider(min=0, max=1, step=0.01, value=1).classes('w-32')
        ui.label().bind_text_from(offset, 'value')
            
    pattern_data.update({'row': row, 'shape': shape, 'num_shapes': num_shapes, 'size': size, 'offset': offset})
    patterns_list.append(pattern_data)

def remove_pattern_row(row_element, pattern_data):
    patterns_container.remove(row_element)
    patterns_list.remove(pattern_data)

def generate_pdf():
    global current_pdf_path
    global saved
    if not saved:
        delete_current_pdf()
        saved = False

    raw_filename = filename_input.value.strip() or "output"
    
    # Force the PDF to be saved inside our static directory
    pdf_path = static_dir / Path(raw_filename).with_suffix(".pdf")
    
    if not patterns_list:
        ui.notify("Please add at least one pattern.", type='warning')
        return

    try:
        c = canvas.Canvas(str(pdf_path), pagesize=A6)
        for p in patterns_list:
            Pattern(
                filename=str(pdf_path),
                num_shapes=int(p['num_shapes'].value),
                size=int(p['size'].value),
                shape=p['shape'].value,
                can=c,
                circles=int(circles.value),
                lines=int(lines.value),
                col=p['hex'],
                offset=float(p['offset'].value),
                sketch=int(sketch.value)
            )
        c.showPage()
        c.save()
        
        ui.notify(f"Generated {pdf_path.name}!", type='positive')
        current_pdf_path = pdf_path
        
        # --- Update the PDF Viewer Section ---
        # We point the iframe source to the local route we mapped earlier + a timestamp to force refresh
        pdf_viewer.set_visibility(True)
        pdf_frame.props(f'src="/download/{pdf_path.name}?t={time.time()}"')
        
    except Exception as e:
        ui.notify(f"Error: {str(e)}", type='negative')

def delete_current_pdf():
    global current_pdf_path
    if current_pdf_path and current_pdf_path.exists():
        try:
            # 1. Clear iframe source so the browser releases the file lock
            pdf_frame.props('src=""')
            
            # 2. Delete file from local storage
            current_pdf_path.unlink()
            ui.notify(f"Deleted {current_pdf_path.name} successfully.", type='positive')
            
            # 3. Clean up UI state
            current_pdf_path = None
            pdf_viewer.set_visibility(False)
        except Exception as e:
            ui.notify(f"Could not delete file: {str(e)}", type='negative')
    else:
        ui.notify("No generated file found to delete.", type='warning')

def save_current_pdf():
    global current_pdf_path
    global saved
    ui.notify(f"Saved {current_pdf_path.name} successfully.", type='positive')
    pdf_viewer.set_visibility(False)
    filename_input.value = ""

    current_pdf_path = None
    saved = True
    



# --- UI Layout ---
ui.query('body').classes('bg-slate-100')

# Main layout split into a 2-column grid (Left: Controls, Right: PDF Viewer)
with ui.grid(columns='1fr 1fr').classes('w-full max-w-6xl mx-auto my-10 gap-6 p-4'):
    
    # LEFT COLUMN: Controls Card
    with ui.card().classes('p-6 shadow-lg rounded-xl bg-white h-fit'):
        ui.label('PDF Pattern Generator').classes('text-2xl font-bold text-slate-800 mb-2')
        
        filename_input = ui.input(label='Filename', placeholder='output', suffix='.pdf').classes('w-full mb-4')
        
        ui.separator().classes('my-2')
        
        with ui.row().classes('w-full justify-between items-center mb-2'):
            ui.label('Patterns').classes('text-lg font-semibold text-slate-700')
            circles = ui.switch('Circles', value=True)
            lines = ui.switch('Lines', value=True)
            sketch = ui.switch('Sketch', value=False)
            ui.button('Add Row', icon='add', on_click=add_pattern_row).props('outline size=sm color=primary')

        patterns_container = ui.column().classes('w-full gap-3 mb-6')
        with patterns_container:
            add_pattern_row() # Initial default row
            
        ui.button('Generate & View PDF', icon='picture_as_pdf', on_click=generate_pdf).classes('w-full py-2 text-lg').props('color=primary')

    # RIGHT COLUMN: Dynamic PDF Viewer Card
    # It starts hidden and reveals itself the first time you click "Generate"
    with ui.card().classes('p-4 shadow-lg rounded-xl bg-white h-[700px]') as pdf_viewer:
        pdf_viewer.set_visibility(False) 
        ui.label('PDF Preview').classes('text-lg font-bold text-slate-700 mb-2')
        with ui.row():
            ui.button('Delete PDF', icon='delete_forever', on_click=delete_current_pdf).props('flat color=red size=md')
            ui.button('Save PDF', icon='save', on_click=save_current_pdf).props('flat color=green size=md')

        
        # Native HTML iframe configured to fill the card space completely
        pdf_frame = ui.element('iframe').classes('w-full h-full border-none rounded-lg')

# Start NiceGUI
ui.run(title="Pattern Generator & Viewer")