"""
Attributes
==========

Provides functionality for converting EAGLE types representing in XML to 
Python representations, and for converting Python representations to EAGLE types in XML.

Attribute Classes
-----------------

The ``ATTR_`` classes correspond to types of attributes in EAGLE.

Each ``ATTR_`` class has two methods: ``parse`` and ``to_str``. ``parse`` accepts
a string and either returns a representation of that string, or raises an ``Exception``.
``to_str`` accepts an object and returns its string representation.

The following classes are easily converted two and from native python types:

* ATTR_STRING
* ATTR_INT
* ATTR_FLOAT

The following require more complex conversion:

* ATTR_EXTENT: represents the start and end layers of via.
* ATTR_BOOL: represents a Boolean value, with string values 'yes' and 'no'.
* ATTR_ON_OFF: represents a Boolean value, with string values 'on' and 'off'.
* ATTR_AUTO_FLOAT: represents a floating-point value with an additional 'auto' value.
* ATTR_ROT: represents a 

Note: one attribute name (from constants.ATTRIBUTES) may have different types depending
on the parent object. 

"""

import constants

class Rotation:
    """
    Represents a rotation attribute. This includes not only angle, but also whether an object is mirrored or spun. 
    """
    
    def __init__(self, angle = 0, mirrored = False, spin = False):
        self.angle = angle
        self.mirrored = mirrored 
        self.spin = spin
        
    def is_set(self):
        return (self.angle != 0 or self.mirrored or self.spin)
    
    def __eq__(self, other):
        return other != None and (self.angle == other.angle and self.mirrored == other.mirrored and self.spin == other.spin)
     
    def __ne__(self, other):
        return not self.__eq__(other)
 
class Extent:
    """
    Represents an extent. Used for ``Via`` elements, and specifies the start and end layers.
    """
    def __init__(self, layer_from, layer_to):
        self.layer_from = layer_from
        self.layer_to = layer_to
 
class ATTR_EXTENT:
    
    @staticmethod
    def parse(val):
        index = val.find('-')
        assert(index > -1)
        
        layer_from = int(val[:index])
        layer_to = int(val[index+1:])
        
        return Extent(layer_from, layer_to)
    
    @staticmethod
    def to_str(val):    
        if val == None:
            return None
        
        return '{0}-{1}'.format(val.layer_from, val.layer_to)
    
 
class ATTR_STRING:
    @staticmethod
    def parse(val):
        return val
    
    @staticmethod
    def to_str(val):
        if val == None:
            return None
        return val
    
class ATTR_BOOL:
    @staticmethod
    def parse(val):
        if val == constants.TRUE:
            return True
        
        if val == constants.FALSE:
            return False
        
        raise Exception('Invalid boolean value {0}; expecting "yes" or "no".'.format(val))
     
    @staticmethod
    def to_str(val):
        if val == True:
            return constants.TRUE
        else:
            return constants.FALSE
       
class ATTR_ON_OFF:
    @staticmethod
    def parse(val):
        if val.lower() == 'on':
            return True
        
        return False
    
    @staticmethod
    def to_str(val):
        if val:
            return 'on'
        else:
            return 'off'
       
class ATTR_INT:
    @staticmethod
    def parse(val):
        try:
            return int(val)
        except:
            raise Exception('Invalid integer value {0}.'.format(val))
        
    @staticmethod
    def to_str(val):
        return str(val)

class ATTR_FLOAT:
    @staticmethod
    def parse(val):
        try:
            return float(val)
        except:
            raise Exception('Invalid floating-point value {0}.'.format(val))

    @staticmethod
    def to_str(val):
        return str(val)
    
class ATTR_AUTO_FLOAT:
    @staticmethod
    def parse(val):
        if val.lower() == 'auto':
            return None
        
        try:
            return float(val)
        except:
            raise Exception('Invalid auto/float value {0}--expecting floating point number or "auto".'.format(val))
    
    @staticmethod
    def to_str(val):
        if val == None:
            return None
        else:
            return str(val)
    
class ATTR_ROT:
    @staticmethod
    def parse(val):
        angle = None
        spin = False
        mirror = False
        index = 0
        
        while index < len(val):
            if val[index] == 'M':
                mirror = True
                index += 1
                continue
            elif val[index] == 'S':
                spin = True
                index += 1
                continue
            elif val[index] == 'R':
                try:
                    angle = float(val[index+1:])
                except:
                    raise Exception('Invalid rotation angle in string "{0}".'.format(val))
                break
            else:
                raise Exception('Invalid character in rotation string "{0}".'.format(val))
            
            index += 1
        
        if angle == None:
            raise Exception('Rotation string "{0}" does not contain a rotation angle.'.format(val))
        
        return Rotation(angle, mirror, spin)
                
 
    @staticmethod
    def to_str(val):
        out_str = ''
        
        if val.mirrored:
            out_str += 'M'
            
        if val.spin:
            out_str += 'S'
            
        out_str += 'R'
            
        return out_str + str(val.angle)

def parse(cls, n, attr):
    """
    Convert the value for an ElementTree ``Element`` attribute to its Python representation.
    
    :param cls: A class with an ``ATTR_MAP`` property.
    :param n: An ElementTree ``Element`` object. 
    :param attr: The name of the attribute to parse.
    
    :raises: An ``Exception`` if an error occurs while parsing the value.
    
    :returns: The parsed attribute value. 
    """
    
    value = n.attrib[attr]
    
    if cls.ATTR_MAP.has_key(attr):
        f = cls.ATTR_MAP[attr]
        return f.parse(value)
    
    return value

def parse_or_default(cls, n, attr, default):
    """
    Convert the value for an ElementTree ``Element`` attribute to its Python representation,
    or return a default value if the ``Element`` does not have the specified attribute.
    
    :param cls: A class with an ``ATTR_MAP`` property.
    :param n: An ElementTree ``Element`` object. 
    :param attr: The name of the attribute to parse.
    :param default: The value to return if the ``Element`` does not have the specified attribute.
    
    :raises: An ``Exception`` if an error occurs while parsing the value.
    
    :returns: The parsed attribute value or the ``default`` value.
    
    """
    
    if n.attrib.has_key(attr):
        return parse(cls, n, attr)
    else:
        return default
    
def set_attr(obj, n, attr, val, default = None):
    """
    Set the specified attribute of an ElementTree ``Element`` object to the value from the
    specified target. 
    
    :param obj: An object which contains an ``ATTR_MAP`` property.
    :param n: An ElementTree ``Element`` object. 
    :param attr: The name of the attribute to set.
    :param val: The value of the attribute to set.
    :param default: The default value of ``val``. If ``val==default``, the attribute will not be set.
    
    """
    
    if default != None and val == default:
        return
    
    if obj.ATTR_MAP.has_key(attr):
        f = obj.ATTR_MAP[attr]
        s = f.to_str(val)
        if s != None:
            n.attrib[attr] = s
        return
    
    if val != None:
        s = str(val)
        n.attrib[attr] = s
