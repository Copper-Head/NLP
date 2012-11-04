Python 2.7.3 (default, Aug  1 2012, 05:14:39) 
[GCC 4.6.3] on linux2
Type "copyright", "credits" or "license()" for more information.
>>> t = 'test'
>>> import re
>>> re
<module 're' from '/usr/lib/python2.7/re.pyc'>
>>> re.find

Traceback (most recent call last):
  File "<pyshell#3>", line 1, in <module>
    re.find
AttributeError: 'module' object has no attribute 'find'
>>> re.findall
<function findall at 0x7f814c3a2d70>
>>> t = '1st of october, second of november, april 4'
>>> t = '1st of october, first of november, april 1'
>>> t
'1st of october, first of november, april 1'
>>> reg = '1(?:st)?|first'
>>> re.findall(reg, t)
['1st', 'first', '1']
>>> t = t + '31st january'
>>> t
'1st of october, first of november, april 131st january'
>>> t = '1st of october, first of november, april 1, 31st january'
>>> re.findall(reg, t)
['1st', 'first', '1', '1st']
>>> reg = '\b1(?:st)?|first'
>>> re.findall(reg, t)
['first']
>>> reg = '[\b\^]1(?:st)?|first'
>>> re.findall(reg, t)
['first']
>>> reg = '\D1(?:st)?|first'
>>> re.findall(reg, t)
['first', ' 1']
>>> reg = '(?:\D|^)1(?:st)?|first'
>>> re.findall(reg, t)
['1st', 'first', ' 1']
>>> t = '1st of october, first of november, april 1, 31st january, twenty first may'
>>> re.findall(reg, t)
['1st', 'first', ' 1', 'first']
>>> reg = '(?:\D|^)1(?:st)?|(?<!twenty) first'
>>> re.findall(reg, t)
['1st', ' first', ' 1']
>>> t = '1st of october, first of november, april 1, 31st january, twenty first may, thirty first january'
>>> reg = '(?:\D|^)1(?:st)?|(?<!twenty|thirty) first'
>>> re.findall(reg, t)
['1st', ' first', ' 1']
>>> reg = '(?:\D|^)21(?:st)?|twenty first'
>>> re.findall(reg, t)
['twenty first']
>>> 
