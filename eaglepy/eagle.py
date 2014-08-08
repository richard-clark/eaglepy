"""

EAGLE-Python
============

A Python package for creating, modifying, and writing Cadsoft EAGLE files

"""

import attributes
import constants
import etree_utils
import key_list
import primitives
import StringIO

# Attempt to use ``lxml``.
# Otherwise, use ``xml``.
try:
    from lxml import etree as ElementTree
except:
    from xml.etree import ElementTree

class Eagle:
    TAG_NAME = constants.TAGS.EAGLE
    
    """
    Represents an EAGLE file, the top element in the hierarchy.
    """
    
    DEFAULT_VERSION = '6.5.0'
    
    def __init__(self, 
                 drawing, 
                 xml_version = '1.0', 
                 encoding = 'utf-8', 
                 version='6.5.0',
                 compatibility = []):
        self.drawing = drawing
        self.xml_version = xml_version
        self.encoding = encoding
        self.version = version
        self.compatibility = compatibility
    
    @staticmethod
    def load(file_name):
        """
        Attempt to read an ``Eagle`` object from an XML file.
        
        :param file_name: The name of the file. 
        :throws: ``Exception`` if an error occurs while attempting to read the file.
        :returns: An ``Eagle`` object.
        
        """
        
        # Parse the specified input file
        dom = ElementTree.parse(file_name)
        
        if hasattr(dom, 'docinfo'):
            xml_version = dom.docinfo.xml_version
            encoding = dom.docinfo.encoding
        else: # etree, not lxml
            xml_version = '1.0'
            encoding = 'utf-8'
        
        # Get the Eagle node
        n_eagle = dom.getroot()
        
        if n_eagle.tag != constants.TAGS.EAGLE:
            raise Exception('Invalid tag name for root node--expecting {0}; got {1}.'.format(constants.TAGS.EAGLE, n_eagle.tag))
        
        # Get the version of the Eagle node.
        if n_eagle.attrib.has_key(constants.ATTRIBUTES.VERSION):
            version = n_eagle.attrib[constants.ATTRIBUTES.VERSION]
        else:
            version = Eagle.DEFAULT_VERSION
        
        # Get the drawing element
        # There should only be one drawing per document.
        n_drawing_arr = n_eagle.findall(constants.TAGS.DRAWING)
        
        if len(n_drawing_arr) == 0:
            raise Exception('Document did not contain a {0} node.'.format(constants.TAGS.DRAWING))
        elif len(n_drawing_arr) > 1:
            raise Exception('Document contained multiple ({0}) {1} nodes; only 1 is supported.'.format(len(n_drawing_arr), constants.TAGS.DRAWING))
        
        n_drawing = n_drawing_arr[0]
        
        # Parse the drawing
        drawing = Drawing.parse(n_drawing)

        # Parse the compatibility
        compatibility = etree_utils.parse_grandchildren_of_class(n_eagle, Note)
        
        return Eagle(drawing, xml_version, encoding, version, compatibility)

    def save(self, file_name):
        """
        Attempt to write the object to an XML file. 
        
        :param file_name: The name of the file to write. 
        :raises: An ``Exception`` if an error occurs while attempting to write the file.
        :returns: ``None``.
        
        """

        # Create the tree by parsing a basic XML template. 
        # (This is the only way to set the document type and XML version.)
        io = StringIO.StringIO('<?xml version="' + self.xml_version + '" ?><!DOCTYPE eagle SYSTEM "eagle.dtd"><' + constants.TAGS.EAGLE + ' />')
        tree = ElementTree.parse(io)
        
        # Set the version
        n = tree.getroot() # returns the <eagle /> element
        n.attrib[constants.ATTRIBUTES.VERSION] = self.version
        
        # Add the drawing (the only childe lement)
        self.drawing.append_node(n)
        
        # Add the compatibility
        if len(self.compatibility) > 0:
            n_compatibility = ElementTree.SubElement(n, constants.TAGS.COMPATIBILITY)
            
            for nn in self.compatibility:
                nn.append_node(n_compatibility)
        
        # Save    
        xml_str = ElementTree.tostring(tree, xml_declaration=True, encoding=self.encoding, pretty_print=True)
        
        f = open(file_name, 'w')
        f.write(xml_str);
        f.close()
    

class Approved_Error:
    TAG_NAME = constants.TAGS.APPROVED
    PARENT_TAG_NAME = constants.TAGS.ERRORS
    
    ATTR_MAP = { constants.ATTRIBUTES.HASH: attributes.ATTR_STRING}
    
    def __init__(self, _hash):
        self._hash = _hash
        
    @classmethod
    def parse(cls, n):
        _hash = attributes.parse(cls, n, constants.ATTRIBUTES.HASH)
        return Approved_Error(_hash)
    
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, constants.TAGS.APPROVED)
        attributes.set_attr(self, n, constants.ATTRIBUTES.HASH, self._hash)

class Attribute:
    TAG_NAME = constants.TAGS.ATTRIBUTE
    PARENT_TAG_NAME = constants.TAGS.ATTRIBUTES
    
    ATTR_MAP = { constants.ATTRIBUTES.NAME: attributes.ATTR_STRING,
                constants.ATTRIBUTES.VALUE: attributes.ATTR_STRING,
                constants.ATTRIBUTES.X: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.Y: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.SIZE: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.LAYER: attributes.ATTR_INT,
                constants.ATTRIBUTES.FONT: attributes.ATTR_STRING,
                constants.ATTRIBUTES.ROTATION: attributes.ATTR_ROT,
                constants.ATTRIBUTES.ALIGN: attributes.ATTR_STRING,
                constants.ATTRIBUTES.DISPLAY: attributes.ATTR_ON_OFF,
                constants.ATTRIBUTES.RATIO: attributes.ATTR_INT
                }
    
    DEFAULT_ALIGN = constants.ALIGN.TOP_LEFT
    DEFAULT_DISPLAY = True
    DEFAULT_FONT = constants.FONT.PROPORTIONAL
    DEFAULT_RATIO = 8
    
    def __init__(self, name, value, x, y, size, layer, font, rotation, align, display, ratio =DEFAULT_RATIO):
        self.name = name
        self.value = value
        self.x = x
        self.y = y
        self.size = size
        self.layer = layer
        self.font = font
        self.rotation = rotation
        self.align = align
        self.display = display
        self.ratio = ratio
        
    @classmethod
    def parse(cls, n):
        name = attributes.parse(cls, n, constants.ATTRIBUTES.NAME)
        value = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.VALUE, None)
        x = attributes.parse(cls, n, constants.ATTRIBUTES.X)
        y = attributes.parse(cls, n, constants.ATTRIBUTES.Y)
        size = attributes.parse(cls, n, constants.ATTRIBUTES.SIZE)
        layer = attributes.parse(cls, n, constants.ATTRIBUTES.LAYER)
        font = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.FONT, cls.DEFAULT_FONT)
        rotation = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.ROTATION, attributes.Rotation(0))
        align = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.ALIGN, cls.DEFAULT_ALIGN)
        display = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.DISPLAY, cls.DEFAULT_DISPLAY)
        ratio = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.RATIO, cls.DEFAULT_RATIO)
        
        return Attribute(name, value, x, y, size, layer, font, rotation, align, display, ratio)
        
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, self.TAG_NAME)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.NAME, self.name)
        attributes.set_attr(self, n, constants.ATTRIBUTES.VALUE, self.value)
        attributes.set_attr(self, n, constants.ATTRIBUTES.X, self.x)
        attributes.set_attr(self, n, constants.ATTRIBUTES.Y, self.y)
        attributes.set_attr(self, n, constants.ATTRIBUTES.SIZE, self.size)
        attributes.set_attr(self, n, constants.ATTRIBUTES.LAYER, self.layer)
        attributes.set_attr(self, n, constants.ATTRIBUTES.FONT, self.font, self.DEFAULT_FONT)
        attributes.set_attr(self, n, constants.ATTRIBUTES.ROTATION, self.rotation, attributes.Rotation(0))
        attributes.set_attr(self, n, constants.ATTRIBUTES.ALIGN, self.align, self.DEFAULT_ALIGN)
        attributes.set_attr(self, n, constants.ATTRIBUTES.DISPLAY, self.display, self.DEFAULT_DISPLAY)
        attributes.set_attr(self, n, constants.ATTRIBUTES.RATIO, self.ratio, self.DEFAULT_RATIO)


