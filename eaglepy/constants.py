"""
Constraints
===========

Contains all supported XML tag and attribute names.

Also contains many commonly-used attribute values.

"""

# The amount by which to multiply a drill values to obtain the diameter
# when the diameter is set to auto.
AUTO_DIAMETER_SCALE = 1.4

# Boolean values
TRUE = 'yes'
FALSE = 'no'

ROUTE_ANY = 'any'

class ADD_LEVEL:
    MUST = 'must'
    CAN = 'can'
    NEXT = 'next'
    REQUEST = 'request'
    ALWAYS = 'always'

# Alignments
class ALIGN:
    """
    Represents an alignment. Used by ``Text`` and ``Label`` objects.
    
    """
    
    _BOTTOM = 'bottom'
    _CENTER = 'center'
    _LEFT = 'left'
    _RIGHT = 'right'
    _TOP = 'top'
    
    TOP_LEFT = _TOP + '-' + _LEFT
    TOP_CENTER = _TOP + '-' + _CENTER
    TOP_RIGHT = _TOP + '-' + _RIGHT
    CENTER_LEFT = _CENTER + '-' + _LEFT
    CENTER = _CENTER
    CENTER_RIGHT = _CENTER + '-' + _RIGHT
    BOTTOM_LEFT = _BOTTOM + '-' + _LEFT
    BOTTOM_CENTER = _BOTTOM + '-' + _CENTER
    BOTTOM_RIGHT = _BOTTOM + '-' + _RIGHT

    @classmethod
    def get_h_and_v_align(cls, alignment):
        """
        Split an alignment string into its horizontal and vertical components.
        
        :param alignment: The alignment string to parse.
        
        :raises: An Exception if the alignment string is invalid.
        
        :returns: The alignment components in the form (vertical, horizontal).
        
        """
        
        if alignment == cls.CENTER:
            return (cls.CENTER, cls.CENTER)
        
        dash_index = alignment.find('-')
        if dash_index == -1:
            raise Exception('Invalid alignment string: expecting {0} or a string containing a "-".'.format(cls.CENTER))
        
        vh = alignment.split('-')
        
        if vh[0] != cls._TOP and vh[0] != cls._CENTER and vh[0] != cls._BOTTOM:
            raise Exception('Invalid vertical alignment specifier: expecting {0}, {1}, or {2}; got {3}.'.format(cls._TOP, cls._CENTER, cls._BOTTOM, vh[0]))
        
        if vh[1] != cls._LEFT and vh[1] != cls._CENTER and vh[1] != cls._RIGHT:
            raise Exception('Invalid horizontal alignment specifier: expecting {0}, {1}, or {2}; got {3}.'.format(cls._LEFT, cls._CENTER, cls._RIGHT, vh[1]))
        
        return (vh[0], vh[1])

class DIMENSION_TYPE:
    VERTICAL = 'vertical'
    HORIZONTAL = 'horizontal'
    LEADER = 'leader'
    PARALLEL = 'parallel'
    RADIUS = 'radius'
    DIAMETER = 'diameter'
    ANGLE = 'angle'


# Font types
class FONT:
    """
    Represents a font. Used by ``Text`` objects.
    
    """
    
    PROPORTIONAL = 'proportional'
    VECTOR = 'vector'
    FIXED = 'fixed'
   

# Grid style 
class GRID_STYLE:
    DOTS = 'dots'
    LINES = 'lines'

    
# Layer number constants.
class LAYERS:
    """
    Contains the numbers for commonly-used layers.
    """
    TOP = 1
    ROUTE2 = 2
    ROUTE3 = 3
    ROUTE14 = 14
    ROUTE15 = 15
    BOTTOM = 16
    PADS = 17
    VIAS = 18
    UNROUTED = 19
    DIMENSION = 20
    TPLACE = 21
    BPLACE = 22
    TORIGINS = 23
    BORIGINS = 24
    TNAMES = 25
    BNAMES = 26
    TVALUES = 27
    BVALUES = 28
    TSTOP = 29
    BSTOP = 30
    TCREAM = 31
    BCREAM = 32
    TFINISH = 33
    BFINISH = 34
    TGLUE = 35
    BGLUE = 36
    TTEST = 37
    BTEST = 38
    TKEEPOUT = 39
    BKEEPOUT = 40
    TRESTRICT = 41
    BRESTRICT = 42
    VRESTRICT = 43
    DRILLS = 44
    HOLES = 45
    MILLING = 46
    MEASURES = 47
    DOCUMENT = 48
    REFERENCE = 49
    TDOCU = 51
    BDOCU = 52
    NETS = 91
    BUSSES = 92
    PINS = 93
    SYMBOLS = 94
    NAMES = 95
    VALUES = 96
    INFO = 97
    GUIDE = 98

