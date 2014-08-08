"""
Print Library Contents
======================

Prints the name of every symbol, package, and device set in a specified EAGLE library. 

Replace the value of ``file_name`` with a library which actually exists.

"""

from eaglepy import eagle

file_name = 'library.lbr'

e = eagle.Eagle.load(file_name)

library = e.drawing.document

print('{0} symbols:'.format(len(library.symbols)))
for s in library.symbols:
    print(' --> {0}'.format(s.name))
print('')
    
print('{0} packages:'.format(len(library.packages)))
for p in library.packages:
    print(' --> {0}'.format(p.name))
print('')

print('{0} device sets:'.format(len(library.device_sets)))
for d in library.device_sets:
    print(' --> {0}'.format(d.name))