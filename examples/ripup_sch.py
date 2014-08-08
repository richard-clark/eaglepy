"""
Rip Up Schematic
================

Removes every wire, junction, and contact reference on every sheet
in the specified schematic. 

Replace the value of ``input_file_name`` with a schematic which actually exists.

The output will be saved to ``output_file_name``.

"""

from eaglepy import eagle
    
input_file_name = 'eagle.sch'
output_file_name = 'eagle_ripped_up.sch'
    
e = eagle.Eagle.load(input_file_name)

schematic = e.drawing.document

for s in schematic.sheets:
    s.nets.clear()
    
e.save(output_file_name)