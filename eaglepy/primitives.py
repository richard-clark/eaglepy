"""
Primitives
==========

Primitives are the objects from which packages and symbols are comprised. Boards and schematics, in addition to 
containing packages and symbols, respectively, may also contain symbols.

Each primitive class contains an ``ATTR_MAP`` property, which is used to associate each attribute of that
primitive with an attribute type.

Each primitive class must contain the following:

* A ``TAG_NAME`` property.
* An ``ATTR_MAP`` property.
* A ``parse()`` method which accepts an ElementTree ``Element`` object and returns an instance of the primitive class
  (or None).
* An ``append_node()`` method which accepts a primitive class object and a parent ElementTree ``Element`` and 
  appends an ``Element`` to that parent.

EAGLE stores the descsription for packages and symbols within the list of primitives. This package stores this
data separately. Thus, the Description element is not considered a primitive, and it returns None.

Initialization
--------------

An ElementTree ``Element`` can be converted to its primitive representation using the ``parse_item()`` method. This
method determines whether the ``Element`` has a corresponding primitive representation. If so, it invokes the ``parse()``
method of that primitive; otherwise, ``None`` is returned. Comparisons are made using a dictionary. The dictionary is
populated dynamically (using reflection) when this module is imported.

"""

import attributes
import constants
import inspect
import sys
from xml.etree import ElementTree

class Circle:
    TAG_NAME = constants.TAGS.CIRCLE
    
    DEFAULT_WIDTH = 0.01
    
    ATTR_MAP = { constants.ATTRIBUTES.X: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.Y: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.RADIUS: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.WIDTH: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.LAYER: attributes.ATTR_INT
                }
    
    def __init__(self, x, y, radius, layer, width = DEFAULT_WIDTH):
        self.x = x
        self.y = y
        self.radius = radius
        self.width = width
        self.layer = layer
    
    @classmethod
    def parse(cls, n):
        x = attributes.parse(cls, n, constants.ATTRIBUTES.X)
        y = attributes.parse(cls, n, constants.ATTRIBUTES.Y)
        radius = attributes.parse(cls, n, constants.ATTRIBUTES.RADIUS)
        width = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.WIDTH, cls.DEFAULT_WIDTH)
        layer = attributes.parse(cls, n, constants.ATTRIBUTES.LAYER)
        
        return Circle(x, y, radius, layer, width)
        
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, self.TAG_NAME)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.X, self.x)
        attributes.set_attr(self, n, constants.ATTRIBUTES.Y, self.y)
        attributes.set_attr(self, n, constants.ATTRIBUTES.RADIUS, self.radius)
        attributes.set_attr(self, n, constants.ATTRIBUTES.LAYER, self.layer)
        attributes.set_attr(self, n, constants.ATTRIBUTES.WIDTH, self.width)
    
class Contact_Ref:
    TAG_NAME = constants.TAGS.CONTACT_REF
    
    DEFAULT_ROUTE = None
    DEFAULT_ROUTE_TAG = None
    
    ATTR_MAP = {constants.ATTRIBUTES.ELEMENT: attributes.ATTR_STRING,
                constants.ATTRIBUTES.PAD: attributes.ATTR_STRING,
                constants.ATTRIBUTES.ROUTE: attributes.ATTR_STRING,
                constants.ATTRIBUTES.ROUTE_TAG: attributes.ATTR_STRING
                }
          
    def __init__(self, element, pad, route = DEFAULT_ROUTE, route_tag = DEFAULT_ROUTE_TAG):
        self.element = element
        self.pad = pad
        self.route = route
        self.route_tag = route_tag
        
    @classmethod
    def parse(cls, n):
        element = attributes.parse(cls, n, constants.ATTRIBUTES.ELEMENT)
        pad = attributes.parse(cls, n, constants.ATTRIBUTES.PAD)
        route = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.ROUTE, cls.DEFAULT_ROUTE)
        route_tag = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.ROUTE_TAG, cls.DEFAULT_ROUTE_TAG)
        
        return Contact_Ref(element, pad, route, route_tag)
          
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, self.TAG_NAME)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.ELEMENT, self.element)
        attributes.set_attr(self, n, constants.ATTRIBUTES.PAD, self.pad)
        attributes.set_attr(self, n, constants.ATTRIBUTES.ROUTE, self.route, self.DEFAULT_ROUTE)
        attributes.set_attr(self, n, constants.ATTRIBUTES.ROUTE_TAG, self.route_tag, self.DEFAULT_ROUTE_TAG)
          
"""
Descriptions are added to the enclosing tags, so this primitive is not used. 
"""
class Description:
    TAG_NAME = constants.TAGS.DESCRIPTION
    
    @classmethod
    def parse(cls, n):
        return None
         
