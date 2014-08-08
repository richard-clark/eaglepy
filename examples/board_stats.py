"""
Board Stats
===========

Print the number of pads, vias, SMDs (on both top and bottom), holes, and total drills
for an EAGLE board file.

Inspired by the ``count.ulp`` user-language program provided with EAGLE.

Replace the value of ``input_file`` with a board which actually exists.

"""

from eaglepy import constants, eagle, primitives
    
input_file = 'eagle.brd'

# Parse the board 
e_brd = eagle.Eagle.load(input_file)
board = e_brd.drawing.document

# Variables to hold the board statistics
num_pads = 0
num_vias = 0
num_smds_top = 0
num_smds_bottom = 0
num_holes = 0

# A package can contain holes, pads, and SMDs
for e in board.elements:
    for i in e.package.items:
        if isinstance(i, primitives.Hole):
            num_holes += 1
        elif isinstance(i, primitives.Pad):
            num_pads += 1
        elif isinstance(i, primitives.SMD):
            if e.rotation.mirrored:
                if i.layer == constants.LAYERS.TOP:
                    num_smds_bottom += 1
                elif i.layer == constants.LAYERS.BOTTOM:
                    num_smds_top += 1
            else:
                if i.layer == constants.LAYERS.TOP:
                    num_smds_top += 1
                elif i.layer == constants.LAYERS.BOTTOM:
                    num_smds_bottom += 1
 
# The plain items can contain holes   
for i in board.plain_items:
    if isinstance(i, primitives.Hole):
        num_holes += 1

# The signals can contain vias
for s in board.signals:
    for i in s.items:
        if isinstance(i, primitives.Via):
            num_vias += 1
            
print('Pads: {0}'.format(num_pads))
print('Vias: {0}'.format(num_vias))
print('SMDs: {0}'.format(num_smds_top + num_smds_bottom))
print(' - Top: {0}'.format(num_smds_top))
print(' - Bottom: {0}'.format(num_smds_bottom))
print('Holes: {0}'.format(num_holes))
print('Total drills: {0}'.format(num_holes + num_vias + num_pads))
        