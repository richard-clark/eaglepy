"""
Make Board
==========

Creates an empty board and saves it to the location specified
by ``board_path``.

"""

from eaglepy import default_layers, eagle

board_path = 'board.brd'

board = eagle.Board()
drawing = eagle.Drawing(grid = eagle.Grid(),
                        layers = default_layers.get_layers(),
                        document = board)
e = eagle.Eagle(drawing)
e.save(board_path)