class Dimension:
    TAG_NAME = constants.TAGS.DIMENSION
    
    DEFAULT_DIMENSION_TYPE = constants.DIMENSION_TYPE.PARALLEL
    DEFAULT_TEXT_SIZE = 0.1 * 25.4
    DEFAULT_TEXT_RATIO = 8
    DEFAULT_UNIT = constants.UNIT.MM
    DEFAULT_PRECISION = 2
    DEFAULT_WIDTH = 0.13
    DEFAULT_EXT_WIDTH = None
    DEFAULT_EXT_LENGTH = None
    DEFAULT_EXT_OFFSET = None
    DEFAULT_UNIT_VISIBLE = False
    
    ATTR_MAP = { constants.ATTRIBUTES.X1: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.Y1: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.X2: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.Y2: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.X3: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.Y3: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.TEXT_SIZE: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.TEXT_RATIO: attributes.ATTR_INT,
                
                
                
                }
    
    def __init__(self, x1, y1, x2, y2, x3, y3, layer, text_size = DEFAULT_TEXT_SIZE, text_ratio = DEFAULT_TEXT_RATIO,
                 dimension_type = DEFAULT_DIMENSION_TYPE, width = DEFAULT_WIDTH,
                 ext_width = DEFAULT_EXT_WIDTH, ext_length = DEFAULT_EXT_LENGTH,
                 ext_offset = DEFAULT_EXT_OFFSET, unit = DEFAULT_UNIT, precision = DEFAULT_PRECISION,
                 unit_visible = DEFAULT_UNIT_VISIBLE):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        self.layer = layer
        self.text_size = text_size
        self.text_ratio = text_ratio
        self.dimension_type = dimension_type
        self.width = width
        self.ext_width = ext_width
        self.ext_length = ext_length
        self.ext_offset = ext_offset
        self.unit = unit
        self.precision = precision
        self.unit_visible = unit_visible
        
    @classmethod
    def parse(cls, n):
        x1 = attributes.parse(cls, n, constants.ATTRIBUTES.X1)
        y1 = attributes.parse(cls, n, constants.ATTRIBUTES.Y1)
        x2 = attributes.parse(cls, n, constants.ATTRIBUTES.X2)
        y2 = attributes.parse(cls, n, constants.ATTRIBUTES.Y2)
        x3 = attributes.parse(cls, n, constants.ATTRIBUTES.X3)
        y3 = attributes.parse(cls, n, constants.ATTRIBUTES.Y3)
        layer = attributes.parse(cls, n, constants.ATTRIBUTES.LAYER)
        text_size = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.TEXT_SIZE, cls.DEFAULT_TEXT_SIZE)
        text_ratio = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.TEXT_RATIO, cls.DEFAULT_TEXT_RATIO)
        dimension_type = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.DIMENSION_TYPE, cls.DEFAULT_DIMENSION_TYPE)
        width = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.WIDTH, cls.DEFAULT_WIDTH)
        ext_width = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.EXT_WIDTH, cls.DEFAULT_EXT_WIDTH)
        ext_length = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.EXT_LENGTH, cls.DEFAULT_EXT_LENGTH)
        ext_offset = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.EXT_OFFSET, cls.DEFAULT_EXT_OFFSET)
        unit = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.UNIT, cls.DEFAULT_UNIT)
        precision = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.PRECISION, cls.DEFAULT_PRECISION)
        unit_visible = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.VISIBLE, cls.DEFAULT_UNIT_VISIBLE)
        
        return Dimension(x1, y1, x2, y2, x3, y3, layer, text_size, text_ratio, dimension_type, width, ext_width, ext_length, ext_offset, unit, precision, unit_visible)
        
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, self.TAG_NAME)
     
        attributes.set_attr(self, n, constants.ATTRIBUTES.X1, self.x1)
        attributes.set_attr(self, n, constants.ATTRIBUTES.Y1, self.y1)
        attributes.set_attr(self, n, constants.ATTRIBUTES.X2, self.x2)
        attributes.set_attr(self, n, constants.ATTRIBUTES.Y2, self.y2)
        attributes.set_attr(self, n, constants.ATTRIBUTES.X3, self.x3)
        attributes.set_attr(self, n, constants.ATTRIBUTES.Y3, self.y3)
        attributes.set_attr(self, n, constants.ATTRIBUTES.LAYER, self.layer)
        attributes.set_attr(self, n, constants.ATTRIBUTES.TEXT_SIZE, self.text_size, self.DEFAULT_TEXT_SIZE)
        attributes.set_attr(self, n, constants.ATTRIBUTES.TEXT_RATIO, self.text_ratio, self.DEFAULT_TEXT_RATIO)
        attributes.set_attr(self, n, constants.ATTRIBUTES.DIMENSION_TYPE, self.dimension_type, self.DEFAULT_DIMENSION_TYPE)
        attributes.set_attr(self, n, constants.ATTRIBUTES.WIDTH, self.width, self.DEFAULT_WIDTH)
        attributes.set_attr(self, n, constants.ATTRIBUTES.EXT_WIDTH, self.ext_width, self.DEFAULT_EXT_WIDTH)
        attributes.set_attr(self, n, constants.ATTRIBUTES.EXT_LENGTH, self.ext_length, self.DEFAULT_EXT_LENGTH)
        attributes.set_attr(self, n, constants.ATTRIBUTES.EXT_OFFSET, self.ext_offset, self.DEFAULT_EXT_OFFSET)
        attributes.set_attr(self, n, constants.ATTRIBUTES.UNIT, self.unit, self.DEFAULT_UNIT)
        attributes.set_attr(self, n, constants.ATTRIBUTES.PRECISION, self.precision, self.DEFAULT_PRECISION)
        attributes.set_attr(self, n, constants.ATTRIBUTES.VISIBLE, self.unit_visible, self.DEFAULT_UNIT_VISIBLE)
     
         
