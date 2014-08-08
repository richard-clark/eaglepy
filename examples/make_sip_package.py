"""
Make SIP Package
================

The ``make_sip_package()`` method returns a ``Package`` with the specified name,
number of pins, pin spacing, and drill diameter.

The package has name and value labels and a silk-screen outline.

"""

from eaglepy import constants, eagle, primitives, primitive_utils

def make_sip_package(package_name, num_pins, spacing, drill):
    # Constants
    CHAMFER_RATIO = 0.029/0.1
    SILK_WIDTH = constants.UNIT.to_default(0.008, constants.UNIT.INCH)

    p = eagle.Package(package_name)

    # Add the name label
    name_label = primitives.Text('>NAME', 
                                 0, 
                                 spacing, 
                                 constants.LAYERS.TNAMES,
                                 align = constants.ALIGN.CENTER)
    p.items.append(name_label)

    # Add the value label
    value_label = primitives.Text('>VALUE', 
                                  0, 
                                  -1 * num_pins * spacing, 
                                  constants.LAYERS.TVALUES, 
                                  align = constants.ALIGN.CENTER)
    p.items.append(value_label)

    # Add the pads and silk
    for i in range(num_pins):
        # Add the pad
        x = 0
        y = -i * spacing
        
        pad = primitives.Pad(str(i+1), 
                             x, 
                             y, 
                             drill)
        if i == 0:
            p.shape = constants.SHAPE.SQUARE
        p.items.append(pad)
        
        # Add the silk
        primitive_utils.add_wire_rect_center(p.items, 
                                             x, 
                                             y, 
                                             spacing, 
                                             spacing, 
                                             SILK_WIDTH, 
                                             constants.LAYERS.TPLACE, 
                                             spacing * CHAMFER_RATIO)

    return p