class Autorouter:
    TAG_NAME = constants.TAGS.AUTOROUTER
    
    def __init__(self, passes):
        self.passes = passes
        
    @classmethod
    def parse(cls, n):
        passes = etree_utils.parse_children_of_class(n, Pass)    
        return Autorouter(passes)
    
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, constants.TAGS.AUTOROUTER)
        
        # Add the passes
        for p in self.passes:
            p.append_node(n)
        
class Board:
    TAG_NAME = constants.TAGS.BOARD
    
    def __init__(self, 
                 libraries = None, 
                 elements = None,
                  signals = None, 
                  plain_items = None, 
                  classes = None, 
                  design_rules = None, 
                  autorouter = None, 
                  errors = None, 
                  attributes = None, 
                  variant_defs = None):
        
        self.libraries = libraries if libraries else key_list.Key_List()
        self.elements = elements if elements else key_list.Key_List()
        self.signals = signals if signals else key_list.Key_List()
        self.plain_items = plain_items if plain_items else []
        self.classes = classes if classes else []
        self.design_rules = design_rules
        self.autorouter = autorouter
        self.errors = errors if errors else []
        self.attributes = attributes if attributes else []
        self.variant_defs = variant_defs if variant_defs else []
                
    @classmethod
    def parse(cls, n):
        libraries = etree_utils.parse_grandchildren_of_class_into_od(n, Library)
        signals = etree_utils.parse_grandchildren_of_class_into_od(n, Signal)
        plain_items = etree_utils.parse_grandchildren_using_function(n, constants.TAGS.PLAIN, primitives.parse_item)
        attribs = etree_utils.parse_grandchildren_of_class(n, Global_Attribute)
        classes = etree_utils.parse_grandchildren_of_class(n, Net_Class)
        design_rules = etree_utils.parse_child_of_class(n, Design_Rules)
        autorouter = etree_utils.parse_child_of_class(n, Autorouter)
        errors = etree_utils.parse_grandchildren_of_class(n, Approved_Error)    
        variant_defs = etree_utils.parse_grandchildren_of_class(n, Variant_Def)
        
        board = Board(libraries = libraries, 
                      signals = signals, 
                      plain_items = plain_items, 
                      classes = classes, 
                      design_rules = design_rules, 
                      autorouter = autorouter, 
                      errors = errors, 
                      attributes = attribs, 
                      variant_defs = variant_defs)

        board.elements = etree_utils.parse_grandchildren_of_class_into_od_with_obj(n, Element, board)

        return board

    def append_node(self, _n):
        # Add this node
        n = ElementTree.SubElement(_n, constants.TAGS.BOARD)
        
        # Add the plain items
        etree_utils.append_grandchildren_with_tag(n, constants.TAGS.PLAIN, self.plain_items)
        etree_utils.append_grandchildren_of_class_from_od(n, Library, self.libraries)
        etree_utils.append_grandchildren_of_class(n, Global_Attribute, self.attributes)
        etree_utils.append_grandchildren_of_class(n, Variant_Def, self.variant_defs)
        etree_utils.append_grandchildren_of_class(n, Net_Class, self.classes)

        if self.design_rules != None:
            self.design_rules.append_node(n)
        
        if self.autorouter != None:
            self.autorouter.append_node(n)
            
        etree_utils.append_grandchildren_of_class_from_od(n, Element, self.elements)
        etree_utils.append_grandchildren_of_class_from_od(n, Signal, self.signals)
        etree_utils.append_grandchildren_of_class(n, Approved_Error, self.errors, False)     
#         
#     def get_package_dict(self):
#         """
#         Returns a dictionary which can be used to associate a library name and package name
#         with a ``Package`` object. 
#         
#         The returned set takes the form:
#             
#             package_dict = {
#                 library_name_1: {
#                     package_name_1: package_1,
#                     package_name_2: package_2,
#                     ...
#                 },
#                 library_name_2: {
#                     package_name_1: package_1,
#                     ...
#                 },
#                 ...
#             }
#         
#         """
#         
#         package_dict = {}
#         
#         for l in self.libraries:
#             packages = {}
#             
#             for p in l.packages:
#                 packages[p.name] = p
#             
#             package_dict[l.name] = packages
#             
#         return package_dict
        



class Bus:
    TAG_NAME = constants.TAGS.BUS
    PARENT_TAG_NAME = constants.TAGS.BUSSES
    
    ATTR_MAP = {constants.ATTRIBUTES.NAME: attributes.ATTR_STRING}
    
    def __init__(self, name, segments = None):
        self.name = name
        self.segments = segments if segments else []
        
    @classmethod
    def parse(cls, n):
        name = attributes.parse(cls, n, constants.ATTRIBUTES.NAME)

        segments = etree_utils.parse_children_using_function(n, Segment.parse, constants.TAGS.SEGMENT)

        return Bus(name, segments)
        
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, constants.TAGS.BUS)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.NAME, self.name)
        
        # Add the segments
        for s in self.segments:
            s.append_node(n)

class Clearance:
    TAG_NAME = constants.TAGS.CLEARANCE
    
    ATTR_MAP = {constants.ATTRIBUTES.CLASS: attributes.ATTR_INT,
                constants.ATTRIBUTES.VALUE: attributes.ATTR_FLOAT}
    
    def __init__(self, eagle_class, value):
        self.eagle_class = eagle_class
        self.value = value
    
    @classmethod
    def parse(cls, n):
        eagle_class = attributes.parse(cls, n, constants.ATTRIBUTES.CLASS)
        value = attributes.parse(cls, n, constants.ATTRIBUTES.VALUE)
        
        return Clearance(eagle_class, value)
   
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, constants.TAGS.CLEARANCE)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.CLASS, self.eagle_class)
        attributes.set_attr(self, n, constants.ATTRIBUTES.VALUE, self.value)
   

class Connect:
    TAG_NAME = constants.TAGS.CONNECT
    PARENT_TAG_NAME = constants.TAGS.CONNECTS
    
    DEFAULT_ROUTE = None
    
    ATTR_MAP = {constants.ATTRIBUTES.NAME: attributes.ATTR_STRING,
                constants.ATTRIBUTES.PIN: attributes.ATTR_STRING,
                constants.ATTRIBUTES.PAD: attributes.ATTR_STRING,
                constants.ATTRIBUTES.ROUTE: attributes.ATTR_STRING}
    
    def __init__(self, gate, pin, pad, route = DEFAULT_ROUTE):
        self.gate = gate
        self.pin = pin
        self.pad = pad
        self.route = route
        
    @classmethod
    def parse(cls, n):
        gate = attributes.parse(cls, n, constants.ATTRIBUTES.GATE)
        pin = attributes.parse(cls, n, constants.ATTRIBUTES.PIN)
        pad = attributes.parse(cls, n, constants.ATTRIBUTES.PAD)
        route = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.ROUTE, cls.DEFAULT_ROUTE)
        
        return Connect(gate, pin, pad, route)
        
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, constants.TAGS.CONNECT)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.GATE, self.gate)
        attributes.set_attr(self, n, constants.ATTRIBUTES.PIN, self.pin)
        attributes.set_attr(self, n, constants.ATTRIBUTES.PAD, self.pad)
        attributes.set_attr(self, n, constants.ATTRIBUTES.ROUTE, self.route)
        
class Description:
    TAG_NAME = constants.TAGS.DESCRIPTION
    
    ATTR_MAP = {constants.ATTRIBUTES.LANGUAGE: attributes.ATTR_STRING}
        
    DEFAULT_LANGUAGE = None
        
    def __init__(self, description, language = DEFAULT_LANGUAGE):
        self.description = description
        self.langauge = language
        
    @classmethod
    def parse(cls, n):
        language = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.LANGUAGE, cls.DEFAULT_LANGUAGE)
        
        description = n.text

        return Description(description, language)

    def append_node(self, _n):
        n = ElementTree.SubElement(_n, constants.TAGS.DESCRIPTION)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.LANGUAGE, self.langauge, self.DEFAULT_LANGUAGE)
    
        n.text = self.description

