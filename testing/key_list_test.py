from eaglepy import key_list
import unittest

class Test_Class():
    def __init__(self, name):
        self.name = name

class Testing(unittest.TestCase):
    
    def setUp(self):
        self.names = ['banana', 'apple', 'pear', 'orange']
        
        nd_list = []
        for n in self.names:
            nd_list.append(Test_Class(n))
            
        self.key_list = key_list.Key_List(nd_list)
        
    def test_append(self):
        new_item = Test_Class('pineapple')
        self.names.append(new_item.name)
        self.key_list.append(new_item)
        self.assertEqual(self.key_list.names(), self.names)
        
    def test_count(self):
        self.assertEqual(self.key_list.count(), len(self.names))
        self.assertEqual(len(self.key_list), len(self.names))
        
    def test_iter(self):
        i = iter(self.key_list)
        for n in self.names:
            self.assertEqual(i.next().name, n)
        
        with self.assertRaises(StopIteration):
            i.next()
                    
    def test_get_item(self):
        for n in self.names:
            self.assertIsNotNone(self.key_list[n])

  
    def test_clear(self):
        self.key_list.clear()
        self.assertEqual(self.key_list.count(),0)
        for n in self.names:
            self.assertFalse(self.key_list.has_name(n))
            
    def test_remove(self):
        objs = self.key_list.items()
        
        for i in range(len(objs)):
            obj = objs[i]
            self.key_list.remove(obj)
        
        self.assertEqual(len(self.key_list), 0)
        
    def test_pop(self):
        for n in self.names:
            f = self.key_list.pop(n)
            self.assertEqual(f.name, n)
            
        self.assertEqual(len(self.key_list), 0)
        
        
    def test_item_at_index(self):
        for i in range(len(self.names)):
            o = self.key_list.item_at_index(i)
            self.assertEqual(o.name, self.names[i])
        
def test_remove():
    nums = range(10)
    
    l = key_list.Key_List()
    
    for n in nums:
        l.append(Test_Class(n))
        
    for i in l:
        if i.name % 2 == 0:
            l.pop(i.name)
            
    for i in l:
        print(i.name)
    
if __name__ == '__main__':
    test_remove()
