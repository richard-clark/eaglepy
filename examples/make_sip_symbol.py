"""
Make SIP Symbol
================

The ``make_sip_symbol()`` method returns a ``Symbol`` with the specified name 
and number of pins. 

The symbol has name and value labels and an outline.

"""

from eaglepy import constants, eagle, primitives, primitive_utils

def make_sip_symbol(symbol_name, pins):
    
    # Constants
    spacing = constants.UNIT.to_default(0.1, constants.UNIT.INCH)
    wire_width = constants.UNIT.to_default(0.01, constants.UNIT.INCH)
    pin_rect_width = constants.UNIT.to_default(0.025, constants.UNIT.INCH)
    font_size = constants.UNIT.to_default(0.07, constants.UNIT.INCH)
    
    # Create the symbol
    s = eagle.Symbol(symbol_name)
    
    # Create a name label and add it above the symbol
    s.items.append(primitives.Text('>NAME', 
                                 spacing / 2.0, spacing, 
                                 constants.LAYERS.NAMES,
                                 size = font_size,
                                 align = constants.ALIGN.CENTER))

    # Create a value label and add it below the symbol
    s.items.append(primitives.Text('>VALUE', 
                                  spacing / 2.0, 
                                  -1 * pins * spacing, 
                                  constants.LAYERS.VALUES, 
                                  size = font_size, 
                                  align = constants.ALIGN.CENTER))   
    
    # Add the pins and pin rectangles
    for i in range(pins):
        y = -i * spacing
        name = str(i+1)
        
        s.items.append(primitives.Pin(name, 
                             -1 * spacing, 
                             y, 
                             visible = constants.PIN.VISIBLE.PAD, 
                             swap_level = 1,  
                             length = constants.PIN.LENGTH.SHORT))
            
        s.items.append(primitives.Rectangle(spacing/2.0 - pin_rect_width / 2.0, 
                                                  y - pin_rect_width / 2.0, 
                                                  spacing/2.0 + pin_rect_width / 2.0, 
                                                  y + pin_rect_width / 2.0, 
                                                  constants.LAYERS.SYMBOLS))
            
    # Add the symbol outline
    primitive_utils.add_wire_rect_tl(s.items, 
                                     0, 
                                     spacing/2.0, 
                                     spacing, 
                                     -1 * spacing * pins, 
                                     wire_width, 
                                     constants.LAYERS.SYMBOLS)
    
    return s