class Frame:
    TAG_NAME = constants.TAGS.FRAME
    
    DEFAULT_ROWS = 5
    DEFAULT_COLUMNS = 8
    DEFAULT_BORDER_TOP = True
    DEFAULT_BORDER_BOTTOM = True
    DEFAULT_BORDER_LEFT = True
    DEFAULT_BORDER_RIGHT = True
    
    ATTR_MAP = {constants.ATTRIBUTES.X1: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.Y1: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.X2: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.Y2: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.COLUMNS: attributes.ATTR_INT,
                constants.ATTRIBUTES.ROWS: attributes.ATTR_INT,
                constants.ATTRIBUTES.LAYER: attributes.ATTR_INT,
                constants.ATTRIBUTES.BORDER.BOTTOM: attributes.ATTR_BOOL,
                constants.ATTRIBUTES.BORDER.LEFT: attributes.ATTR_BOOL,
                constants.ATTRIBUTES.BORDER.RIGHT: attributes.ATTR_BOOL,
                constants.ATTRIBUTES.BORDER.TOP: attributes.ATTR_BOOL,
                
                }
          
    def __init__(self, x1, y1, x2, y2, layer, rows = DEFAULT_ROWS, columns = DEFAULT_COLUMNS, border_left = DEFAULT_BORDER_LEFT,
                 border_top = DEFAULT_BORDER_TOP, border_right = DEFAULT_BORDER_RIGHT, border_bottom = DEFAULT_BORDER_BOTTOM):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.layer = layer
        self.rows = rows
        self.columns = columns
        
        self.border_top = border_top
        self.border_left = border_left
        self.border_bottom = border_bottom
        self.border_right = border_right
        

    @classmethod
    def parse(cls, n):
        x1 = attributes.parse(cls, n, constants.ATTRIBUTES.X1)
        y1 = attributes.parse(cls, n, constants.ATTRIBUTES.Y1)
        x2 = attributes.parse(cls, n, constants.ATTRIBUTES.X2)
        y2 = attributes.parse(cls, n, constants.ATTRIBUTES.Y2)
        rows = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.ROWS, cls.DEFAULT_ROWS)
        columns = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.COLUMNS, cls.DEFAULT_COLUMNS)
        layer = attributes.parse(cls, n, constants.ATTRIBUTES.LAYER)
        
        border_top = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.BORDER.TOP, cls.DEFAULT_BORDER_TOP)
        border_left = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.BORDER.LEFT, cls.DEFAULT_BORDER_LEFT)
        border_bottom = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.BORDER.BOTTOM, cls.DEFAULT_BORDER_BOTTOM)
        border_right = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.BORDER.RIGHT, cls.DEFAULT_BORDER_RIGHT)
        
        return Frame(x1, y1, x2, y2, layer, rows, columns, border_left, border_top, border_right, border_bottom)
          
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, self.TAG_NAME)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.X1, self.x1)
        attributes.set_attr(self, n, constants.ATTRIBUTES.Y1, self.y1)
        attributes.set_attr(self, n, constants.ATTRIBUTES.X2, self.x2)
        attributes.set_attr(self, n, constants.ATTRIBUTES.Y2, self.y2)
        attributes.set_attr(self, n, constants.ATTRIBUTES.ROWS, self.rows)
        attributes.set_attr(self, n, constants.ATTRIBUTES.COLUMNS, self.columns)
        attributes.set_attr(self, n, constants.ATTRIBUTES.LAYER, self.layer)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.BORDER.TOP, self.border_top, self.DEFAULT_BORDER_TOP)
        attributes.set_attr(self, n, constants.ATTRIBUTES.BORDER.LEFT, self.border_left, self.DEFAULT_BORDER_LEFT)
        attributes.set_attr(self, n, constants.ATTRIBUTES.BORDER.BOTTOM, self.border_bottom, self.DEFAULT_BORDER_BOTTOM)
        attributes.set_attr(self, n, constants.ATTRIBUTES.BORDER.RIGHT, self.border_right, self.DEFAULT_BORDER_RIGHT)
        
class Hole:
    TAG_NAME = constants.TAGS.HOLE
    
    ATTR_MAP = {constants.ATTRIBUTES.X: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.Y: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.DRILL: attributes.ATTR_FLOAT
                }
    
    def __init__(self, x, y, drill):
        self.x = x
        self.y = y
        self.drill = drill
        
    @classmethod
    def parse(cls, n):
        x = attributes.parse(cls, n, constants.ATTRIBUTES.X)
        y = attributes.parse(cls, n, constants.ATTRIBUTES.Y)
        drill = attributes.parse(cls, n, constants.ATTRIBUTES.DRILL)
        
        return Hole(x, y, drill)
    
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, self.TAG_NAME)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.X, self.x)
        attributes.set_attr(self, n, constants.ATTRIBUTES.Y, self.y)
        attributes.set_attr(self, n, constants.ATTRIBUTES.DRILL, self.drill)
   
class Junction:
    TAG_NAME = constants.TAGS.JUNCTION
    
    ATTR_MAP = {constants.ATTRIBUTES.X: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.Y: attributes.ATTR_FLOAT}
        
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    @classmethod
    def parse(cls, n):
        x = attributes.parse(cls, n, constants.ATTRIBUTES.X)
        y = attributes.parse(cls, n, constants.ATTRIBUTES.Y)
        
        return Junction(x, y)
    
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, self.TAG_NAME)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.X, self.x)
        attributes.set_attr(self, n, constants.ATTRIBUTES.Y, self.y)
        
class Label:
    TAG_NAME = constants.TAGS.LABEL
    
    DEFAULT_XREF = False
    DEFAULT_FONT = constants.FONT.PROPORTIONAL
    DEFAULT_RATIO = 8
    
    ATTR_MAP = {constants.ATTRIBUTES.X: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.Y: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.SIZE: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.LAYER: attributes.ATTR_INT,
                constants.ATTRIBUTES.ROTATION: attributes.ATTR_ROT,
                constants.ATTRIBUTES.XREF: attributes.ATTR_BOOL,
                constants.ATTRIBUTES.FONT: attributes.ATTR_STRING,
                constants.ATTRIBUTES.RATIO: attributes.ATTR_INT
                }
    
    def __init__(self, x, y, size, layer, xref, rotation = attributes.Rotation(0), font = DEFAULT_FONT, ratio = DEFAULT_RATIO):
        self.x = x
        self.y = y
        self.size = size
        self.layer = layer
        self.xref = xref
        self.rotation = rotation
        self.font = font
        self.ratio = ratio
        
    @classmethod
    def parse(cls, n):
        x = attributes.parse(cls, n, constants.ATTRIBUTES.X)
        y = attributes.parse(cls, n, constants.ATTRIBUTES.Y)
        size = attributes.parse(cls, n, constants.ATTRIBUTES.SIZE)
        layer = attributes.parse(cls, n, constants.ATTRIBUTES.LAYER)
        xref = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.XREF, cls.DEFAULT_XREF)
        rotation = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.ROTATION, attributes.Rotation(0))
        font = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.FONT, cls.DEFAULT_FONT)
        ratio = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.RATIO, cls.DEFAULT_RATIO)
        
        return Label(x, y, size, layer, xref, rotation, font, ratio)
        
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, self.TAG_NAME)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.X, self.x)
        attributes.set_attr(self, n, constants.ATTRIBUTES.Y, self.y)
        attributes.set_attr(self, n, constants.ATTRIBUTES.SIZE, self.size)
        attributes.set_attr(self, n, constants.ATTRIBUTES.LAYER, self.layer)
        attributes.set_attr(self, n, constants.ATTRIBUTES.XREF, self.xref, self.DEFAULT_XREF)
        attributes.set_attr(self, n, constants.ATTRIBUTES.ROTATION, self.rotation, attributes.Rotation(0))
        attributes.set_attr(self, n, constants.ATTRIBUTES.FONT, self.font, self.DEFAULT_FONT)
        attributes.set_attr(self, n, constants.ATTRIBUTES.RATIO, self.ratio, self.DEFAULT_RATIO)
        
