"""
Print Libraries
===============

Print the name of every library referenced in an SCH or BRD file.

Replace the value of ``file_name`` with a board or schematic which actually exists.
 

"""

from eaglepy import eagle

file_name = 'eagle.sch'
# file_name = 'eagle.brd'
e = eagle.Eagle.load(file_name)

for l in e.drawing.document.libraries:
    print(l.name)