class PIN:
    """
    Represents various attributes of ``Pin`` objects.
    
    """
    
    class LENGTH:
        POINT = 'point'
        SHORT = 'short'
        MIDDLE = 'middle'
        LONG = 'long'

    class VISIBLE:
        OFF = 'off'
        BOTH = 'both'
        PAD = 'pad'
        PIN = 'pin'

    class FUNCTION:
        NONE = 'none'
        DOT = 'dot'
        CLK = 'clk'
        DOTCLK = 'dotclk'

class POUR:
    SOLID = 'solid'
    HATCH = 'hatch'

class SHAPE:
    """
    Represents the shape of a ``Pad`` object.
    """
    
    ROUND = 'round'
    SQUARE = 'square'
    OCTAGON = 'octagon'
    LONG = 'long'
    OFFSET = 'offset'

class UNIT:
    MM = 'mm'
    MICRON = 'mic'
    MIL = 'mil'
    INCH = 'inch'

    PER_MM = { INCH: 0.0393701,
                     MM: 1,
                     MIL: 39.3701,
                     MICRON: 1000
                    }

    MM_PER = { INCH: 25.4,
               MM: 1,
               MIL: 0.0254,
               MICRON: 0.001
             }

    @classmethod
    def to_default(cls, value, unit):
        return value * cls.MM_PER[unit]


class WIRE:
    class STYLE:
        CONTINUOUS = 'continuous'
        LONG_DASH = 'longdash'
        SHORT_DASH = 'shortdash'
        DASH_DOT = 'dashdot'

    class CAP:
        ROUND = 'round'
        FLAT = 'flat'
        
# Attribute name constants
class ATTRIBUTES:
    """
    Contains the name of all supported attributes.
    """
    ACTIVE = 'active'
    ADD_LEVEL = 'addlevel'
    AIRWIRES_HIDDEN = 'airwireshidden'
    ALIGN = 'align'
    ALT_DISTANCE = 'altdistance'
    ALT_UNIT = 'altunit'
    ALT_UNIT_DIST = 'altunitdist'
    ALWAYS_STOP = 'alwaysstop'

    class BORDER:
        BOTTOM = 'border-bottom'
        LEFT = 'border-left'
        RIGHT = 'border-right'
        TOP = 'border-top'
    
    CAP = 'cap'
    CLASS = 'class'
    COLOR = 'color'
    COLUMNS = 'columns'
    CONSTANT= 'constant'
    CREAM = 'cream'
    CURVE = 'curve'
    DEVICE = 'device'
    DEVICE_SET = 'deviceset'
    DIAMETER = 'diameter'
    DIMENSION_TYPE = 'dtype'
    DIRECTION = 'direction'
    DISPLAY = 'display'
    DISTANCE = 'distance'
    DRILL = 'drill'
    DX = 'dx'
    DY = 'dy'
    ELEMENT = 'element'
    EXT_LENGTH = 'extlength'
    EXT_OFFSET = 'extoffset'
    EXT_WIDTH = 'extwidth'
    EXTENT = 'extent'
    FILL = 'fill'
    FIRST = 'first'
    FONT = 'font'
    FUNCTION = 'function'
    GATE = 'gate'
    HASH = 'hash'
    ISOLATE = 'isolate'
    LANGUAGE = 'language'
    LAYER = 'layer'
    LENGTH = 'length'
    LIBRARY = 'library'
    LOCKED = 'locked'
    MIN_VERSION = 'minversion'
    MULTIPLE = 'multiple'
    NAME = 'name'
    NUMBER = 'number'
    ORPHANS = 'orphans'
    PACKAGE = 'package'
    PAD = 'pad'
    PART = 'part'
    PIN = 'pin'
    POUR = 'pour'
    PRECISION = 'precision'
    PREFIX = 'prefix'
    RADIUS = 'radius'
    RANK = 'rank'
    RATIO = 'ratio'
    REFER = 'refer'
    ROTATION = 'rot'
    ROUNDNESS = 'roundness'
    ROUTE = 'route'
    ROUTE_TAG = 'routetag'
    ROWS = 'rows'
    SEVERITY = 'severity'
    SHAPE = 'shape'
    SIGNAL_CLASS = 'class'
    SIZE = 'size'
    SMASHED = 'smashed'
    SPACING = 'spacing'
    SPIN = 'spin'
    STOP = 'stop'
    STYLE = 'style'
    SWAP_LEVEL = 'swaplevel'
    SYMBOL = 'symbol'
    TECHNOLOGY = 'technology'
    TEXT_RATIO = 'textratio'
    TEXT_SIZE = 'textsize'
    THERMALS = 'thermals'
    UNIT = 'unit'
    UNIT_DIST = 'unitdist'
    USER_VALUE = 'uservalue'
    VALUE = 'value'
    VERSION = 'version'
    VISIBLE = 'visible'
    WIDTH = 'width'
    X = 'x'
    X1 = 'x1'
    X2 = 'x2'
    X3 = 'x3'
    XREF = 'xref'
    XREF_LABEL = 'xreflabel'
    XREF_PART = 'xrefpart'
    Y = 'y'
    Y1 = 'y1'
    Y2 = 'y2'
    Y3 = 'y3'

    