class Design_Rules:
    TAG_NAME = constants.TAGS.DESIGN_RULES
    
    ATTR_MAP = {constants.ATTRIBUTES.NAME: attributes.ATTR_STRING
                }
    
    def __init__(self, name, params = None, descriptions = None):
        self.name = name
        self.params = params if params else []
        self.descriptions = descriptions if descriptions else []
        
    @classmethod
    def parse(cls, n):
        name = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.NAME, None)
        
        descriptions = etree_utils.parse_children_of_class(n, Description)
        params = etree_utils.parse_children_of_class(n, Param)
        
        return Design_Rules(name, params, descriptions)
        
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, constants.TAGS.DESIGN_RULES)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.NAME, self.name)
        
        # Add the descriptions
        for d in self.descriptions:
            d.append_node(n)

        # Add the parameters
        for p in self.params:
            p.append_node(n)

class Device:
    TAG_NAME = constants.TAGS.DEVICE
    PARENT_TAG_NAME = constants.TAGS.DEVICES

    ATTR_MAP = {constants.ATTRIBUTES.NAME: attributes.ATTR_STRING,
                constants.ATTRIBUTES.PACKAGE: attributes.ATTR_STRING}
    
    def __init__(self, 
                 name, 
                 package, 
                 connects = None, 
                 technologies = None):
        self.name = name
        self.package = package
        self.connects = connects if connects else []
        self.technologies = technologies if technologies else []
        
    @classmethod
    def parse(cls, n, lib):
        name = attributes.parse(cls, n, constants.ATTRIBUTES.NAME)
        
        package_name = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.PACKAGE, None)
        if package_name != None:
            package = lib.packages[package_name]
        else:
            package = None
        
        technologies = etree_utils.parse_grandchildren_of_class(n, Technology)
        connects = etree_utils.parse_grandchildren_of_class(n, Connect)
        return Device(name, package, connects, technologies)
        
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, constants.TAGS.DEVICE)
        attributes.set_attr(self, n, constants.ATTRIBUTES.NAME, self.name if self.name != None else "")
        attributes.set_attr(self, n, constants.ATTRIBUTES.PACKAGE, None if self.package == None else self.package.name)
        etree_utils.append_grandchildren_of_class(n, Connect, self.connects, False)
        etree_utils.append_grandchildren_of_class(n, Technology, self.technologies)
        


class Device_Attribute:
    TAG_NAME = constants.TAGS.ATTRIBUTE
    
    DEFAULT_CONSTANT = True
    
    ATTR_MAP = { constants.ATTRIBUTES.NAME: attributes.ATTR_STRING,
                constants.ATTRIBUTES.VALUE: attributes.ATTR_STRING,
                constants.ATTRIBUTES.CONSTANT: attributes.ATTR_BOOL}
    
    def __init__(self, name, value, constant = DEFAULT_CONSTANT):
        self.name = name
        self.value = value
        self.constant = constant
        
    @classmethod
    def parse(cls, n):
        name = attributes.parse(cls, n, constants.ATTRIBUTES.NAME)
        value = attributes.parse(cls, n, constants.ATTRIBUTES.VALUE)
        constant = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.CONSTANT, cls.DEFAULT_CONSTANT)
        
        return Device_Attribute(name, value, constant)
        
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, constants.TAGS.ATTRIBUTE)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.NAME, self.name)
        attributes.set_attr(self, n, constants.ATTRIBUTES.VALUE, self.value)
        attributes.set_attr(self, n, constants.ATTRIBUTES.CONSTANT, self.constant, self.DEFAULT_CONSTANT)
        
class Device_Set:
    TAG_NAME = constants.TAGS.DEVICE_SET
    PARENT_TAG_NAME = constants.TAGS.DEVICE_SETS
    
    ATTR_MAP = { constants.ATTRIBUTES.NAME: attributes.ATTR_STRING,
                constants.ATTRIBUTES.PREFIX: attributes.ATTR_STRING,
                constants.ATTRIBUTES.USER_VALUE: attributes.ATTR_BOOL
                }
    
    DEFAULT_PREFIX = None
    DEFAULT_USER_VALUE = False
    
    def __init__(self, 
                 name, 
                 prefix = DEFAULT_PREFIX, 
                 user_value = DEFAULT_USER_VALUE, 
                 gates = None, 
                 devices = None, 
                 description = None):
        self.name = name
        self.prefix = prefix
        self.user_value = user_value
        self.gates = gates if gates else key_list.Key_List()
        self.devices = devices if devices else key_list.Key_List()
        self.description = description
        
    @classmethod
    def parse(cls, n, lib):
        
        name = attributes.parse(cls, n, constants.ATTRIBUTES.NAME)
        prefix = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.PREFIX, cls.DEFAULT_PREFIX)
        user_value = attributes.parse_or_default(cls, n , constants.ATTRIBUTES.USER_VALUE, cls.DEFAULT_USER_VALUE)
        description = etree_utils.parse_text(n, constants.TAGS.DESCRIPTION, None)        
        
        gates = etree_utils.parse_grandchildren_of_class_into_od_with_obj(n, Gate, lib)
        devices = etree_utils.parse_grandchildren_of_class_into_od_with_obj(n, Device, lib)

        return Device_Set(name, 
                          gates = gates, 
                          devices = devices, 
                          description = description, 
                          prefix = prefix, 
                          user_value = user_value)
        
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, constants.TAGS.DEVICE_SET)
        attributes.set_attr(self, n, constants.ATTRIBUTES.NAME, self.name)
        
        # Add the description
        etree_utils.append_text_node_if_not_none(n, self.description, constants.TAGS.DESCRIPTION)
        
        # Add the attributes
        attributes.set_attr(self, n, constants.ATTRIBUTES.PREFIX, self.prefix)
        attributes.set_attr(self, n, constants.ATTRIBUTES.USER_VALUE, self.user_value, self.DEFAULT_USER_VALUE)
            
        # Add gates
        n_gates = ElementTree.SubElement(n, constants.TAGS.GATES)
        
        for g in self.gates:
            g.append_node(n_gates)
            
        # Add the devices
        n_devices = ElementTree.SubElement(n, constants.TAGS.DEVICES)
        
        for d in self.devices:
            d.append_node(n_devices)
              

class Drawing:
    TAG_NAME = constants.TAGS.DRAWING
    
    def __init__(self, grid, document, layers = None, settings = None):
        self.grid = grid
        self.document = document
        self.layers = layers if layers else []
        self.settings = settings if settings else []
        
    @staticmethod
    def parse(n_drawing):
        settings = etree_utils.parse_grandchildren_of_class(n_drawing, Setting, False)
        layers = etree_utils.parse_grandchildren_of_class(n_drawing, Layer)
        grid = etree_utils.parse_child_of_class(n_drawing, Grid)
        
        # An Eagle file is either
        # 1. A schematic
        # 2. A board
        # 3. A library
        
        # Determine which type of file this is
        board = n_drawing.find(constants.TAGS.BOARD)
        schematic = n_drawing.find(constants.TAGS.SCHEMATIC)
        library = n_drawing.find(constants.TAGS.LIBRARY)
        
        if board != None:
            document = Board.parse(board)
        elif schematic != None:
            document = Schematic.parse(schematic)
        elif library != None:
            document = Library.parse(library)
        else:
            raise Exception('File did not contain a board, schematic, or library.')
    
        return Drawing(settings = settings, 
                       grid = grid, 
                       layers = layers, 
                       document = document)
        
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, constants.TAGS.DRAWING)
        
        etree_utils.append_grandchildren_of_class(n, Setting, self.settings)
            
        # Add the grid
        if self.grid != None:
            self.grid.append_node(n)
            
        # Add the layers
        etree_utils.append_grandchildren_of_class(n, Layer, self.layers)
              
        if self.document != None:
            self.document.append_node(n)

