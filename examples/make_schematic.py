"""
Make Schematic
==============

Creates an empty schematic at the specified location.

"""

from eaglepy import default_layers, eagle

schematic_path = 'schematic.sch'

schematic = eagle.Schematic(sheets = [eagle.Sheet()])

drawing = eagle.Drawing(grid = eagle.Grid(),
                        layers = default_layers.get_layers(),
                        document = schematic)

e = eagle.Eagle(drawing)

e.save(schematic_path)