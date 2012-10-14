Python 2.7.3 (default, Aug  1 2012, 05:14:39) 
[GCC 4.6.3] on linux2
Type "copyright", "credits" or "license()" for more information.
>>> list1 = [('y', 3), ('b', 4)]
>>> list2 = [('y', 3), ('c', 4)]
>>> list1 = dict([('y', 3), ('b', 4)])
>>> list3 = dict([(x[0], list1[x[0]]+x[1]) if x[0] in list1 else (x[0], x[1]) for x in list2])
>>> 
>>> list3
{'y': 6, 'c': 4}
>>> list3 = [(x[0], list1[x[0]]+x[1]) if x[0] in list1 else (x[0], x[1]) for x in list2]
>>> list4 = [(x[0], x[1]) if x not in list2 for x in list1]
SyntaxError: invalid syntax
>>> list4 = [x if x not in list2 for x in list1]
SyntaxError: invalid syntax
>>> list4 = [x for x in list1 if x not in list2]
>>> list4
['y', 'b']
>>> list4 = [(x, list1[x]) for x in list1 if x not in list2]
>>> list4
[('y', 3), ('b', 4)]
>>> list2 = [('c',4), ('y', 3), ]
>>> list2
[('c', 4), ('y', 3)]
>>> sorted(list2)
[('c', 4), ('y', 3)]
>>> li = set(list2)
>>> li
set([('y', 3), ('c', 4)])
>>> dir(li)
['__and__', '__class__', '__cmp__', '__contains__', '__delattr__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__iand__', '__init__', '__ior__', '__isub__', '__iter__', '__ixor__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__or__', '__rand__', '__reduce__', '__reduce_ex__', '__repr__', '__ror__', '__rsub__', '__rxor__', '__setattr__', '__sizeof__', '__str__', '__sub__', '__subclasshook__', '__xor__', 'add', 'clear', 'copy', 'difference', 'difference_update', 'discard', 'intersection', 'intersection_update', 'isdisjoint', 'issubset', 'issuperset', 'pop', 'remove', 'symmetric_difference', 'symmetric_difference_update', 'union', 'update']
>>> li2 = set(list4)
>>> li.intersection(li2)
set([('y', 3)])
>>> li.difference(li2)
set([('c', 4)])
>>> list(li.difference(li2))
[('c', 4)]
>>> list4
[('y', 3), ('b', 4)]
>>> list2
[('c', 4), ('y', 3)]
>>> li.union(li2)
set([('y', 3), ('b', 4), ('c', 4)])
>>> list1
{'y': 3, 'b': 4}
>>> 
>>> '''Using sets can prove very useful for combining lists in a way that makes sure we do not have duplicates. '''
'Using sets can prove very useful for combining lists in a way that makes sure we do not have duplicates. '
>>> 