class Element:
    TAG_NAME = constants.TAGS.ELEMENT
    PARENT_TAG_NAME = constants.TAGS.ELEMENTS
    
    DEFAULT_SMASHED = False
    DEFAULT_LOCKED = False
    
    ATTR_MAP = { constants.ATTRIBUTES.NAME: attributes.ATTR_STRING,
                constants.ATTRIBUTES.LIBRARY: attributes.ATTR_STRING,
                constants.ATTRIBUTES.PACKAGE: attributes.ATTR_STRING,
                constants.ATTRIBUTES.VALUE: attributes.ATTR_STRING,
                constants.ATTRIBUTES.X: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.Y: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.SMASHED: attributes.ATTR_BOOL,
                constants.ATTRIBUTES.ROTATION: attributes.ATTR_ROT,
                constants.ATTRIBUTES.LOCKED: attributes.ATTR_BOOL
                }
    
    def __init__(self, name, 
                 library, 
                 package, 
                 value, 
                 x, 
                 y, 
                 smashed = DEFAULT_SMASHED, 
                 rotation = attributes.Rotation(),
                 attributes = None,
                 locked = DEFAULT_LOCKED):
        self.name = name
        self.library = library
        self.package = package
        self.value = value
        self.x = x
        self.y = y
        self.smashed = smashed
        self.rotation = rotation
        self.attributes = attributes if attributes else []
        self.locked = locked
        
    @classmethod
    def parse(cls, n, board):
        name = attributes.parse(cls, n, constants.ATTRIBUTES.NAME)
        
        library_name = attributes.parse(cls, n, constants.ATTRIBUTES.LIBRARY)
        library = board.libraries[library_name]
        
        package_name = attributes.parse(cls, n, constants.ATTRIBUTES.PACKAGE)
        package = library.packages[package_name]
        
        value = attributes.parse(cls, n, constants.ATTRIBUTES.VALUE)
        x = attributes.parse(cls, n, constants.ATTRIBUTES.X)
        y = attributes.parse(cls, n, constants.ATTRIBUTES.Y)        
        smashed = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.SMASHED, cls.DEFAULT_SMASHED)
        rotation = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.ROTATION, attributes.Rotation())
        locked = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.LOCKED, cls.DEFAULT_LOCKED)
        _attributes = etree_utils.parse_children_of_class(n, Attribute)

        return Element(name, library, package, value, x, y, smashed, rotation, _attributes, locked)

    def append_node(self, _n):
        n = ElementTree.SubElement(_n, constants.TAGS.ELEMENT)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.NAME, self.name)
        attributes.set_attr(self, n, constants.ATTRIBUTES.LIBRARY, self.library.name)
        attributes.set_attr(self, n, constants.ATTRIBUTES.PACKAGE, self.package.name)
        attributes.set_attr(self, n, constants.ATTRIBUTES.VALUE, self.value)
        attributes.set_attr(self, n, constants.ATTRIBUTES.X, self.x)
        attributes.set_attr(self, n, constants.ATTRIBUTES.Y, self.y)
        attributes.set_attr(self, n, constants.ATTRIBUTES.SMASHED, self.smashed, self.DEFAULT_SMASHED)
        attributes.set_attr(self, n, constants.ATTRIBUTES.ROTATION, self.rotation, attributes.Rotation())
        attributes.set_attr(self, n, constants.ATTRIBUTES.LOCKED, self.locked, self.DEFAULT_LOCKED)
        
        # Add the element attributes
        for a in self.attributes:
            a.append_node(n)
        

class Gate:
    TAG_NAME = constants.TAGS.GATE
    PARENT_TAG_NAME = constants.TAGS.GATES
    
    DEFAULT_ADD_LEVEL = constants.ADD_LEVEL.NEXT
    DEFAULT_SWAP_LEVEL = 0
    
    ATTR_MAP = {constants.ATTRIBUTES.NAME: attributes.ATTR_STRING,
                constants.ATTRIBUTES.SYMBOL: attributes.ATTR_STRING,
                constants.ATTRIBUTES.X: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.Y: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.ADD_LEVEL: attributes.ATTR_STRING,
                constants.ATTRIBUTES.SWAP_LEVEL: attributes.ATTR_INT}
    
    def __init__(self, name, symbol, x, y, add_level = DEFAULT_ADD_LEVEL, swap_level = DEFAULT_SWAP_LEVEL):
        self.name = name
        self.symbol = symbol
        self.x = x
        self.y = y
        self.add_level = add_level
        self.swap_level = swap_level
        
    @classmethod
    def parse(cls, n, lib):
        name = attributes.parse(cls, n, constants.ATTRIBUTES.NAME)
        symbol_name = attributes.parse(cls, n, constants.ATTRIBUTES.SYMBOL)
        symbol = lib.symbols[symbol_name]
        x = attributes.parse(cls, n, constants.ATTRIBUTES.X)
        y = attributes.parse(cls, n, constants.ATTRIBUTES.Y)
        add_level = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.ADD_LEVEL, cls.DEFAULT_ADD_LEVEL)
        swap_level = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.SWAP_LEVEL, cls.DEFAULT_SWAP_LEVEL)
        
        return Gate(name, symbol, x, y, add_level, swap_level)
        
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, constants.TAGS.GATE)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.NAME, self.name)
        attributes.set_attr(self, n, constants.ATTRIBUTES.SYMBOL, self.symbol.name)
        attributes.set_attr(self, n, constants.ATTRIBUTES.X, self.x)
        attributes.set_attr(self, n, constants.ATTRIBUTES.Y, self.y)
        attributes.set_attr(self, n, constants.ATTRIBUTES.ADD_LEVEL, self.add_level, self.DEFAULT_ADD_LEVEL)
        attributes.set_attr(self, n, constants.ATTRIBUTES.SWAP_LEVEL, self.swap_level, self.DEFAULT_SWAP_LEVEL)
        
        



class Global_Attribute:
    TAG_NAME = constants.TAGS.ATTRIBUTE
    PARENT_TAG_NAME = constants.TAGS.ATTRIBUTES
    
    ATTR_MAP = {constants.ATTRIBUTES.NAME: attributes.ATTR_STRING,
                constants.ATTRIBUTES.VALUE: attributes.ATTR_STRING}
    
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    @classmethod
    def parse(cls, n):
        name = attributes.parse(cls, n, constants.ATTRIBUTES.NAME)
        value = attributes.parse(cls, n, constants.ATTRIBUTES.VALUE)
        return Global_Attribute(name, value)
    
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, self.TAG_NAME)
        attributes.set_attr(self, n, constants.ATTRIBUTES.NAME, self.name)
        attributes.set_attr(self, n, constants.ATTRIBUTES.VALUE, self.value)

class Grid:
    TAG_NAME = constants.TAGS.GRID
    
    ATTR_MAP = {    constants.ATTRIBUTES.DISTANCE: attributes.ATTR_FLOAT,
                    constants.ATTRIBUTES.UNIT_DIST: attributes.ATTR_STRING,
                    constants.ATTRIBUTES.UNIT: attributes.ATTR_STRING,
                    constants.ATTRIBUTES.STYLE: attributes.ATTR_STRING,
                    constants.ATTRIBUTES.MULTIPLE: attributes.ATTR_INT,
                    constants.ATTRIBUTES.DISPLAY: attributes.ATTR_BOOL,
                    constants.ATTRIBUTES.ALT_DISTANCE: attributes.ATTR_FLOAT,
                    constants.ATTRIBUTES.ALT_UNIT_DIST: attributes.ATTR_STRING,
                    constants.ATTRIBUTES.ALT_UNIT: attributes.ATTR_STRING
                  }
    
    def __init__(self, 
                 distance = 0.1, 
                 unit_dist = constants.UNIT.INCH, 
                 unit = constants.UNIT.INCH, 
                 style = constants.GRID_STYLE.LINES, 
                 multiple = 1, 
                 display = False, 
                 alt_distance = 0.01, 
                 alt_unit_dist = constants.UNIT.INCH, 
                 alt_unit = constants.UNIT.INCH):   
             
        self.distance = distance
        self.unit_dist = unit_dist
        self.unit = unit
        self.style = style
        self.multiple = multiple
        self.display = display
        self.alt_distance = alt_distance
        self.alt_unit_dist = alt_unit_dist
        self.alt_unit = alt_unit
        
    @classmethod
    def parse(cls, n):
        distance = attributes.parse(cls, n, constants.ATTRIBUTES.DISTANCE)
        unit_dist = attributes.parse(cls, n, constants.ATTRIBUTES.UNIT_DIST)
        unit = attributes.parse(cls, n, constants.ATTRIBUTES.UNIT)
        style = attributes.parse(cls, n, constants.ATTRIBUTES.STYLE)
        multiple = attributes.parse(cls, n, constants.ATTRIBUTES.MULTIPLE)
        display = attributes.parse(cls, n, constants.ATTRIBUTES.DISPLAY)
        altdistance = attributes.parse(cls, n, constants.ATTRIBUTES.ALT_DISTANCE)
        altunitdist = attributes.parse(cls, n, constants.ATTRIBUTES.ALT_UNIT_DIST)
        altunit = attributes.parse(cls, n, constants.ATTRIBUTES.ALT_UNIT)
        
        return Grid(distance, unit_dist, unit, style, multiple, display, altdistance, altunitdist, altunit)
        
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, constants.TAGS.GRID)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.DISTANCE, self.distance)
        attributes.set_attr(self, n, constants.ATTRIBUTES.UNIT_DIST, self.unit_dist)
        attributes.set_attr(self, n, constants.ATTRIBUTES.UNIT, self.unit)
        attributes.set_attr(self, n, constants.ATTRIBUTES.STYLE, self.style)
        attributes.set_attr(self, n, constants.ATTRIBUTES.MULTIPLE, self.multiple)
        attributes.set_attr(self, n, constants.ATTRIBUTES.DISPLAY, self.display)
        attributes.set_attr(self, n, constants.ATTRIBUTES.ALT_DISTANCE, self.alt_distance)
        attributes.set_attr(self, n, constants.ATTRIBUTES.ALT_UNIT_DIST, self.alt_unit_dist)
        attributes.set_attr(self, n, constants.ATTRIBUTES.ALT_UNIT, self.alt_unit)
        





