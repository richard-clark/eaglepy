"""
Make Board with Outline
=======================

Creates a board with a octagonal outline and saves it to the location specified by
``board_path``.

"""

from eaglepy import constants, default_layers, eagle, primitive_utils

# Constants
board_path = 'board_with_outline.brd'
num_sides = 8
radius = constants.UNIT.to_default(2, constants.UNIT.INCH)
width = constants.UNIT.to_default(0.02, constants.UNIT.INCH)

# Create a board
board = eagle.Board()

# Add the outline
primitive_utils.add_wire_ngon(board.plain_items, 
                              radius, radius, 
                              num_sides, 
                              radius, 
                              width, 
                              constants.LAYERS.DIMENSION)

# Save the board
drawing = eagle.Drawing(grid = eagle.Grid(),
                        layers = default_layers.get_layers(),
                        document = board)

e = eagle.Eagle(drawing)

e.save(board_path)