class Pad:
    TAG_NAME = constants.TAGS.PAD
    
    DEFAULT_SHAPE = constants.SHAPE.ROUND
    DEFAULT_FIRST = False
    DEFAULT_STOP = True
    DEFAULT_THERMALS = True
    
    ATTR_MAP = {constants.ATTRIBUTES.NAME: attributes.ATTR_STRING,
                constants.ATTRIBUTES.X: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.Y: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.DRILL: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.DIAMETER: attributes.ATTR_AUTO_FLOAT,
                constants.ATTRIBUTES.ROTATION: attributes.ATTR_ROT,
                constants.ATTRIBUTES.SHAPE: attributes.ATTR_STRING,
                constants.ATTRIBUTES.FIRST: attributes.ATTR_BOOL,
                constants.ATTRIBUTES.STOP: attributes.ATTR_BOOL,
                constants.ATTRIBUTES.THERMALS: attributes.ATTR_BOOL}
    
    def __init__(self, name, x, y, drill, diameter = None, rotation = attributes.Rotation(), shape = DEFAULT_SHAPE, first = DEFAULT_FIRST, stop = DEFAULT_STOP, thermals = DEFAULT_THERMALS):
        self.name = name
        self.x = x
        self.y = y
        self.drill = drill
        self.diameter = diameter
        self.rotation = rotation
        self.shape = shape
        self.first = first
        self.stop = stop
        self.thermals = thermals
    
    @classmethod
    def parse(cls, n):
        name = attributes.parse(cls, n, constants.ATTRIBUTES.NAME)
        x = attributes.parse(cls, n, constants.ATTRIBUTES.X)
        y = attributes.parse(cls, n, constants.ATTRIBUTES.Y)
        drill = attributes.parse(cls, n, constants.ATTRIBUTES.DRILL)
        diameter = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.DIAMETER, None)
        rotation = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.ROTATION, attributes.Rotation())
        shape = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.SHAPE, cls.DEFAULT_SHAPE)
        first = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.FIRST, cls.DEFAULT_FIRST)
        stop = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.STOP, cls.DEFAULT_STOP)
        thermals = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.THERMALS, cls.DEFAULT_THERMALS)
        
        return Pad(name, x, y, drill, diameter, rotation, shape, first, stop, thermals)
    
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, self.TAG_NAME)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.NAME, self.name)
        attributes.set_attr(self, n, constants.ATTRIBUTES.X, self.x)
        attributes.set_attr(self, n, constants.ATTRIBUTES.Y, self.y)
        attributes.set_attr(self, n, constants.ATTRIBUTES.DRILL, self.drill)
        attributes.set_attr(self, n, constants.ATTRIBUTES.DIAMETER, self.diameter)
        attributes.set_attr(self, n, constants.ATTRIBUTES.ROTATION, self.rotation, attributes.Rotation())
        attributes.set_attr(self, n, constants.ATTRIBUTES.SHAPE, self.shape, self.DEFAULT_SHAPE)
        attributes.set_attr(self, n, constants.ATTRIBUTES.FIRST, self.first, self.DEFAULT_FIRST)
        attributes.set_attr(self, n, constants.ATTRIBUTES.STOP, self.stop, self.DEFAULT_STOP)
        attributes.set_attr(self, n, constants.ATTRIBUTES.THERMALS, self.thermals, self.DEFAULT_THERMALS)
        
