"""
Make Library
============

Creates an empty library with the specified name and location.

"""

from eaglepy import default_layers, eagle

library_name = 'My Library'
library_path = 'library.lbr'

lib = eagle.Library(library_name)

drawing = eagle.Drawing(grid = eagle.Grid(),
                        layers = default_layers.get_layers(),
                        document = lib)
    
e = eagle.Eagle(drawing)

e.save(library_path)