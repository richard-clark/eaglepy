"""
XML Compare
===========

Provides basic functionality for comparing XML documents.

This functionality is sensitive to the order of XML nodes within a document.

For every node in the first document, there must be a corresponding node
in the second document with the same tag and attributes (attribute does not order),
same parent, and same number of siblings both before and after. Each node must have
the same number of children.

Trees are compared recursively.

The ``ignore_empty_tags`` parameter specifies whether an element with no attributes,
no children, and no text (other than whitespace) is equivalent to the absence of a tag.

By default, two attributes are compared as strings. This can be overriden by specifying
a different function for the ``compare_function`` parameter, which accepts two strings,
and returns a Boolean value indicting whether the strings are equal.

There is no difference in precedence between two XML files, two trees, or two nodes: the
result of any compare function will be the same regardless of the order of the arguments.

The ``compare_tree()`` method (and thus, the ``compare_files()`` method) returns ``None``,
and will raise an ``Exception`` if two nodes are not equal.

Two files ``foo.xml`` and ``bar.xml`` can be compared using:

    compare_files('foo.xml', 'bar.xml')
    
Two ``ElementTree`` objects ``foo`` and ``bar`` can be compared using:

    compare_tree(foo, bar)

"""

from lxml import etree as ElementTree

def compare_function_equal(val1, val2):
    """
    A basic string equality comparison function.
    
    :param val1: The first string to compare.
    :param val2: The second string to compare. 
    
    :returns: Whether the strings are equal.
    """
    
    return val1 == val2

def remove_empty_children(node, ignore_whitespace):
    """
    Remove all "empty" children from an ``Element`` object. 
    
    These are children which have no attributes, no children, and no (non-whitespace) text.
    
    :param node: The node from which to remove empty children.
    """
    
    children = node.getchildren()
    
    for i in range(len(children)-1,-1,-1):
        c = children[i]
        
        if ignore_whitespace and c.text != None:
            text = c.text.strip()
            if len(text) == 0:
                text = None
        else:
            text = c.text
        
        if len(c.getchildren()) == 0 and len(c.attrib.keys()) == 0 and text == None:
            print('Removing empty child {0}.'.format(c.tag))
            node.remove(c)
    
def compare_text(t1, t2, ignore_whitespace):
    
    if t1 == None:
        t1 = ''
    elif ignore_whitespace:
        t1 = t1.strip()
        
    if t2 == None:
        t2 = ''
    elif ignore_whitespace:
        t2 = t2.strip()
    
    return t1 == t2
    
    

def compare_nodes(n1, n2, compare_function, ignore_empty_tags, ignore_whitespace):
    """
    Compare two ``Element`` objects.
    
    Ensure that the tag names, attributes, and number of children all match. Recursively test each child.
    
    Note: if ``ignore_empty_tags`` is ``True``, this method may mutate either ``ElementTree`` object.
    
    :param ref_tree: The first node to compare.
    :param cmp_tree: The second node to compare.
    :param compare_function: The function to use to determine the equality of two attribute values.
    :param ignore_empty_tags: Whether tags with no attributes, no children, and no (non-whitespace) text can be removed for comparison purposes.
    
    :raises: An ``Exception`` if the trees are not identical.
    """
    
    # Compare the tag names.
    if n1.tag != n2.tag:
        raise Exception('Tag mismatch: ref = {0} (line {1}); cmp = {2} (line {3}).'.format(n1.tag, n1.sourceline, n2.tag, n2.sourceline))
    
    # Compare the attributes 
    keys_1 = n1.attrib.keys()
    
    for k in keys_1:
        if n2.attrib.has_key(k) == False:
            raise Exception('Cmp node with tag {0} is missing attribute {1} at line {2}.'.format(n2.tag, k, n2.sourceline))
        
    keys_2 = n2.attrib.keys()
    
    for k in keys_2:
        if n1.attrib.has_key(k) == False:
            raise Exception('Ref node with tag {0} is missing attribute {1} at line {2}.'.format(n1.tag, k, n1.sourceline))
    
    for k in keys_1:
        val_1 = n1.attrib[k]
        val_2 = n2.attrib[k]
        
        if not compare_function(val_1, val_2):
            raise Exception('Attribute mismatch attribute {0} for tag {1}: ref = {2} (line {3}); cmp = {4} (line {5}).'.format(k, n1.tag, val_1, n1.sourceline, val_2, n2.sourceline))
    
    # Compare the children
    children_1 = n1.getchildren()
    children_2 = n2.getchildren()
    
    if len(children_1) != len(children_2):
        
        child_mismatch = True
        
        if ignore_empty_tags:
            remove_empty_children(n1, ignore_whitespace)
            remove_empty_children(n2, ignore_whitespace)
            
            children_no_empty_1 = n1.getchildren()
            children_no_empty_2 = n2.getchildren()
        
            if len(children_no_empty_1) == len(children_no_empty_2):
                print('Warning--removed empty nodes from tag {0} at line {1} ({2} and {3}).'.format(n1.tag, n1.sourceline, len(children_1) - len(children_no_empty_1), len(children_2) - len(children_no_empty_2)))
                
                children_1 = children_no_empty_1
                children_2 = children_no_empty_2
                
                child_mismatch = False
                 
        if child_mismatch:
            raise Exception('Child count mismatch in node with tag {0} at line {3}: {1} vs. {2}.'.format(n1.tag, len(children_1), len(children_2), n1.sourceline))
    
    if len(children_1) == 0:
        
        if not compare_text(n1.text, n2.text, ignore_whitespace):
            
            s1 = None if n1.text == None else '"' + n1.text + '"'
            s2 = None if n2.text == None else '"' + n2.text + '"'
            
            raise Exception('Text mismatch in node with tag {0} at line {1}: {2} vs. {3}.'.format(n1.tag, n1.sourceline, s1, s2)) 
    else:
        for i in range(len(children_1)):
            child_1 = children_1[i]
            child_2 = children_2[i]
            
            compare_nodes(child_1, child_2, compare_function, ignore_empty_tags, ignore_whitespace)
        
