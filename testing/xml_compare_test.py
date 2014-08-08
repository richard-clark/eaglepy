"""

Unit testing for the XML Compare module.

"""

import StringIO
import xml_compare
import unittest

def file_obj_from_string(s):
    f = StringIO.StringIO()
    f.write(s)
    f.seek(0)
    return f

def get_xml_declaration(version, encoding):
    s = '<?xml'
    
    if version != None:
        s += ' version="' + version + '"'
        
    if encoding != None:
        s += ' encoding="' + encoding + '"'

    return s + "?>"

def get_xml_doctype(root_name, identifier, system_url):
    return '<!DOCTYPE {0} {1} "{2}">'.format(root_name, identifier, system_url)

class TestXMLCompareFunctions(unittest.TestCase):
    
    def test_local_functions(self):
        # XML declaration
        self.assertEqual(get_xml_declaration('1.0', 'utf-8'), '<?xml version="1.0" encoding="utf-8"?>')
        self.assertEqual(get_xml_declaration('1.0', None), '<?xml version="1.0"?>')
        self.assertEqual(get_xml_declaration(None, 'utf-8'), '<?xml encoding="utf-8"?>')
        self.assertEqual(get_xml_declaration(None, None), '<?xml?>')

        # XML doctype
        self.assertEqual(get_xml_doctype('eagle', 'SYSTEM', 'eagle.dtd'), '<!DOCTYPE eagle SYSTEM "eagle.dtd">')

    def test_successful_compare(self):
        # Basic document
        doc_1 = get_xml_declaration('1.0', 'utf-8') + get_xml_doctype('foo', 'SYSTEM', 'test.dtd') + '<foo><bar /></foo>'
        doc_2 = get_xml_declaration('1.0', 'utf-8') + get_xml_doctype('foo', 'SYSTEM', 'test.dtd') + '<foo><bar /></foo>'
        f1 = file_obj_from_string(doc_1)
        f2 = file_obj_from_string(doc_2)
        self.assertIsNone(xml_compare.compare_files(f1, f2))

    def test_doctype_version_mismatch(self):
        # Basic document
        doc_1 = get_xml_declaration('1.0', 'utf-8') + get_xml_doctype('foo', 'SYSTEM', 'test.dtd') + '<foo><bar /></foo>'
        doc_2 = get_xml_declaration('1.1', 'utf-8') + get_xml_doctype('foo', 'SYSTEM', 'test.dtd') + '<foo><bar /></foo>'
        f1 = file_obj_from_string(doc_1)
        f2 = file_obj_from_string(doc_2)
        self.assertRaises(Exception, xml_compare.compare_files, (f1, f2))

    def test_doctype_encoding_mismatch(self):
        # Basic document
        doc_1 = get_xml_declaration('1.0', 'utf-8') + get_xml_doctype('foo', 'SYSTEM', 'test.dtd') + '<foo><bar /></foo>'
        doc_2 = get_xml_declaration('1.0', 'utf-16') + (get_xml_doctype('foo', 'SYSTEM', 'test.dtd') + '<foo><bar /></foo>').encode('utf-16')
        f1 = file_obj_from_string(doc_1)
        f2 = file_obj_from_string(doc_2)
        self.assertRaises(Exception, xml_compare.compare_files, (f1, f2))

    def test_doctype_system_url_mismatch(self):
        # Basic document
        doc_1 = get_xml_declaration('1.0', 'utf-8') + get_xml_doctype('foo', 'SYSTEM', 'test1.dtd') + '<foo><bar /></foo>'
        doc_2 = get_xml_declaration('1.0', 'utf-8') + get_xml_doctype('foo', 'SYSTEM', 'test2.dtd') + '<foo><bar /></foo>'
        f1 = file_obj_from_string(doc_1)
        f2 = file_obj_from_string(doc_2)
        self.assertRaises(Exception, xml_compare.compare_files, (f1, f2))

    def test_doctype_root_tag_mismatch(self):
        # Basic document
        doc_1 = get_xml_declaration('1.0', 'utf-8') + get_xml_doctype('foo', 'SYSTEM', 'test.dtd') + '<foo><bar /></foo>'
        doc_2 = get_xml_declaration('1.0', 'utf-8') + get_xml_doctype('baz', 'SYSTEM', 'test.dtd') + '<baz><bar /></baz>'
        f1 = file_obj_from_string(doc_1)
        f2 = file_obj_from_string(doc_2)
        self.assertRaises(Exception, xml_compare.compare_files, (f1, f2))
        
    def test_successful_comapre_with_param(self):
        # Basic document
        doc_1 = get_xml_declaration('1.0', 'utf-8') + get_xml_doctype('foo', 'SYSTEM', 'test.dtd') + '<foo a="1" b="c"><bar /></foo>'
        doc_2 = get_xml_declaration('1.0', 'utf-8') + get_xml_doctype('foo', 'SYSTEM', 'test.dtd') + '<foo a="1" b="c"><bar /></foo>'
        f1 = file_obj_from_string(doc_1)
        f2 = file_obj_from_string(doc_2)
        self.assertIsNone(xml_compare.compare_files(f1, f2))

    def test_param_mismatch(self):
        # Basic document
        doc_1 = get_xml_declaration('1.0', 'utf-8') + get_xml_doctype('foo', 'SYSTEM', 'test.dtd') + '<foo a="1"><bar /></foo>'
        doc_2 = get_xml_declaration('1.0', 'utf-8') + get_xml_doctype('foo', 'SYSTEM', 'test.dtd') + '<foo b="c"><bar /></foo>'
        f1 = file_obj_from_string(doc_1)
        f2 = file_obj_from_string(doc_2)
        self.assertRaises(Exception, xml_compare.compare_files, (f1, f2))

    def test_child_num_mismatch(self):
        # Basic document
        doc_1 = get_xml_declaration('1.0', 'utf-8') + get_xml_doctype('foo', 'SYSTEM', 'test.dtd') + '<foo><bar /></foo>'
        doc_2 = get_xml_declaration('1.0', 'utf-8') + get_xml_doctype('foo', 'SYSTEM', 'test.dtd') + '<foo><bar /><bar /></foo>'
        f1 = file_obj_from_string(doc_1)
        f2 = file_obj_from_string(doc_2)
        self.assertRaises(Exception, xml_compare.compare_files, (f1, f2))
        
    def test_child_tag_mismatch(self):
        # Basic document
        doc_1 = get_xml_declaration('1.0', 'utf-8') + get_xml_doctype('foo', 'SYSTEM', 'test.dtd') + '<foo><bar /><car /></foo>'
        doc_2 = get_xml_declaration('1.0', 'utf-8') + get_xml_doctype('foo', 'SYSTEM', 'test.dtd') + '<foo><bar /><bar /></foo>'
        f1 = file_obj_from_string(doc_1)
        f2 = file_obj_from_string(doc_2)
        self.assertRaises(Exception, xml_compare.compare_files, (f1, f2))
        
    def test_text_compare(self):
        # Basic document
        doc_1 = get_xml_declaration('1.0', 'utf-8') + get_xml_doctype('foo', 'SYSTEM', 'test.dtd') + '<foo>bar</foo>'
        doc_2 = get_xml_declaration('1.0', 'utf-8') + get_xml_doctype('foo', 'SYSTEM', 'test.dtd') + '<foo>bar</foo>'
        f1 = file_obj_from_string(doc_1)
        f2 = file_obj_from_string(doc_2)
        self.assertIsNone(xml_compare.compare_files(f1, f2))
        
    def test_text_compare_with_whitespace(self):
        """
        Ensure that whitespace is ignored if ignore_whitespace is set to True.
        """
        # Basic document
        doc_1 = get_xml_declaration('1.0', 'utf-8') + get_xml_doctype('foo', 'SYSTEM', 'test.dtd') + '<foo>bar</foo>'
        doc_2 = get_xml_declaration('1.0', 'utf-8') + get_xml_doctype('foo', 'SYSTEM', 'test.dtd') + """<foo>
        
bar

</foo>"""
        f1 = file_obj_from_string(doc_1)
        f2 = file_obj_from_string(doc_2)
        self.assertIsNone(xml_compare.compare_files(f1, f2))
        
    def test_text_no_ignore_whitespace(self):
        """
        Ensure that whitespace is not ignored if ignore_whitespace is set to false.
        """
        
        # Basic document
        doc_1 = get_xml_declaration('1.0', 'utf-8') + get_xml_doctype('foo', 'SYSTEM', 'test.dtd') + '<foo>bar</foo>'
        doc_2 = get_xml_declaration('1.0', 'utf-8') + get_xml_doctype('foo', 'SYSTEM', 'test.dtd') + """<foo>
        
bar

</foo>"""
        f1 = file_obj_from_string(doc_1)
        f2 = file_obj_from_string(doc_2)
        with self.assertRaises(Exception):
            xml_compare.compare_files(f1, f2, ignore_whitespace = False)

    def test_ignore_empty(self):
        """
        Ensure that empty tags are ignored if ignore_empty_tags is set to True.
        
        """
        doc_1 = get_xml_declaration('1.0', 'utf-8') + get_xml_doctype('foo', 'SYSTEM', 'test.dtd') + '<foo></foo>'
        doc_2 = get_xml_declaration('1.0', 'utf-8') + get_xml_doctype('foo', 'SYSTEM', 'test.dtd') + '<foo><bar /></foo>'
        f1 = file_obj_from_string(doc_1)
        f2 = file_obj_from_string(doc_2)
        self.assertIsNone(xml_compare.compare_files(f1, f2))
               
    def test_no_ignore_empty(self):
        """
        Ensure that empty tags are not ignored if ignore_empty_tags is set to False.
        """
        doc_1 = get_xml_declaration('1.0', 'utf-8') + get_xml_doctype('foo', 'SYSTEM', 'test.dtd') + '<foo></foo>'
        doc_2 = get_xml_declaration('1.0', 'utf-8') + get_xml_doctype('foo', 'SYSTEM', 'test.dtd') + '<foo><bar /></foo>'
        f1 = file_obj_from_string(doc_1)
        f2 = file_obj_from_string(doc_2)
        with self.assertRaises(Exception):
            xml_compare.compare_files(f1, f2, ignore_empty_tags = False)
            
    def test_custom_compare_function(self):
        def lower_case_compare(s1, s2):
            return s1.lower() == s2.lower()
    
        doc_1 = get_xml_declaration('1.0', 'utf-8') + get_xml_doctype('foo', 'SYSTEM', 'test.dtd') + '<foo a="HeLlO"></foo>'
        doc_2 = get_xml_declaration('1.0', 'utf-8') + get_xml_doctype('foo', 'SYSTEM', 'test.dtd') + '<foo a="hElLo"></foo>'
        f1 = file_obj_from_string(doc_1)
        f2 = file_obj_from_string(doc_2)
        
        with self.assertRaises(Exception):
            # Compare using the default compare function, which should fail
            xml_compare.compare_files(f1, f2)
    
        # Compare using the custom, lower-case compare function
        self.assertIsNone(xml_compare.compare_files(f1, f2, compare_function = lower_case_compare))
        