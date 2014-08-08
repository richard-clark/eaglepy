"""
Make Schematic (Multiple Sheets)
================================

This creates a new schematic with multiple sheets. Each sheet contains a frame
and a label which indicates the sheet number.

"""

from eaglepy import constants, default_layers, eagle, primitives

schematic_path = 'schem_mult_sheets.sch'
num_sheets = 4
width = constants.UNIT.to_default(11, constants.UNIT.INCH)
height = constants.UNIT.to_default(8.5, constants.UNIT.INCH)
font_size = constants.UNIT.to_default(0.7, constants.UNIT.INCH)

schematic = eagle.Schematic()

for i in range(num_sheets):
    frame = primitives.Frame(0, 0, width, height, constants.LAYERS.NETS)
    
    label = primitives.Text("This is page {0}!".format(i+1), 
                            width/2.0, 
                            height/2.0, 
                            constants.LAYERS.INFO, 
                            font_size, 
                            constants.ALIGN.CENTER)
    
    sheet = eagle.Sheet(plain = [frame, label])
    
    schematic.sheets.append(sheet)

drawing = eagle.Drawing(grid = eagle.Grid(),
                        layers = default_layers.get_layers(),
                        document = schematic)
    
e = eagle.Eagle(drawing)

e.save(schematic_path)