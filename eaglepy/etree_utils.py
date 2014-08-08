"""
Etree Utilities
===============

Provides helper functions for parsing XML data as objects, and for serialing
objects as XML data.

``parse`` methods are used to parse XML data (from an ElementTree ``Element``) object. 

``append`` methods are used to convert objects into XML and append them to an existing
ElementTree ``Element`` object.

For methods which accept classes as parameters, the class must have a 
``TAG_NAME`` property.

For methods which accept classes and operate on grandchildren (either parsing 
or appending), the class must additionally have a ``PARENT_TAG_NAME`` property.

The following class would be valid:

    class Foo:
        TAG_NAME = 'foo'
        PARENT_TAG_NAME = 'foos'


"""

import key_list

try:
    from lxml import etree as ElementTree
except:
    from xml.etree import ElementTree

def append_text_node_if_not_none(parent, text, tag_name):
    """
    If ``text`` is not ``None``, add an ``Element`` whose ``text`` value is equal to ``text``.
    
    :param parent: The parent ``Element`` object. 
    :param text: The value for the ``text`` property, or None. 
    :param tag_name: The tag name to use if ``text`` is not None.
    
    """
    
    if text != None:
        n = ElementTree.SubElement(parent, tag_name)
        n.text = text

def parse_text(parent, child_tag, default=None):
    """
    If a child element with the specified tag exists, return its text content. Otherwise, return a default value.
    
    :param parent: The parent Element object.
    :param child_tag: The tag name of the child elemenet. 
    :param default: The defualt value to return if no child exists with the specified tag.
    
    """
    node = parent.find(child_tag)
    
    if node == None:
        return default
    else:
        return node.text

def parse_child_of_class(parent, child_class, optional = True):
    """
    Find and parse a single instance of the specified class.
    
    :param parent: The parent Element object.
    :param child_class: The class of the child.
    :param optional: If False, raise an exception if no node is found.
    
    :raises: An Exception if no node is found and ``optional`` is ``False``.
    
    :returns: An object of child_class, or ``None`` if no object is found and ``optional`` is ``True``.
    
    """
    
    node = parent.find(child_class.TAG_NAME)
    
    if node == None and not optional:
        raise Exception('Node {0} does not contain required child node {1}.'.format(parent.tag, child_class.TAG_NAME))
    
    return child_class.parse(node)
    
def parse_children_of_class(parent, child_class):
    """
    Find and parse all instances of the specified class.
    
    :param parent: The parent ``Element`` object.
    :param child_class: The class of the children.
    
    :returns: A list of objects of the type child_class.
    
    """
    
    children = []
    
    nodes = parent.findall(child_class.TAG_NAME)
    
    for n in nodes:
        c = child_class.parse(n)
        if c != None:
            children.append(c)
        
    return children

def parse_grandchildren_of_class(parent, child_class, optional = True):
    """
    Find and parse all instances of the specified class contained by the child element with
    the tag name specified by the ``PARENT_TAG_NAME`` attribute of ``child_class``.
    
    :param parent: The parent ``Element`` object. 
    :param child_class: The class of the grandchildren.
    :param optional: If False, raise an exception if no parent node is found.
    
    :raises: An Exception if no parent node with the tag name specified by 
        ``child_class.PARENT_TAG_NAME`` is found and ``optional`` is ``False``.
    
    :returns: A list of objects of the type child_class.
    
    """
    
    node = parent.find(child_class.PARENT_TAG_NAME)
    
    if node == None:
        if optional:
            return []
        else:
            raise Exception('Node {0} does not contain required child node {1}.'.format(parent.tag, child_class.TAG_NAME))
    else:
        nodes = node.findall(child_class.TAG_NAME)
        children = []
            
        for n in nodes:
            c = child_class.parse(n)
            if c != None:
                children.append(c)
            
        return children


def parse_grandchildren_of_class_with_obj(parent, child_class, obj, optional = True):
    """
    Find and parse all instances of the specified class contained by the child element with
    the tag name specified by the ``PARENT_TAG_NAME`` attribute of ``child_class``.
    
    :param parent: The parent ``Element`` object. 
    :param child_class: The class of the grandchildren.
    :param optional: If False, raise an exception if no parent node is found.
    
    :raises: An Exception if no parent node with the tag name specified by 
        ``child_class.PARENT_TAG_NAME`` is found and ``optional`` is ``False``.
    
    :returns: A list of objects of the type child_class.
    
    """
    
    node = parent.find(child_class.PARENT_TAG_NAME)
    
    if node == None:
        if optional:
            return []
        else:
            raise Exception('Node {0} does not contain required child node {1}.'.format(parent.tag, child_class.TAG_NAME))
    else:
        nodes = node.findall(child_class.TAG_NAME)
        children = []
            
        for n in nodes:
            c = child_class.parse(n, obj)
            if c != None:
                children.append(c)
            
        return children


def parse_grandchildren_of_class_into_od(parent, child_class, optional = True):
    """
    Find and parse all instances of the specified class contained by the child element with
    the tag name specified by the ``PARENT_TAG_NAME`` attribute of ``child_class`` and return
    an OrderedDict.
    
    The key for the OrderedDict is the ``name`` property of the parsed object.
    
    :param parent: The parent ``Element`` object. 
    :param child_class: The class of the grandchildren.
    :param optional: If False, raise an exception if no parent node is found.
    
    :raises: An Exception if no parent node with the tag name specified by 
        ``child_class.PARENT_TAG_NAME`` is found and ``optional`` is ``False``.
    
    :returns: An OrderedDict of objects of the type child_class.
    
    """
    
    node = parent.find(child_class.PARENT_TAG_NAME)
    
    if node == None:
        if optional:
            return key_list.Key_List()
        else:
            raise Exception('Node {0} does not contain required child node {1}.'.format(parent.tag, child_class.TAG_NAME))
    else:
        nodes = node.findall(child_class.TAG_NAME)
        children = key_list.Key_List()
            
        for n in nodes:
            c = child_class.parse(n)
            if c != None:
                children.append(c)

        return children