class Pin:
    TAG_NAME = constants.TAGS.PIN
    
    DEFAULT_VISIBLE = constants.PIN.VISIBLE.BOTH
    DEFAULT_LENGTH = constants.PIN.LENGTH.LONG
    DEFAULT_SWAP_LEVEL = 0
    DEFAULT_DIRECTION = 'io'
    DEFAULT_FUNCTION = constants.PIN.FUNCTION.NONE
    
    ATTR_MAP = {constants.ATTRIBUTES.NAME: attributes.ATTR_STRING,
                constants.ATTRIBUTES.X: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.Y: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.VISIBLE: attributes.ATTR_STRING,
                constants.ATTRIBUTES.SWAP_LEVEL: attributes.ATTR_INT,
                constants.ATTRIBUTES.ROTATION: attributes.ATTR_ROT,
                constants.ATTRIBUTES.LENGTH: attributes.ATTR_STRING,
                constants.ATTRIBUTES.DIRECTION: attributes.ATTR_STRING,
                constants.ATTRIBUTES.FUNCTION: attributes.ATTR_STRING
                }

    def __init__(self, name, 
                 x, 
                 y, 
                 visible = DEFAULT_VISIBLE, 
                 swap_level = DEFAULT_SWAP_LEVEL, 
                 rotation = attributes.Rotation(), 
                 length = DEFAULT_LENGTH,
                 direction = DEFAULT_DIRECTION,
                 function = DEFAULT_FUNCTION):
        self.name = name
        self.x = x
        self.y = y
        self.visible = visible
        self.swap_level = swap_level
        self.rotation = rotation
        self.length = length
        self.direction = direction
        self.function = function
        
    @classmethod
    def parse(cls, n):
        name = attributes.parse(cls, n, constants.ATTRIBUTES.NAME)
        x = attributes.parse(cls, n, constants.ATTRIBUTES.X)
        y = attributes.parse(cls, n, constants.ATTRIBUTES.Y)
        visible = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.VISIBLE, cls.DEFAULT_VISIBLE)
        swap_level = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.SWAP_LEVEL, cls.DEFAULT_SWAP_LEVEL)
        rotation = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.ROTATION, attributes.Rotation())
        length = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.LENGTH, cls.DEFAULT_LENGTH)
        direction = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.DIRECTION, cls.DEFAULT_DIRECTION)
        function = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.FUNCTION, cls.DEFAULT_FUNCTION)
        
        return Pin(name, x, y, visible, swap_level, rotation, length, direction, function)
        
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, self.TAG_NAME)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.X, self.x)
        attributes.set_attr(self, n, constants.ATTRIBUTES.Y, self.y)
        attributes.set_attr(self, n, constants.ATTRIBUTES.NAME, self.name)
        attributes.set_attr(self, n, constants.ATTRIBUTES.VISIBLE, self.visible, self.DEFAULT_VISIBLE)
        attributes.set_attr(self, n, constants.ATTRIBUTES.SWAP_LEVEL, self.swap_level, self.DEFAULT_SWAP_LEVEL)
        attributes.set_attr(self, n, constants.ATTRIBUTES.ROTATION, self.rotation, attributes.Rotation())
        attributes.set_attr(self, n, constants.ATTRIBUTES.LENGTH, self.length, self.DEFAULT_LENGTH)
        attributes.set_attr(self, n, constants.ATTRIBUTES.DIRECTION, self.direction, self.DEFAULT_DIRECTION)
        attributes.set_attr(self, n, constants.ATTRIBUTES.FUNCTION, self.function, self.DEFAULT_FUNCTION)

class Pin_Ref:
    TAG_NAME = constants.TAGS.PIN_REF
    
    ATTR_MAP = {constants.ATTRIBUTES.PART: attributes.ATTR_STRING,
                constants.ATTRIBUTES.GATE: attributes.ATTR_STRING,
                constants.ATTRIBUTES.PIN: attributes.ATTR_STRING
                }
    
    def __init__(self, part, gate, pin):
        self.part = part
        self.gate = gate
        self.pin = pin
        
    @classmethod
    def parse(cls, n):
        part = attributes.parse(cls, n, constants.ATTRIBUTES.PART)
        gate = attributes.parse(cls, n, constants.ATTRIBUTES.GATE)
        pin = attributes.parse(cls, n, constants.ATTRIBUTES.PIN)

        return Pin_Ref(part, gate, pin)

    def append_node(self, _n):
        n = ElementTree.SubElement(_n, self.TAG_NAME)

        attributes.set_attr(self, n, constants.ATTRIBUTES.PART, self.part)
        attributes.set_attr(self, n, constants.ATTRIBUTES.GATE, self.gate)
        attributes.set_attr(self, n, constants.ATTRIBUTES.PIN, self.pin)
        

class Polygon:
    TAG_NAME = constants.TAGS.POLYGON
    
    DEFAULT_WIDTH = 0.01
    DEFAULT_RANK = 1
    DEFAULT_SPACING = 0.05*25.4
    DEFAULT_POUR = constants.POUR.SOLID
    DEFAULT_ISOLATE = 0
    DEFAULT_ORPHANS = False
    DEFAULT_THERMALS = True
    
    ATTR_MAP = {constants.ATTRIBUTES.LAYER: attributes.ATTR_INT,
                constants.ATTRIBUTES.WIDTH: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.X: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.Y: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.RANK: attributes.ATTR_INT,
                constants.ATTRIBUTES.SPACING: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.POUR: attributes.ATTR_STRING,
                constants.ATTRIBUTES.ISOLATE: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.ORPHANS: attributes.ATTR_BOOL,
                constants.ATTRIBUTES.THERMALS: attributes.ATTR_BOOL}
    
    def __init__(self, layer, points = [], width = DEFAULT_WIDTH, rank = DEFAULT_RANK, spacing = DEFAULT_SPACING, pour = DEFAULT_POUR, isolate = DEFAULT_ISOLATE,
                 orphans = DEFAULT_ORPHANS, thermals = DEFAULT_THERMALS):
        self.layer = layer
        self.points = points
        self.width = width
        self.rank = rank
        self.spacing = spacing
        self.pour = pour
        self.isolate = isolate
        self.orphans = orphans
        self.thermals = thermals
        
    @classmethod
    def parse(cls, n):
        layer = attributes.parse(cls, n, constants.ATTRIBUTES.LAYER)
        width = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.WIDTH, cls.DEFAULT_WIDTH)
        rank = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.RANK, cls.DEFAULT_RANK)
        spacing = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.SPACING, cls.DEFAULT_SPACING)
        pour = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.POUR, cls.DEFAULT_POUR)
        isolate = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.ISOLATE, cls.DEFAULT_ISOLATE)
        orphans = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.ORPHANS, cls.DEFAULT_ORPHANS)
        thermals = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.THERMALS, cls.DEFAULT_THERMALS)
        
        # Get the points
        n_vertex_arr = n.findall(constants.TAGS.VERTEX)
        points = []
        
        for nv in n_vertex_arr:
            x = attributes.parse(cls, nv, constants.ATTRIBUTES.X)
            y = attributes.parse(cls, nv, constants.ATTRIBUTES.Y)
            curve = attributes.parse_or_default(cls, nv, constants.ATTRIBUTES.CURVE, 0)
            points.append((x, y, curve))
        
        return Polygon(layer, points = points, width = width, rank = rank, spacing = spacing, pour = pour, isolate = isolate,
                       orphans = orphans, thermals = thermals)
            
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, self.TAG_NAME)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.WIDTH, self.width)
        attributes.set_attr(self, n, constants.ATTRIBUTES.LAYER, self.layer)
        attributes.set_attr(self, n, constants.ATTRIBUTES.RANK, self.rank, self.DEFAULT_RANK)
        attributes.set_attr(self, n, constants.ATTRIBUTES.SPACING, self.spacing, self.DEFAULT_SPACING)
        attributes.set_attr(self, n, constants.ATTRIBUTES.POUR, self.pour, self.DEFAULT_POUR)
        attributes.set_attr(self, n, constants.ATTRIBUTES.ISOLATE, self.isolate, self.DEFAULT_ISOLATE)
        attributes.set_attr(self, n, constants.ATTRIBUTES.ORPHANS, self.orphans, self.DEFAULT_ORPHANS)
        attributes.set_attr(self, n, constants.ATTRIBUTES.THERMALS, self.thermals, self.DEFAULT_THERMALS)
        
        for p in self.points:
            n_vertex = ElementTree.SubElement(n, constants.TAGS.VERTEX)
            attributes.set_attr(self, n_vertex, constants.ATTRIBUTES.X, p[0])
            attributes.set_attr(self, n_vertex, constants.ATTRIBUTES.Y, p[1])
            attributes.set_attr(self, n_vertex, constants.ATTRIBUTES.CURVE, p[2], 0)
            