def compare_tree(ref_tree, cmp_tree, compare_function = compare_function_equal, ignore_empty_tags = True, ignore_whitespace = True):
    """
    Compare two ``ElementTree`` objects.
    
    Note: if ``ignore_empty_tags`` is ``True``, this method may mutate either ``ElementTree`` object.
    
    :param ref_tree: The first tree to compare.
    :param cmp_tree: The second object to compare.
    :param compare_function: The function to use to determine the equality of two attribute values.
    :param ignore_empty_tags: Whether tags with no attributes, no children, and no (non-whitespace) text can be removed for comparison purposes.
    
    :raises: An ``Exception`` if the trees are not identical.
    """

    ref_has_docinfo = ref_tree.docinfo.standalone != None
    cmp_has_docinfo = cmp_tree.docinfo.standalone != None

    if ref_has_docinfo != cmp_has_docinfo:
        raise Exception('Docinfo mismatch: present in ref = {0}; present in cmp = {1}.'.format(ref_has_docinfo, cmp_has_docinfo))

    if ref_has_docinfo:
        ref_version = ref_tree.docinfo.xml_version
        cmp_version = cmp_tree.docinfo.xml_version
        
        ref_encoding = ref_tree.docinfo.xml_version
        cmp_encoding = cmp_tree.docinfo.xml_version
        
        if ref_version != cmp_version:
            raise Exception('Docinfo version mismatch: ref = {0}; cmp = {1}.'.format(ref_version, cmp_version))
        
        if ref_encoding != cmp_encoding:
            raise Exception('Docinfo encoding mismatch: ref = {0}; cmp = {1}'.format(ref_encoding, cmp_encoding))
        
        if ref_tree.docinfo.doctype != cmp_tree.docinfo.doctype:
            raise Exception('Docinfo doctype mismatch: ref = {0}; cmp = {1}'.format(ref_tree.docinfo.doctype, cmp_tree.docinfo.doctype))
        
    ref_root = ref_tree.getroot()
    cmp_root = cmp_tree.getroot()

    compare_nodes(ref_root, cmp_root, compare_function, ignore_empty_tags, ignore_whitespace)


def compare_files(file_1, file_2, compare_function = compare_function_equal, ignore_empty_tags = True, ignore_whitespace = True):
    """
    Compare two XML files.
    
    :param file_1: The path to the first file to compare.
    :param file_2: The path to the second file to compare.
    :param compare_function: The function to use to determine the equality of two attribute values.
    :param ignore_empty_tags: Whether tags with no attributes, no children, and no (non-whitespace) text can be removed for comparison purposes.
    
    :raises: An ``Exception`` if the trees are not identical.
    """
    
    dom1 = ElementTree.parse(file_1)
    dom2 = ElementTree.parse(file_2)
    compare_tree(dom1, dom2, compare_function, ignore_empty_tags, ignore_whitespace)
    
    
if __name__ == '__main__':
    t1 = None
    t2 = """
"""
    print(compare_text(t1, t2, True))
