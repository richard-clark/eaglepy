"""
File Compare Test
=================

Verifies the integrity of Eagle-Python by parsing and then serializing files, and comparing
the input and output files to ensure they are identical (that no information was lost or
gained).

"""

from eaglepy.eagle import Eagle
import os
import shutil
import xml_compare

def parse_rot_str(rot_str):
    """
    Attempt to extract an EAGLE rotation value from the string.
    
    :param rot_str: The string to parse.
    
    :returns: If the string is a valid rotation string, returns (mirrored, spin, angle); otherwise, returns None.
    
    """
    
    m = False
    r = False
    s = False
    
    val = None
    
    for i in range(len(rot_str)):
        if rot_str[i] == 'M':
            m = True
        elif rot_str[i] == 'R':
            r = True
        elif rot_str[i] == 'S':
            s = True
        else:
            val_str = rot_str[i:]
            try:
                val = float(val_str)
                
                if r:
                    return (m, s, val)
                else:
                    return None
                
            except:
                return None
    
    return None

def compare_rot(v1, v2):
    """
    Compare two potential rotation strings. 
    
    :param v1: The first string to compare. 
    :param v2: The second string to compare.
    
    :returns: True if both strings are rotation strings and are equal; otherwise False.
    
    """
    
    rs1 = parse_rot_str(v1)
    rs2 = parse_rot_str(v2)
    
    return rs1 != None and rs2 != None and rs1 == rs2
    
def compare_function(v1, v2):
    """
    Compare two XML attribute value strings.
    
    Attempts to compare as strings, floating-point values, and roations. 
    
    :param v1: The first string to compare.
    :param v2: The second string to compare.
    
    :returns: Whether the strings are equal.
    
    """
    
    # Attempt to compare as string
    if v1 == v2:
        return True 
     
    # Attempt to compare as float
    try:
        f1 = float(v1)
        f2 = float(v2)
        
        # Values parsed successfully 
        return f1 == f2
    except:
        pass
     
    # Attempt to compare as rotations
    return compare_rot(v1, v2)


def test_files(input_file_path, output_file_path, working_file_path_no_ext):
    """
    Test all of the EAGLE files (sch, brd, and lbr) in a dictory by parsing each file, 
    writing the parsed data to another file (the working file), and ensuring that the 
    input and output files are identical.

    :param input_file_path: The directory from which to read input files. 
    :param output_file_path: The directory to which to move files which have been successfully parsed, or ``None``.
    :param working_file_path_no_ext: The file name (without extension) to use to store the output file.    
    """

    # Make the output file path if it doesn't exist
    if not os.path.isdir(output_file_path):
        os.makedirs(output_file_path)

    # Iterate over all of the input files
    for f in os.listdir(input_file_path):
    
        input_file_name = input_file_path + os.sep + f
        ext = os.path.splitext(f)[1]
         
        if ext != '.sch' and ext != '.brd' and ext != '.lbr':
            continue
        
        working_file_name = working_file_path_no_ext + ext
        
        print('Parsing {0}...'.format(f))
        e = Eagle.load(input_file_name)
        print('Saving...')
        e.save(working_file_name)
        print('Testing...')
        xml_compare.compare_files(input_file_name, working_file_name, compare_function)
        
        if output_file_path != None:
            output_file_name = output_file_path + os.sep + f
            shutil.move(input_file_name, output_file_name)
    
if __name__ == '__main__':
#     INPUT_FILE_PATH = '/Users/richardclark/Testing/eagle_examples'
#     OUTPUT_FILE_PATH = '/Users/richardclark/Testing/eagle_examples_passed'
    
    INPUT_FILE_PATH = '/Users/richardclark/Testing/sf_eagle_files'
    OUTPUT_FILE_PATH = '/Users/richardclark/Testing/sf_eagle_files_passed'

#     INPUT_FILE_PATH = '/Users/richardclark/Testing/libs'
#     OUTPUT_FILE_PATH = '/Users/richardclark/Testing/libs_passed'

    WORKING_FILE_PATH_NO_EXT = '/Users/richardclark/Testing/eagle_testing'
    
    test_files(INPUT_FILE_PATH, OUTPUT_FILE_PATH, WORKING_FILE_PATH_NO_EXT)