class Instance:
    TAG_NAME = constants.TAGS.INSTANCE
    PARENT_TAG_NAME = constants.TAGS.INSTANCES
    
    ATTR_MAP = {constants.ATTRIBUTES.PART: attributes.ATTR_STRING,
                constants.ATTRIBUTES.GATE: attributes.ATTR_STRING,
                constants.ATTRIBUTES.X: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.Y: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.ROTATION: attributes.ATTR_ROT,
                constants.ATTRIBUTES.SMASHED: attributes.ATTR_BOOL}
    
    def __init__(self, part, gate, x, y, rotation = attributes.Rotation(0), attributes = None, smashed = False):
        self.part = part
        self.gate = gate
        self.x = x
        self.y = y
        self.rotation = rotation
        self.attributes = attributes if attributes else []
        self.smashed = smashed

    @classmethod
    def parse(cls, n, schematic):
        
        part_name = attributes.parse(cls, n, constants.ATTRIBUTES.PART)
        part = schematic.parts[part_name]
        
        gate_name = attributes.parse(cls, n, constants.ATTRIBUTES.GATE)
        gate = part.device_set.gates[gate_name]
        
        x = attributes.parse(cls, n, constants.ATTRIBUTES.X)
        y = attributes.parse(cls, n, constants.ATTRIBUTES.Y)
        rotation = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.ROTATION, attributes.Rotation(0))
        smashed = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.SMASHED, False)
        
        _attributes = etree_utils.parse_children_of_class(n, Attribute)
        
        return Instance(part, gate, x, y, rotation, _attributes, smashed)
        
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, constants.TAGS.INSTANCE)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.PART, self.part.name)
        attributes.set_attr(self, n, constants.ATTRIBUTES.GATE, self.gate.name)
        attributes.set_attr(self, n, constants.ATTRIBUTES.X, self.x)
        attributes.set_attr(self, n, constants.ATTRIBUTES.Y, self.y)
        attributes.set_attr(self, n, constants.ATTRIBUTES.ROTATION, self.rotation, attributes.Rotation(0))
        attributes.set_attr(self, n, constants.ATTRIBUTES.SMASHED, self.smashed, False)
        
        # Add the attributes
        for a in self.attributes:
            a.append_node(n)

class Layer:
    TAG_NAME = constants.TAGS.LAYER
    PARENT_TAG_NAME = constants.TAGS.LAYERS
    
    ATTR_MAP = { constants.ATTRIBUTES.NUMBER: attributes.ATTR_INT,
                constants.ATTRIBUTES.NAME: attributes.ATTR_STRING,
                constants.ATTRIBUTES.COLOR: attributes.ATTR_INT,
                constants.ATTRIBUTES.FILL: attributes.ATTR_INT,
                constants.ATTRIBUTES.VISIBLE: attributes.ATTR_BOOL,
                constants.ATTRIBUTES.ACTIVE: attributes.ATTR_BOOL
                }
    
    def __init__(self, number, name, color, fill, visible, active):
        self.number = number
        self.name = name
        self.color = color
        self.fill = fill
        self.visible = visible
        self.active = active 
            
    @classmethod
    def parse(cls, n):
        number = attributes.parse(cls, n, constants.ATTRIBUTES.NUMBER)
        name = attributes.parse(cls, n, constants.ATTRIBUTES.NAME)
        color = attributes.parse(cls, n, constants.ATTRIBUTES.COLOR)
        fill = attributes.parse(cls, n, constants.ATTRIBUTES.FILL)
        visible = attributes.parse(cls, n, constants.ATTRIBUTES.VISIBLE)
        active = attributes.parse(cls, n, constants.ATTRIBUTES.ACTIVE)
        
        return Layer(number, name, color, fill, visible, active)
    
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, constants.TAGS.LAYER)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.NUMBER, self.number)
        attributes.set_attr(self, n, constants.ATTRIBUTES.NAME, self.name)
        attributes.set_attr(self, n, constants.ATTRIBUTES.COLOR, self.color)
        attributes.set_attr(self, n, constants.ATTRIBUTES.FILL, self.fill)
        attributes.set_attr(self, n, constants.ATTRIBUTES.VISIBLE, self.visible)
        attributes.set_attr(self, n, constants.ATTRIBUTES.ACTIVE, self.active)
        



class Library:
    TAG_NAME = constants.TAGS.LIBRARY
    PARENT_TAG_NAME = constants.TAGS.LIBRARIES
    
    ATTR_MAP = { constants.ATTRIBUTES.NAME: attributes.ATTR_STRING
                }
    
    def __init__(self, name = None, 
                 description = None,
                 packages = None, 
                 symbols = None, 
                 device_sets = None):
        self.packages = packages if packages else key_list.Key_List()
        self.symbols = symbols if symbols else key_list.Key_List()
        self.device_sets = device_sets if device_sets else key_list.Key_List()
        self.name = name
        self.description = description

    @classmethod
    def parse(cls, n):
        name = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.NAME, None)
        description = etree_utils.parse_text(n, constants.TAGS.DESCRIPTION, None)
        
        # Parse the packages and symbols, which don't have dependencies
        packages = etree_utils.parse_grandchildren_of_class_into_od(n, Package)
        symbols = etree_utils.parse_grandchildren_of_class_into_od(n, Symbol)
        
        # Create the library
        lib = Library(packages = packages, symbols = symbols, name = name, description = description)
        
        # Parse the device sets, which depend on the packages and symbols
        lib.device_sets = etree_utils.parse_grandchildren_of_class_into_od_with_obj(n, Device_Set, lib)

        return lib
    
    def append_node(self, _n):
        # Add this node
        n = ElementTree.SubElement(_n, constants.TAGS.LIBRARY)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.NAME, self.name, None)
        
        etree_utils.append_text_node_if_not_none(n, self.description, constants.TAGS.DESCRIPTION)
            
        etree_utils.append_grandchildren_of_class_from_od(n, Package, self.packages, False)
        etree_utils.append_grandchildren_of_class_from_od(n, Symbol, self.symbols, False)
        etree_utils.append_grandchildren_of_class_from_od(n, Device_Set, self.device_sets, False)
        

    

class Net:
    TAG_NAME = constants.TAGS.NET
    PARENT_TAG_NAME = constants.TAGS.NETS
    
    ATTR_MAP = {constants.ATTRIBUTES.NAME: attributes.ATTR_STRING,
                constants.ATTRIBUTES.CLASS: attributes.ATTR_INT}
    
    def __init__(self, 
                 name, 
                 net_class, 
                 segments = None):
        self.name = name
        self.net_class = net_class
        self.segments = segments if segments else []
        
    @classmethod
    def parse(cls, n):
        name = attributes.parse(cls, n, constants.ATTRIBUTES.NAME)
        net_class = attributes.parse(cls, n, constants.ATTRIBUTES.CLASS)
        
        segments = etree_utils.parse_children_using_function(n, Segment.parse, constants.TAGS.SEGMENT)
            
        return Net(name, net_class, segments)
        
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, constants.TAGS.NET)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.NAME, self.name)
        attributes.set_attr(self, n, constants.ATTRIBUTES.CLASS, self.net_class)
        
        # Add the segments
        for s in self.segments:
            s.append_node(n)
        