class Rectangle:
    TAG_NAME = constants.TAGS.RECTANGLE
    
    ATTR_MAP = { constants.ATTRIBUTES.X1: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.Y1: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.X2: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.Y2: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.LAYER: attributes.ATTR_INT,
                constants.ATTRIBUTES.ROTATION: attributes.ATTR_ROT
                }
    
    def __init__(self, x1, y1, x2, y2, layer, rotation = attributes.Rotation(0)):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.layer = layer
        self.rotation = rotation
        
    @classmethod
    def parse(cls, n):
        x1 = attributes.parse(cls, n, constants.ATTRIBUTES.X1)
        y1 = attributes.parse(cls, n, constants.ATTRIBUTES.Y1)
        x2 = attributes.parse(cls, n, constants.ATTRIBUTES.X2)
        y2 = attributes.parse(cls, n, constants.ATTRIBUTES.Y2)
        layer = attributes.parse(cls, n, constants.ATTRIBUTES.LAYER)
        rotation = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.ROTATION, attributes.Rotation(0))
        
        return Rectangle(x1, y1, x2, y2, layer, rotation)
    
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, self.TAG_NAME)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.X1, self.x1)
        attributes.set_attr(self, n, constants.ATTRIBUTES.Y1, self.y1)
        attributes.set_attr(self, n, constants.ATTRIBUTES.X2, self.x2)
        attributes.set_attr(self, n, constants.ATTRIBUTES.Y2, self.y2)
        attributes.set_attr(self, n, constants.ATTRIBUTES.LAYER, self.layer)
        attributes.set_attr(self, n, constants.ATTRIBUTES.ROTATION, self.rotation, attributes.Rotation(0))
        
class SMD:
    TAG_NAME = constants.TAGS.SMD
    
    DEFAULT_CREAM = True
    DEFAULT_ROUNDNESS = 0
    DEFAULT_STOP = True
    DEFAULT_THERMALS = True
    DEFAULT_FIRST = False
    
    ATTR_MAP = {constants.ATTRIBUTES.NAME: attributes.ATTR_STRING,
                constants.ATTRIBUTES.X: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.Y: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.DX: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.DY: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.LAYER: attributes.ATTR_INT,
                constants.ATTRIBUTES.ROTATION: attributes.ATTR_ROT,
                constants.ATTRIBUTES.ROUNDNESS: attributes.ATTR_INT,
                constants.ATTRIBUTES.CREAM: attributes.ATTR_BOOL,
                constants.ATTRIBUTES.FIRST: attributes.ATTR_BOOL,
                constants.ATTRIBUTES.STOP: attributes.ATTR_BOOL,
                constants.ATTRIBUTES.THERMALS: attributes.ATTR_BOOL
                }
    
    def __init__(self, name, x, y, dx, dy, layer, rotation = attributes.Rotation(), roundness = DEFAULT_ROUNDNESS, cream = DEFAULT_CREAM, first = DEFAULT_FIRST, stop = DEFAULT_STOP, thermals = DEFAULT_THERMALS):
        self.name = name
        self.x = x 
        self.y = y
        self.dx = dx
        self.dy = dy
        self.layer = layer
        self.rotation = rotation
        self.roundness = roundness
        self.cream = cream
        self.first = first
        self.stop = stop
        self.thermals = thermals
        
    @classmethod
    def parse(cls, n):
        name = attributes.parse(cls, n, constants.ATTRIBUTES.NAME)
        x = attributes.parse(cls, n, constants.ATTRIBUTES.X)
        y = attributes.parse(cls, n, constants.ATTRIBUTES.Y)
        dx = attributes.parse(cls, n, constants.ATTRIBUTES.DX)
        dy = attributes.parse(cls, n, constants.ATTRIBUTES.DY)
        layer = attributes.parse(cls, n, constants.ATTRIBUTES.LAYER)
        rotation = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.ROTATION, attributes.Rotation())
        roundness = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.ROUNDNESS, cls.DEFAULT_ROUNDNESS)
        cream = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.CREAM, cls.DEFAULT_CREAM)
        first = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.FIRST, cls.DEFAULT_FIRST)
        stop = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.STOP, cls.DEFAULT_STOP)
        thermals = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.THERMALS, cls.DEFAULT_THERMALS)
        
        return SMD(name, x, y, dx, dy, layer, rotation, roundness, cream, first, stop, thermals)

    def append_node(self, _n):
        n = ElementTree.SubElement(_n, self.TAG_NAME)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.NAME, self.name)
        attributes.set_attr(self, n, constants.ATTRIBUTES.X, self.x)
        attributes.set_attr(self, n, constants.ATTRIBUTES.Y, self.y)
        attributes.set_attr(self, n, constants.ATTRIBUTES.DX, self.dx)
        attributes.set_attr(self, n, constants.ATTRIBUTES.DY, self.dy)
        attributes.set_attr(self, n, constants.ATTRIBUTES.LAYER, self.layer)
        attributes.set_attr(self, n, constants.ATTRIBUTES.ROTATION, self.rotation, attributes.Rotation())
        attributes.set_attr(self, n, constants.ATTRIBUTES.ROUNDNESS, self.roundness, self.DEFAULT_ROUNDNESS)
        attributes.set_attr(self, n, constants.ATTRIBUTES.CREAM, self.cream, self.DEFAULT_CREAM)
        attributes.set_attr(self, n, constants.ATTRIBUTES.FIRST, self.first, self.DEFAULT_FIRST)
        attributes.set_attr(self, n, constants.ATTRIBUTES.STOP, self.stop, self.DEFAULT_STOP)
        attributes.set_attr(self, n, constants.ATTRIBUTES.THERMALS, self.thermals, self.DEFAULT_THERMALS)