# All supported XML tag names.
class TAGS:
    APPROVED =    'approved'
    ATTRIBUTE =   'attribute'
    ATTRIBUTES =  'attributes'
    AUTOROUTER =  'autorouter' 
    BOARD =       'board'
    BUS =         'bus'
    BUSSES =      'busses'
    CIRCLE =      'circle'
    CLASS =       'class'
    CLASSES =     'classes'
    CLEARANCE =   'clearance'       
    COMPATIBILITY='compatibility'
    CONNECT =     'connect'
    CONNECTS =    'connects'
    CONTACT_REF = 'contactref'
    DESCRIPTION = 'description'
    DESIGN_RULES ='designrules'
    DEVICE =      'device'
    DEVICE_SET =  'deviceset'
    DEVICE_SETS = 'devicesets'
    DEVICES =     'devices'
    DIMENSION =   'dimension'
    DRAWING =     'drawing'
    EAGLE =       'eagle'
    ELEMENT =     'element'
    ELEMENTS =    'elements'
    ERRORS =      'errors'
    FRAME =       'frame'
    GATE =        'gate'
    GATES =       'gates'
    GRID =        'grid'
    HOLE =        'hole'
    INSTANCE =    'instance'
    INSTANCES =   'instances'
    JUNCTION =    'junction'
    LABEL =       'label'
    LAYER =       'layer'
    LAYERS =      'layers'
    LIBRARIES =   'libraries'
    LIBRARY =     'library'
    NET =         'net'
    NETS =        'nets'
    NOTE =        'note'
    PACKAGE =     'package'
    PACKAGES =    'packages'
    PAD =         'pad'
    PARAM =       'param' 
    PART =        'part' 
    PARTS =       'parts'
    PASS =        'pass'
    PIN =         'pin'
    PIN_REF =     'pinref'
    PLAIN =       'plain'
    POLYGON =     'polygon'
    RECTANGLE =   'rectangle'
    SCHEMATIC =   'schematic'
    SEGMENT =     'segment'
    SETTING =     'setting'
    SETTINGS =    'settings'
    SHEET =       'sheet'
    SHEETS =      'sheets'
    SIGNAL =      'signal'
    SIGNALS =     'signals'
    SMD =         'smd'
    SYMBOL =      'symbol'
    SYMBOLS =     'symbols'
    TECHNOLOGIES ='technologies'
    TECHNOLOGY =  'technology'
    TEXT =        'text'
    VARIANT =     'variant'
    VARIANT_DEF = 'variantdef'
    VARIANT_DEFS ='variantdefs'
    VERTEX =      'vertex'
    VIA =         'via'
    WIRE =        'wire'