class Net_Class:
    TAG_NAME = constants.TAGS.CLASS
    PARENT_TAG_NAME = constants.TAGS.CLASSES
    
    ATTR_MAP = {constants.ATTRIBUTES.NUMBER: attributes.ATTR_INT,
                constants.ATTRIBUTES.NAME: attributes.ATTR_STRING,
                constants.ATTRIBUTES.WIDTH: attributes.ATTR_FLOAT,
                constants.ATTRIBUTES.DRILL: attributes.ATTR_FLOAT}
    
    def __init__(self, 
                 number, 
                 name, 
                 width, 
                 drill, 
                 clearances = None):
        self.number = number
        self.name = name
        self.width = width
        self.drill = drill
        self.clearances = clearances if clearances else []

    @classmethod
    def parse(cls, n):
        number = attributes.parse(cls, n, constants.ATTRIBUTES.NUMBER)
        name = attributes.parse(cls, n, constants.ATTRIBUTES.NAME)
        width = attributes.parse(cls, n, constants.ATTRIBUTES.WIDTH)
        drill = attributes.parse(cls, n, constants.ATTRIBUTES.DRILL)
        
        # Parse the clearances
        clearances = etree_utils.parse_children_of_class(n, Clearance)
        
        return Net_Class(number, name, width, drill, clearances)

    def append_node(self, _n):
        n = ElementTree.SubElement(_n, constants.TAGS.CLASS)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.NUMBER, self.number)
        attributes.set_attr(self, n, constants.ATTRIBUTES.NAME, self.name)
        attributes.set_attr(self, n, constants.ATTRIBUTES.WIDTH, self.width)
        attributes.set_attr(self, n, constants.ATTRIBUTES.DRILL, self.drill)
        
        # Add the clearances
        for c in self.clearances:
            c.append_node(n)
        

class Note:
    TAG_NAME = constants.TAGS.NOTE
    PARENT_TAG_NAME = constants.TAGS.COMPATIBILITY
    
    ATTR_MAP = { constants.ATTRIBUTES.VERSION: attributes.ATTR_STRING,
                constants.ATTRIBUTES.MIN_VERSION: attributes.ATTR_STRING,
                constants.ATTRIBUTES.SEVERITY: attributes.ATTR_STRING
                }
    
    def __init__(self, 
                 version, 
                 min_version, 
                 severity, 
                 message):
        self.version = version
        self.min_version = min_version
        self.severity = severity
        self.message = message

    @classmethod
    def parse(cls, n):
        version = attributes.parse(cls, n, constants.ATTRIBUTES.VERSION)
        min_version = attributes.parse(cls, n, constants.ATTRIBUTES.MIN_VERSION)
        severity = attributes.parse(cls, n, constants.ATTRIBUTES.SEVERITY)
        message = n.text
        
        return Note(version, min_version, severity, message)
    
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, constants.TAGS.NOTE)
        n.text = self.message
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.VERSION, self.version)
        attributes.set_attr(self, n, constants.ATTRIBUTES.MIN_VERSION, self.min_version)
        attributes.set_attr(self, n, constants.ATTRIBUTES.SEVERITY, self.severity)
        

class Package:
    TAG_NAME = constants.TAGS.PACKAGE
    PARENT_TAG_NAME = constants.TAGS.PACKAGES
    
    ATTR_MAP = {constants.ATTRIBUTES.NAME: attributes.ATTR_STRING}
    
    def __init__(self, 
                 name, 
                 description = None, 
                 items = None):
        self.name = name
        self.description = description
        self.items = items if items else []
        
    @classmethod
    def parse(cls, n):
        # Get the name
        name = attributes.parse(cls, n, constants.ATTRIBUTES.NAME)
        
        description = etree_utils.parse_text(n, constants.TAGS.DESCRIPTION, None)
        
        # Parse the contents
        items = etree_utils.parse_children_using_function(n, primitives.parse_item)
        
        return Package(name, description, items)

    def append_node(self, _n):
        n = ElementTree.SubElement(_n, constants.TAGS.PACKAGE)
        n.attrib[constants.ATTRIBUTES.NAME] = self.name
        
        etree_utils.append_text_node_if_not_none(n, self.description, constants.TAGS.DESCRIPTION)
        
        # Add the primitives
        for i in self.items:
            i.append_node(n)

class Param:
    TAG_NAME = constants.TAGS.PARAM
    
    ATTR_MAP = {constants.ATTRIBUTES.NAME: attributes.ATTR_STRING,
                constants.ATTRIBUTES.VALUE: attributes.ATTR_STRING
                }
        
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    @classmethod
    def parse(cls, n):
        name = attributes.parse(cls, n, constants.ATTRIBUTES.NAME)
        value = attributes.parse(cls, n, constants.ATTRIBUTES.VALUE)
        
        return Param(name, value)
    
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, constants.TAGS.PARAM)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.NAME, self.name)
        attributes.set_attr(self, n, constants.ATTRIBUTES.VALUE, self.value)
        
class Part:
    TAG_NAME = constants.TAGS.PART
    PARENT_TAG_NAME = constants.TAGS.PARTS
    
    ATTR_MAP = {constants.ATTRIBUTES.NAME: attributes.ATTR_STRING,
                constants.ATTRIBUTES.LIBRARY: attributes.ATTR_STRING,
                constants.ATTRIBUTES.DEVICE_SET: attributes.ATTR_STRING,
                constants.ATTRIBUTES.DEVICE: attributes.ATTR_STRING,
                constants.ATTRIBUTES.VALUE: attributes.ATTR_STRING,
                constants.ATTRIBUTES.TECHNOLOGY: attributes.ATTR_STRING}

    def __init__(self, 
                 name, 
                 library, 
                 device_set, 
                 device, 
                 value = None, 
                 attributes = None, 
                 technology=None, 
                 variants = None):
        self.name = name
        self.library = library
        self.device_set = device_set
        self.device = device
        self.value = value
        self.attributes = attributes if attributes else []
        self.technology = technology
        self.variants = variants if variants else []

    @classmethod
    def parse(cls, n, schematic):
        name = attributes.parse(cls, n, constants.ATTRIBUTES.NAME)
        
        library_name = attributes.parse(cls, n, constants.ATTRIBUTES.LIBRARY)
        library = schematic.libraries[library_name]
        
        device_set_name = attributes.parse(cls, n, constants.ATTRIBUTES.DEVICE_SET)
        device_set = library.device_sets[device_set_name]
        
        device_name = attributes.parse(cls, n, constants.ATTRIBUTES.DEVICE)
        device = device_set.devices[device_name]
        
        value = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.VALUE, None)
        technology = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.TECHNOLOGY, "")
        
        _attributes = etree_utils.parse_children_of_class(n, Device_Attribute)
        variants = etree_utils.parse_children_of_class(n, Variant)
        
        return Part(name, library, device_set, device, value, _attributes, technology, variants)
    
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, constants.TAGS.PART)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.NAME, self.name)
        attributes.set_attr(self, n, constants.ATTRIBUTES.LIBRARY, self.library.name)
        attributes.set_attr(self, n, constants.ATTRIBUTES.DEVICE_SET, self.device_set.name)
        attributes.set_attr(self, n, constants.ATTRIBUTES.DEVICE, self.device.name)
        attributes.set_attr(self, n, constants.ATTRIBUTES.VALUE, self.value)
        attributes.set_attr(self, n, constants.ATTRIBUTES.TECHNOLOGY, self.technology, "")
        
        for a in self.attributes:
            a.append_node(n)
            
        for v in self.variants:
            v.append_node(n)