def parse_grandchildren_of_class_into_od_with_obj(parent, child_class, obj, optional = True):
    """
    Find and parse all instances of the specified class contained by the child element with
    the tag name specified by the ``PARENT_TAG_NAME`` attribute of ``child_class`` and return
    an OrderedDict.
    
    The key for the OrderedDict is the ``name`` property of the parsed object.
    
    :param parent: The parent ``Element`` object. 
    :param child_class: The class of the grandchildren.
    :param optional: If False, raise an exception if no parent node is found.
    
    :raises: An Exception if no parent node with the tag name specified by 
        ``child_class.PARENT_TAG_NAME`` is found and ``optional`` is ``False``.
    
    :returns: An OrderedDict of objects of the type child_class.
    
    """
    
    node = parent.find(child_class.PARENT_TAG_NAME)
    
    if node == None:
        if optional:
            return key_list.Key_List()
        else:
            raise Exception('Node {0} does not contain required child node {1}.'.format(parent.tag, child_class.TAG_NAME))
    else:
        nodes = node.findall(child_class.TAG_NAME)
        children = key_list.Key_List()
            
        for n in nodes:
            c = child_class.parse(n, obj)
            if c != None:
                children.append(c)
                
        return children

def parse_children_using_function(parent, parse_function, tag = None):
    """
    Find and parse children using a specified function. 
    
    :param parent: The parent ``Element`` object. 
    :param parse_function: A function which accepts an ``Element`` and returns an object. 
    :param tag: The tag name of the specific type of child to parse, or None to parse all children.
    
    :returns: A list of objects.

    """

    children = []
    
    if tag == None:
        nodes = parent.getchildren()
    else:
        nodes = parent.findall(tag)
    
    for n in nodes:
        c = parse_function(n)
        if c != None:
            children.append(c)
        
    return children

def parse_grandchildren_using_function(parent, child_tag, parse_function, tag = None, optional = False):
    """
    Find and parse grandchildren using a specified function.
    
    :param parent: The parent ``Element`` object.
    :param child_tag: The name of the child tag.
    :param parse_function: A function which accepts an ``Element`` and returns an object.
    :param tag: Thet ag name of tehs pecific type of grandchild to parse, or None to parse all grandchildren. 
    :param optional: If False, raise an exception if no parent node is found.
    
    :raises: An Exception if no parent node with the tag name specified by 
        ``child_class.PARENT_TAG_NAME`` is found and ``optional`` is ``False``.
    
    :returns: A list of objects.
    """

    node = parent.find(child_tag)
     
    if node == None:
        if optional:
            return []
        else:
            raise Exception('Node {0} does not contain required child node {1}.'.format(parent.tag, tag))
    else:
        if tag == None:
            nodes = node.getchildren()
        else:
            nodes = node.findall(tag)
             
        children = []
             
        for n in nodes:
            c = parse_function(n)
            if c != None:
                children.append(c)
             
        return children


def append_grandchildren_with_tag(parent, tag, children, add_node_if_empty = True):
    """
    Add a single child node and a grandchild for each object in ``children``.
    
    :param parent: The parent ``Element`` object. 
    :param tag: The name of the parent tag.
    :param child: A list of grandchildren.
    :param add_node_if_empty: Whether to add the parent node if the list of grandchildren is empty.
    
    """
    if not add_node_if_empty and len(children) == 0:
        return
    
    n = ElementTree.SubElement(parent, tag)
    
    for c in children:
        c.append_node(n)


def append_grandchildren_of_class(parent, child_class, children, add_node_if_empty = True):
    """
    Add a single child node and a grandchild for each object in ``children``.
    
    The tag of the parent is set by the ``child_class.PARENT_TAG_NAME`` attribute.

    :param parent: The parent ``Element`` object. 
    :param child_class: The class of the grandchild objects. 
    :param child: A list of grandchildren.
    :param add_node_if_empty: Whether to add the parent node if the list of grandchildren is empty.
    
    """
    
    append_grandchildren_with_tag(parent, child_class.PARENT_TAG_NAME, children, add_node_if_empty)
    
def append_grandchildren_with_tag_from_od(parent, tag, children, add_node_if_empty = True):
    """
    Add a single child node and a grandchild for each object in ``children``.
    
    :param parent: The parent ``Element`` object. 
    :param tag: The name of the parent tag.
    :param child: A list of grandchildren.
    :param add_node_if_empty: Whether to add the parent node if the list of grandchildren is empty.
    
    """
    if not add_node_if_empty and len(children) == 0:
        return
    
    n = ElementTree.SubElement(parent, tag)
    
    for c in children:
        c.append_node(n)


def append_grandchildren_of_class_from_od(parent, child_class, children, add_node_if_empty = True):
    """
    Add a single child node and a grandchild for each object in ``children``.
    
    The tag of the parent is set by the ``child_class.PARENT_TAG_NAME`` attribute.

    :param parent: The parent ``Element`` object. 
    :param child_class: The class of the grandchild objects. 
    :param child: A list of grandchildren.
    :param add_node_if_empty: Whether to add the parent node if the list of grandchildren is empty.
    
    """
    
    append_grandchildren_with_tag_from_od(parent, child_class.PARENT_TAG_NAME, children, add_node_if_empty)