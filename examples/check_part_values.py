"""
Check Part Values
=================

Check for parts which should have a value but don't. Print the name of the
offending part, or a success message if every part which should have a value
does have a value.

Replace the value of ``file_name`` with a board which actually exists.

"""


from eaglepy import eagle
    
file_name = 'eagle_unconnected_nets.sch'
    
e = eagle.Eagle.load(file_name)

schematic = e.drawing.document

parts_without_values = []

# Iterate over each part.
for p in schematic.parts:
    # Check whether the part shold have a value but doesn't.
    if p.device_set.user_value and p.value == None:
        parts_without_values.append(p)

# If all parts which should have values do have values, print a success message. 
# Otherwise, print the name of the parts without values. 
if len(parts_without_values) == 0:
    print('PASS: no parts without values')
else:
    print('Parts without values:')
    for p in parts_without_values:
        print(' - ' + p.name)