class Pass:
    TAG_NAME = constants.TAGS.PASS
    
    DEFAULT_REFER = None
    DEFAULT_ACTIVE = False
    
    ATTR_MAP = {constants.ATTRIBUTES.NAME: attributes.ATTR_STRING,
                constants.ATTRIBUTES.REFER: attributes.ATTR_STRING,
                constants.ATTRIBUTES.ACTIVE: attributes.ATTR_BOOL}
    
    
    def __init__(self, name, refer, active, params):
        self.name = name
        self.refer = refer
        self.active = active
        self.params = params
        
    @classmethod
    def parse(cls, n):
        name = attributes.parse(cls, n, constants.ATTRIBUTES.NAME)
        refer = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.REFER, cls.DEFAULT_REFER)
        active = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.ACTIVE, cls.DEFAULT_ACTIVE)
        
        params = etree_utils.parse_children_of_class(n, Param)
            
        return Pass(name, refer, active, params)
        
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, constants.TAGS.PASS)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.NAME, self.name)
        attributes.set_attr(self, n, constants.ATTRIBUTES.REFER, self.refer, self.DEFAULT_REFER)
        attributes.set_attr(self, n, constants.ATTRIBUTES.ACTIVE, self.active, self.DEFAULT_ACTIVE)
       
        # Add the parameters
        for p in self.params:
            p.append_node(n) 

class Schematic:
    TAG_NAME = constants.TAGS.SCHEMATIC
    
    DEFAULT_XREF_LABEL = None
    DEFAULT_XREF_PART = None
    
    ATTR_MAP = { constants.ATTRIBUTES.XREF_LABEL: attributes.ATTR_STRING,
                constants.ATTRIBUTES.XREF_PART: attributes.ATTR_STRING
                }
    
    def __init__(self, 
                 libraries = None, 
                 parts = None, 
                 classes = None, 
                 sheets = None, 
                 errors = None, 
                 xref_label = DEFAULT_XREF_LABEL, 
                 xref_part = DEFAULT_XREF_PART, 
                 attributes = None,
                 variant_defs = None):
        self.libraries = libraries if libraries else key_list.Key_List()
        self.parts = parts if parts else key_list.Key_List()
        self.classes = classes if classes else []
        self.sheets = sheets if sheets else []
        self.errors = errors if errors else []
        self.xref_label = xref_label
        self.xref_part = xref_part
        self.attributes = attributes if attributes else []
        self.variant_defs = variant_defs if variant_defs else []
        
    @classmethod
    def parse(cls, n):
        xref_label = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.XREF_LABEL, cls.DEFAULT_XREF_LABEL)
        xref_part = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.XREF_PART, cls.DEFAULT_XREF_PART)
        libraries = etree_utils.parse_grandchildren_of_class_into_od(n, Library)
        classes = etree_utils.parse_grandchildren_of_class(n, Net_Class)
        errors = etree_utils.parse_grandchildren_of_class(n, Approved_Error)
        attribs = etree_utils.parse_grandchildren_of_class(n, Global_Attribute)
        variant_defs = etree_utils.parse_grandchildren_of_class(n, Variant_Def)
        
        schematic = Schematic(libraries = libraries,
                              classes = classes,
                              errors = errors,
                              xref_label = xref_label,
                              xref_part = xref_part,
                              attributes = attribs,
                              variant_defs = variant_defs)
                           
        schematic.parts = etree_utils.parse_grandchildren_of_class_into_od_with_obj(n, Part, schematic)

        schematic.sheets = etree_utils.parse_grandchildren_of_class_with_obj(n, Sheet, schematic)
        
        return schematic

    def append_node(self, _n):
        # Add this node
        n = ElementTree.SubElement(_n, constants.TAGS.SCHEMATIC)

        attributes.set_attr(self, n, constants.ATTRIBUTES.XREF_LABEL, self.xref_label, self.DEFAULT_XREF_LABEL)
        attributes.set_attr(self, n, constants.ATTRIBUTES.XREF_PART, self.xref_part, self.DEFAULT_XREF_PART)
        
        etree_utils.append_grandchildren_of_class_from_od(n, Library, self.libraries)
        etree_utils.append_grandchildren_of_class(n, Global_Attribute, self.attributes)
        etree_utils.append_grandchildren_of_class(n, Variant_Def, self.variant_defs)
        etree_utils.append_grandchildren_of_class(n, Net_Class, self.classes)
        etree_utils.append_grandchildren_of_class_from_od(n, Part, self.parts)
        etree_utils.append_grandchildren_of_class(n, Sheet, self.sheets)
        etree_utils.append_grandchildren_of_class(n, Approved_Error, self.errors, False)
#     
#     def get_lib_dict(self):
#         """
#         Returns a dictionary which can be used to associate a library name with a ``Library`` object.
#         
#         The returend dictionary takes the form:
#         
#             lib_dict = {
#                 library_name_1: library_1,
#                 library_name_2: library_2,
#                 ...
#             }
#         
#         """
#     
#     def get_device_set_dict(self):
#         """
#         Returns a dictionary which can be used to associate a library name and device set name
#         with a ``Device_Set`` object.
#         
#         The returned device set takes the form:
#         
#             device_set_dict = {
#                 library_name_1: {
#                     device_set_name_1: device_set_1
#                     device_set_name_2: device_set_2
#                     ...
#                 },
#                 library_name_2: {
#                     ...
#                 },
#                 ...
#             }
#         
#         """
#         
#         device_set_dict = {}
#         
#         for l in self.libraries:
#             device_sets = {}
#             
#             for ds in l.device_sets:
#                 device_sets[ds.name] = ds
#                             
#             device_set_dict[l.name] = device_sets
#             
#         return device_set_dict
#         
#     def get_device_dict(self):
#         """
#         Returns a dictionary which can be used to associate a library name, device set name, and device
#         with a ``Device`` object. 
#         
#         The returned set takes the form:
#             
#             device_dict = {
#                 library_name_1: {
#                     device_set_name_1: {
#                         device_name_1: device_1,
#                         device_name_2, device_2,
#                         ...
#                     },
#                     device_set_name_2: {
#                         ...
#                     },
#                     ...
#                 },
#                 library_name_2: {
#                     ...
#                 },
#                 ...
#             }
#         
#         """
#         
#         device_dict = {}
#         
#         for l in self.libraries:
#             device_sets = {}
#             
#             for ds in l.device_sets:
#                 devices = {}
#                 
#                 for d in ds.devices:
#                     devices[d.name] = d
#                     
#                 device_sets[ds.name] = devices
#                 
#             device_dict[l.name] = device_sets
#             
#         return device_dict
#         
#     def get_gate_dict(self, device_set_dict = None):
#         """
#         Return a dictionary which can be used to associate a part name and gate name with a ``Gate`` object.
#         
#         gate_dict = {
#             part_name_1: {
#                 gate_name_1: gate_1,
#                 gate_name_2, gate_2,
#                 ...
#             },
#             part_name_2: {
#                 ...
#             },
#             ...
#         }
#         
#         """
#         
#         if device_set_dict == None:
#             device_set_dict = self.get_device_set_dict()
#         
#         gate_dict = {}
#         
#         for p in self.parts:
#             device_set = device_set_dict[p.library][p.device_set]
#             
#             d = {}
#             
#             for g in device_set.gates:
#                 d[g.name] = g
#                
#             gate_dict[p.name] = d
#                 
#         return gate_dict
# 
#     def get_symbol_dict(self):
#         """
#         Return a dictionary which can be used to associate a library name and symbol name with a ``Symbol`` object.
#         
#         symbol_dict = {
#             library_name_1: {
#                 symbol_name_1: symbol_1,
#                 ...
#             },
#             ...
#         }
#         
#         """
#         
#         symbol_dict = {}
#         
#         for l in self.libraries:
#             lib_dict = {}
#             
#             for s in l.symbols:
#                 lib_dict[s.name] = s
#                 
#             symbol_dict[l.name] = lib_dict
#             
#         return symbol_dict
# 
#     def get_part_dict(self):
#         """
#         Return a dictionary which can be used to associate a part name with a ``Part`` object. 
#         
#         """
# 
#         parts = {}
#         
#         for p in self.parts:
#             parts[p.name] = p
#             
#         return parts
# 
#     def get_net_dict(self):
#         """
#         Return a dictionary which can be used to associate a net name with a ``Net`` object.
#         """
#         
#         sheets = {}
#         
#         for s in self.sheets:
#             nets = {}
#             for n in s.nets:
#                 nets[n.name] = n
#             sheets[s] = nets
#             
#         return sheets


