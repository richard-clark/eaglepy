"""
Make SIP Header Library
=======================

Create a library containing SIP headers.

"""

from eaglepy import constants, default_layers, eagle
import make_sip_package, make_sip_symbol

# Constants
LIBRARY_NAME = 'Headers'
LIBRARY_PATH = 'headers.lbr'
MAX_NUM_PINS = 10
SPACING = constants.UNIT.to_default(0.1, constants.UNIT.INCH)
DRILL = constants.UNIT.to_default(0.04, constants.UNIT.INCH)
GATE_NAME = 'G$1'

# Create the library
lib = eagle.Library(LIBRARY_NAME)

for num_pins in range(1, MAX_NUM_PINS+1):
    # Create the package
    name = 'M{0}X1'.format(num_pins)
    
    package = make_sip_package.make_sip_package(name, 
                                                 num_pins, 
                                                 SPACING, 
                                                 DRILL)
    lib.packages.append(package)
    
    # Create the symbol
    symbol = make_sip_symbol.make_sip_symbol(name, num_pins)
    lib.symbols.append(symbol)
    
    # Create the device set
    device_set = eagle.Device_Set(name, 'J')
    device_set.gates.append(eagle.Gate(GATE_NAME, symbol, 0, 0))
    device = eagle.Device(name, package)
    for i in range(1,num_pins+1):
        c = eagle.Connect(GATE_NAME, str(i), str(i))
        device.connects.append(c)
    device_set.devices.append(device)
    lib.device_sets.append(device_set)
    
# Save the library
drawing = eagle.Drawing(grid = eagle.Grid(),
                        layers = default_layers.get_layers(),
                        document = lib)

e = eagle.Eagle(drawing)
e.save(LIBRARY_PATH)