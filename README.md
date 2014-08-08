EAGLE-Python
============

A Python package for creating, modifying, and writing Cadsoft EAGLE files

Dependencies
------------

For writing EAGLE files, the non-standard Python package [lxml] is required. This can be installed using pip:

	pip install lxml 

If lxml is not available (for example, with IronPython), it is still possible to read EAGLE files, but it is not possible to write EAGLE files. 

Installation
------------

The package can be installed by cloning into the repository and then invoking
``setup.py`` from the source directory:

	python setup.py install
	
This package is also avilable on the [Python Package Index][ppi], and can be installed using pip:

	pip install eaglepy

Basic Usage
-----------

As a basic example, the following will create (and save) an empty schematic:

	from eaglepy import default_layers, eagle

	schematic_path = 'schematic.sch'

	schematic = eagle.Schematic(sheets = [eagle.Sheet()])

	drawing = eagle.Drawing(grid = eagle.Grid(),
		layers = default_layers.get_layers(),
		document = schematic)

	e = eagle.Eagle(drawing)

	e.save(schematic_path)

Documentation
-------------

More extensive documentation is available [here][doc].


There are a number of example modules provided in the ``examples/`` directory.

[lxml]: http://lxml.de/
[ppi]: https://pypi.python.org/pypi/eaglepy
[doc]: http://richard-h-clark.com/projects/eaglepy