class Text:
    TAG_NAME = constants.TAGS.TEXT
    
    DEFAULT_SIZE = 1.27
    DEFAULT_ALIGN = constants.ALIGN.BOTTOM_LEFT
    DEFAULT_FONT = constants.FONT.PROPORTIONAL
    DEFAULT_RATIO = 8
    DEFAULT_DISTANCE = 25
    DEFAULT_SPIN = False
    
    ATTR_MAP = { constants.ATTRIBUTES.X: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.Y: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.SIZE: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.LAYER: attributes.ATTR_INT,
                constants.ATTRIBUTES.ALIGN: attributes.ATTR_STRING,
                constants.ATTRIBUTES.FONT: attributes.ATTR_STRING,
                constants.ATTRIBUTES.ROTATION: attributes.ATTR_ROT,
                constants.ATTRIBUTES.RATIO: attributes.ATTR_INT,
                constants.ATTRIBUTES.DISTANCE: attributes.ATTR_INT,
                constants.ATTRIBUTES.SPIN: attributes.ATTR_BOOL
                }
    
    def __init__(self, value, 
                 x, 
                 y, 
                 layer, 
                 size = DEFAULT_SIZE, 
                 align = DEFAULT_ALIGN, 
                 font = DEFAULT_FONT,
                 rotation = attributes.Rotation(0),
                 ratio = DEFAULT_RATIO,
                 distance = DEFAULT_DISTANCE,
                 spin = DEFAULT_SPIN):
        self.value = value
        self.x = x
        self.y = y
        self.size = size
        self.layer = layer
        self.align = align
        self.font = font
        self.rotation = rotation
        self.ratio = ratio
        self.distance = distance
        self.spin = spin
        
    @classmethod
    def parse(cls, n):
        
        value = n.text
        
        x = attributes.parse(cls, n, constants.ATTRIBUTES.X)
        y = attributes.parse(cls, n, constants.ATTRIBUTES.Y)
        layer = attributes.parse(cls, n, constants.ATTRIBUTES.LAYER)
        size = attributes.parse(cls, n, constants.ATTRIBUTES.SIZE)
        align = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.ALIGN, cls.DEFAULT_ALIGN)
        font = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.FONT, cls.DEFAULT_FONT)
        rotation = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.ROTATION, attributes.Rotation())
        ratio = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.RATIO, cls.DEFAULT_RATIO)
        distance = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.DISTANCE, cls.DEFAULT_DISTANCE)
        spin = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.SPIN, cls.DEFAULT_SPIN)
        
        return Text(value, x, y, layer, size, align, font, rotation, ratio, distance, spin)
    
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, self.TAG_NAME)
        n.text = self.value
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.X, self.x)
        attributes.set_attr(self, n, constants.ATTRIBUTES.Y, self.y)
        attributes.set_attr(self, n, constants.ATTRIBUTES.LAYER, self.layer)
        attributes.set_attr(self, n, constants.ATTRIBUTES.SIZE, self.size)
        attributes.set_attr(self, n, constants.ATTRIBUTES.FONT, self.font, self.DEFAULT_FONT)
        attributes.set_attr(self, n, constants.ATTRIBUTES.ALIGN, self.align, self.DEFAULT_ALIGN)
        attributes.set_attr(self, n, constants.ATTRIBUTES.RATIO, self.ratio, self.DEFAULT_RATIO)
        attributes.set_attr(self, n, constants.ATTRIBUTES.ROTATION, self.rotation, attributes.Rotation(0))
        attributes.set_attr(self, n, constants.ATTRIBUTES.DISTANCE, self.distance, self.DEFAULT_DISTANCE)
        attributes.set_attr(self, n, constants.ATTRIBUTES.SPIN, self.spin, self.DEFAULT_SPIN)

  
