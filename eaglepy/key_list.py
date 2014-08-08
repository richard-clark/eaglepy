import collections
import unittest

"""
Key_List
=========

This is a data structure which stores data in the order in which it was added (like a list),
but also provides access based on a key (like a dict). This functionality is implemented by
wrapping an instance of ``collections.OrderedDict``.

Every object added to the list must have a ``name`` varaible. This name variable is used as the key.
Thus, every object must have a unique name.

The data structure is designed to keep the keys transparant.

Because this class is a subclass of ``collections.OrderedDict``, this class does not have an
insert method.

Consider a ``Key_List`` instantiated as follows:

    nd = Key_List(obj(name = 'apple'), obj(name = 'pear'), obj(name = 'banana'))
    
Iteration is over the values, not the keys; that is,

    for n in nd:
        print(n)
        
results in the output:

    <__main__.obj instance at 0x101fd0cb0>
    <__main__.obj instance at 0x101fd0db0>
    <__main__.obj instance at 0x101fd0eb0>
    
They keys can be obtained using the ``iternames()`` method:

    for k in nd.iternames():
        print(k)
        
results in the output:

    apple
    pear
    banana

Items are added using the ``append()`` method:

    nd.append(obj(name = 'coconut'))
    
Items can be retrieved by name:

    o = nd['apple']
    
Or by index:

    o = nd.item_at_index(0)

"""

class Key_List():
    def __init__(self, items = None):
        self.list = collections.OrderedDict()
        if items != None:
            for i in items:
                self.append(i)

    def append(self, obj):
        """
        Add an object to the end of the list. 
        
        :param obj: The object to add.
        """
        self.list[obj.name] = obj
        
    def count(self):
        """
        Returns the number of items in the list. 
        
        :returns: The number of items in the list.
        """
        return len(self.list)
    
    def __iter__(self):
        """
        Returns an iterator for the list values.
        
        :returns: An iterator for the list values.
        """
        return self.list.itervalues()
        
    def clear(self):
        """
        Remove all items from the list.
        """
        self.list.clear()
    
    def __getitem__(self, i):
        """
        Returns the object with the specified key.
        
        :returns: The object with the specified key.
        """
        
        return self.list[i]

    def names(self):
        """
        Returns a list of the names of all objects in the list, in the order in which they were added.
        
        :returns: A list of the names of all objects in the list.
        """
        return self.list.keys()
    
    def items(self):
        """
        Returns a list of all items in the list. 
        
        :returns: A list of all items in the list.
        """
        
        return self.list.values()
    
    def iternames(self):
        """
        Returns an iterator for the object names. 
        
        :returns: An iterator for the object names.
        """
        
        return self.list.iterkeys()

    def pop(self, name):
        """
        Remove and return the object with the specified name.
        
        :param name: The name of the object to remove.
        
        :returns: The object with the specified name.
        """
        return self.list.pop(name)

    def remove(self, obj):
        """
        Remove the specified object.
        
        :param obj: The object to remove.
        
        """
        self.list.pop(obj.name)
    
    def __len__(self):
        """
        Returns the number of items in the list. 
        
        :returns: The number of items in the list.
        """
        
        return len(self.list)
        
    def has_name(self, name):
        """
        Returns a boolean value indicating whether an object with the
        specified name is contained within the list.
        
        :returns: Whether the list contains an object with the specified name. 
        """
        
        return self.list.has_key(name)
    
    def item_at_index(self, index):
        """
        Returns the list item at the specified index.
        
        :returns: The list item at the specified index. 
        """
        return self.list[self.list.keys()[index]]