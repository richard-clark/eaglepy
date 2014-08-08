"""
Check Pin Count
===============

Determine the number of connections on each net in a schematic. 

Print those nets which have no connections, and those which
have one connection.

Replace the value of ``file_name`` with a board which actually exists.

"""
from eaglepy import eagle, primitives
    
file_name = 'schematic.sch'

e = eagle.Eagle.load(file_name)

schematic = e.drawing.document

# A dictionary--key is the net name, value is the pin count
nets = {}

# Iterate over each segment of each net on each sheet.
# For each Pin_Ref which the segment contains, update the pin count.
for s in schematic.sheets:
    for n in s.nets:
        if not nets.has_key(n.name):
            nets[n.name] = 0
            
        for seg in n.segments:
            for i in seg.items:
                if isinstance(i, primitives.Pin_Ref):
                    nets[n.name] += 1

keys = nets.keys()

nets_no_pins = []
nets_one_pin = []

# Iterate over all of the nets, and extract nets with no
# connections and with one connection.
for k in keys:
    if nets[k] == 0:
        nets_no_pins.append(k)
    elif nets[k] == 1:
        nets_one_pin.append(k)
  
# Determine if all nets have at least two connections.
# If so, print a message. 
if len(nets_no_pins) == 0 and len(nets_one_pin) == 0:
    print('PASS: all nets have at least two connections.')
    
# Print the nets with no connections
if len(nets_no_pins) > 0:
    print('No connections:')
    for n in nets_no_pins:
        print(' - ' + n)
    
# Print the nets with one connection
if len(nets_one_pin) > 0:
    print('One connection:')
    for n in nets_one_pin:
        print(' - ' + n)