class Via:
    TAG_NAME = constants.TAGS.VIA
    
    DEFAULT_EXTENT = None
    DEFAULT_ALWAYS_STOP = False
    DEFAULT_SHAPE = constants.SHAPE.ROUND
    
    ATTR_MAP = { constants.ATTRIBUTES.X: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.Y: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.DRILL: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.DIAMETER: attributes.ATTR_AUTO_FLOAT,
                constants.ATTRIBUTES.ROTATION: attributes.ATTR_ROT,
                constants.ATTRIBUTES.EXTENT: attributes.ATTR_EXTENT,
                constants.ATTRIBUTES.ALWAYS_STOP: attributes.ATTR_BOOL,
                constants.ATTRIBUTES.SHAPE: attributes.ATTR_STRING
                }
    
    def __init__(self, x, y, drill, diameter = None, rotation = attributes.Rotation(), extent = DEFAULT_EXTENT, always_stop = DEFAULT_ALWAYS_STOP, shape = DEFAULT_SHAPE):
        self.x = x
        self.y = y
        self.drill = drill
        self.diameter = diameter
        self.rotation = rotation
        self.extent = extent
        self.always_stop = always_stop
        self.shape = shape
        
    @classmethod
    def parse(cls, n):
        x = attributes.parse(cls, n, constants.ATTRIBUTES.X)
        y = attributes.parse(cls, n, constants.ATTRIBUTES.Y)
        drill = attributes.parse(cls, n, constants.ATTRIBUTES.DRILL)
        diameter = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.DIAMETER, None)
        rotation = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.ROTATION, attributes.Rotation(0))
        extent = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.EXTENT, cls.DEFAULT_EXTENT)
        always_stop = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.ALWAYS_STOP, cls.DEFAULT_ALWAYS_STOP)
        shape = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.SHAPE, cls.DEFAULT_SHAPE)
        
        return Via(x, y, drill, diameter, rotation, extent, always_stop, shape)
    
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, self.TAG_NAME)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.X, self.x)
        attributes.set_attr(self, n, constants.ATTRIBUTES.Y, self.y)
        attributes.set_attr(self, n, constants.ATTRIBUTES.DRILL, self.drill)
        attributes.set_attr(self, n, constants.ATTRIBUTES.DIAMETER, self.diameter)
        attributes.set_attr(self, n, constants.ATTRIBUTES.ROTATION, self.rotation, attributes.Rotation(0))
        attributes.set_attr(self, n, constants.ATTRIBUTES.EXTENT, self.extent, self.DEFAULT_EXTENT)
        attributes.set_attr(self, n, constants.ATTRIBUTES.ALWAYS_STOP, self.always_stop, self.DEFAULT_ALWAYS_STOP)
        attributes.set_attr(self, n, constants.ATTRIBUTES.SHAPE, self.shape, self.DEFAULT_SHAPE)

class Wire:
    TAG_NAME = constants.TAGS.WIRE
    
    DEFAULT_CURVE = 0.0
    DEFAULT_EXTENT = None
    DEFAULT_STYLE = constants.WIRE.STYLE.CONTINUOUS
    DEFAULT_CAP = constants.WIRE.CAP.ROUND
    
    ATTR_MAP = { constants.ATTRIBUTES.X1: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.Y1: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.X2: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.Y2: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.WIDTH: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.LAYER: attributes.ATTR_INT,
                constants.ATTRIBUTES.CURVE: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.EXTENT: attributes.ATTR_EXTENT,
                constants.ATTRIBUTES.STYLE: attributes.ATTR_STRING,
                constants.ATTRIBUTES.CAP: attributes.ATTR_STRING
                }
    
    def __init__(self, x1, y1, x2, y2, width, layer, curve = DEFAULT_CURVE, extent = DEFAULT_EXTENT, style = DEFAULT_STYLE, cap = DEFAULT_CAP):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.width = width
        self.layer = layer
        self.curve = curve
        self.extent = extent
        self.style = style
        self.cap = cap

    @classmethod
    def parse(cls, n):
        x1 = attributes.parse(cls, n, constants.ATTRIBUTES.X1)
        y1 = attributes.parse(cls, n, constants.ATTRIBUTES.Y1)
        x2 = attributes.parse(cls, n, constants.ATTRIBUTES.X2)
        y2 = attributes.parse(cls, n, constants.ATTRIBUTES.Y2)
        width = attributes.parse(cls, n, constants.ATTRIBUTES.WIDTH)
        layer = attributes.parse(cls, n, constants.ATTRIBUTES.LAYER)
        curve = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.CURVE, cls.DEFAULT_CURVE)
        extent = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.EXTENT, cls.DEFAULT_EXTENT)
        style = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.STYLE, cls.DEFAULT_STYLE)
        cap = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.CAP, cls.DEFAULT_CAP)

        return Wire(x1, y1, x2, y2, width, layer, curve, extent, style, cap)

    def append_node(self, _n):
        n = ElementTree.SubElement(_n, self.TAG_NAME)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.X1, self.x1)
        attributes.set_attr(self, n, constants.ATTRIBUTES.Y1, self.y1)
        attributes.set_attr(self, n, constants.ATTRIBUTES.X2, self.x2)
        attributes.set_attr(self, n, constants.ATTRIBUTES.Y2, self.y2)
        attributes.set_attr(self, n, constants.ATTRIBUTES.WIDTH, self.width)
        attributes.set_attr(self, n, constants.ATTRIBUTES.LAYER, self.layer)
        attributes.set_attr(self, n, constants.ATTRIBUTES.CURVE, self.curve, self.DEFAULT_CURVE)
        attributes.set_attr(self, n, constants.ATTRIBUTES.EXTENT, self.extent, self.DEFAULT_EXTENT)
        attributes.set_attr(self, n, constants.ATTRIBUTES.STYLE, self.style, self.DEFAULT_STYLE)
        attributes.set_attr(self, n, constants.ATTRIBUTES.CAP, self.cap, self.DEFAULT_CAP)

def parse_item(n):
    """
    Return a primitive for the given ElementTree ``Element``, or None if the element is not supported.
    
    :param n: An ElementTree Element.
    
    :returns: A pritive object, or None if the element is unsupported, or if the element has no representation (e.g. for a discription element).
    
    """
    
    if ITEM_MAP.has_key(n.tag) == False:
        print("Warning--unsupported tag {0}.".format(n.tag))
        return None

    cls = ITEM_MAP[n.tag]
    return cls.parse(n)

# A dictionary used to associate XML tag names with primitive classes.
# Populated dynamically when the module is imported.
ITEM_MAP = {}

classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)

for n, c in classes:
    ITEM_MAP[c.TAG_NAME] = c