class Segment:
    TAG_NAME = constants.TAGS.SEGMENT
    
    def __init__(self, items = None):
        self.items = items if items else []

    @classmethod
    def parse(cls, n):
        items = etree_utils.parse_children_using_function(n, primitives.parse_item, None)
        
        return Segment(items)
    
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, constants.TAGS.SEGMENT)
        
        for i in self.items:
            i.append_node(n)

class Setting:
    TAG_NAME = constants.TAGS.SETTING
    PARENT_TAG_NAME = constants.TAGS.SETTINGS
    
    ATTR_MAP = {constants.ATTRIBUTES.NAME: attributes.ATTR_STRING,
                constants.ATTRIBUTES.VALUE: attributes.ATTR_STRING}
    
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    @classmethod
    def parse(cls, n):
        name = n.attrib.keys()[0]
        value = n.attrib[name]
        return Setting(name, value)
        
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, self.TAG_NAME)
        n.attrib[self.name] = self.value



class Sheet:
    TAG_NAME = constants.TAGS.SHEET
    PARENT_TAG_NAME = constants.TAGS.SHEETS
    
    ATTR_MAP = {}
    
    def __init__(self, 
                 plain = None, 
                 instances = None, 
                 busses = None, 
                 nets = None, 
                 descriptions = None):
        self.plain = plain if plain else []
        self.instances = instances if instances else []
        self.nets = nets if nets else key_list.Key_List()
        self.descriptions = descriptions if descriptions else []
        self.busses = busses if busses else key_list.Key_List()
         
    @classmethod
    def parse(cls, n, schematic):
        descriptions = etree_utils.parse_children_using_function(n, Description.parse, constants.TAGS.DESCRIPTION)
        plain_items = etree_utils.parse_grandchildren_using_function(n, constants.TAGS.PLAIN, primitives.parse_item)
        instances = etree_utils.parse_grandchildren_of_class_with_obj(n, Instance, schematic)
        nets = etree_utils.parse_grandchildren_of_class_into_od(n, Net)
        busses = etree_utils.parse_grandchildren_of_class_into_od(n, Bus)
        
        return Sheet(plain_items, instances, busses, nets, descriptions)
        
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, constants.TAGS.SHEET)
    
        for d in self.descriptions:
            d.append_node(n)
        
        etree_utils.append_grandchildren_with_tag(n, constants.TAGS.PLAIN, self.plain)
        etree_utils.append_grandchildren_with_tag(n, constants.TAGS.INSTANCES, self.instances)
        etree_utils.append_grandchildren_with_tag_from_od(n, constants.TAGS.BUSSES, self.busses)
        etree_utils.append_grandchildren_with_tag_from_od(n, constants.TAGS.NETS, self.nets)

class Signal:
    TAG_NAME = constants.TAGS.SIGNAL
    PARENT_TAG_NAME = constants.TAGS.SIGNALS
    
    DEFAULT_SIGNAL_CLASS = 0
    DEFAULT_AIRWIRES_HIDDEN = False
    
    ATTR_MAP = { constants.ATTRIBUTES.NAME: attributes.ATTR_STRING,
                constants.ATTRIBUTES.SIGNAL_CLASS: attributes.ATTR_INT,
                constants.ATTRIBUTES.AIRWIRES_HIDDEN: attributes.ATTR_BOOL
                }
    
    def __init__(self, 
                 name, 
                 signal_class = DEFAULT_SIGNAL_CLASS, 
                 airwires_hidden = DEFAULT_AIRWIRES_HIDDEN, 
                 items = None):
        self.name = name
        self.signal_class = signal_class
        self.airwires_hidden = airwires_hidden
        self.items = items if items else []
            
    @classmethod
    def parse(cls, n):
        name = attributes.parse(cls, n, constants.ATTRIBUTES.NAME)
        signal_class = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.SIGNAL_CLASS, cls.DEFAULT_SIGNAL_CLASS)
        airwires_hidden = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.AIRWIRES_HIDDEN, cls.DEFAULT_AIRWIRES_HIDDEN)
        
        items = etree_utils.parse_children_using_function(n, primitives.parse_item)
            
        return Signal(name, signal_class, airwires_hidden, items)
        
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, constants.TAGS.SIGNAL)
        
        attributes.set_attr(self, n, constants.ATTRIBUTES.NAME, self.name)
        attributes.set_attr(self, n, constants.ATTRIBUTES.SIGNAL_CLASS, self.signal_class, self.DEFAULT_SIGNAL_CLASS)
        attributes.set_attr(self, n, constants.ATTRIBUTES.AIRWIRES_HIDDEN, self.airwires_hidden, self.DEFAULT_AIRWIRES_HIDDEN)
        
        # Add the primitives
        for i in self.items:
            i.append_node(n)
                

class Symbol:
    TAG_NAME = constants.TAGS.SYMBOL
    PARENT_TAG_NAME = constants.TAGS.SYMBOLS
    
    ATTR_MAP = {constants.ATTRIBUTES.NAME: attributes.ATTR_STRING}
    
    def __init__(self, 
                 name, 
                 description = None, 
                 items = None):
        self.name = name
        self.description = description
        self.items = items if items else []
        
    @classmethod
    def parse(cls, n):
        # Get the name
        name = attributes.parse(cls, n, constants.ATTRIBUTES.NAME)
        
        description = etree_utils.parse_text(n, constants.TAGS.DESCRIPTION, None)
        
        # Parse the contents
        items = etree_utils.parse_children_using_function(n, primitives.parse_item)
                        
        return Symbol(name, description, items)
    
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, constants.TAGS.SYMBOL) 
        n.attrib[constants.ATTRIBUTES.NAME] = self.name
        
        etree_utils.append_text_node_if_not_none(n, self.description, constants.TAGS.DESCRIPTION)
            
        # Add the primitives
        for i in self.items:
            i.append_node(n)

class Technology:
    TAG_NAME = constants.TAGS.TECHNOLOGY
    PARENT_TAG_NAME = constants.TAGS.TECHNOLOGIES
    
    ATTR_MAP = {constants.ATTRIBUTES.NAME: attributes.ATTR_STRING}
    
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes
        
    @classmethod
    def parse(cls, n):
        name = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.NAME, None)
        attrs = etree_utils.parse_children_of_class(n, Device_Attribute)
        return Technology(name, attrs)
        
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, self.TAG_NAME)
        attributes.set_attr(self, n, constants.ATTRIBUTES.NAME, self.name, None)
        
        for a in self.attributes:
            a.append_node(n)
        
class Variant:
    TAG_NAME = constants.TAGS.VARIANT
    
    ATTR_MAP = {constants.ATTRIBUTES.NAME: attributes.ATTR_STRING,
                constants.ATTRIBUTES.TECHNOLOGY: attributes.ATTR_STRING,
                constants.ATTRIBUTES.VALUE: attributes.ATTR_STRING
                }
    
    def __init__(self, name, technology, value):
        self.name = name
        self.technology = technology
        self.value = value
        
    @classmethod
    def parse(cls, n):
        name = attributes.parse(cls, n, constants.ATTRIBUTES.NAME)
        technology = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.TECHNOLOGY, None)
        value = attributes.parse_or_default(cls, n, constants.ATTRIBUTES.VALUE, None)
        return Variant(name, technology, value)
        
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, self.TAG_NAME)
        attributes.set_attr(self, n, constants.ATTRIBUTES.NAME, self.name)
        attributes.set_attr(self, n, constants.ATTRIBUTES.TECHNOLOGY, self.technology, None)
        attributes.set_attr(self, n, constants.ATTRIBUTES.VALUE, self.value, None)
        
class Variant_Def:
    TAG_NAME = constants.TAGS.VARIANT_DEF
    PARENT_TAG_NAME = constants.TAGS.VARIANT_DEFS
    
    ATTR_MAP = {constants.ATTRIBUTES.NAME: attributes.ATTR_STRING}
    
    def __init__(self, name):
        self.name = name
        
    @classmethod
    def parse(cls, n):
        name = attributes.parse(cls, n, constants.ATTRIBUTES.NAME)
        return Variant_Def(name)
    
    def append_node(self, _n):
        n = ElementTree.SubElement(_n, self.TAG_NAME)
        attributes.set_attr(self, n, constants.ATTRIBUTES.NAME, self.name)





        



        

        

   

