#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/10/25

# li = ['qwe', 'ewqead', '151654']
# for n in li:
#     tid = (n and 'p' or 'f')
#     print('n = %s is %s' %(n, tid))
#
# n = True
# tid = (n and 'p' or 'f')
# print('n = %s is %s' %(n, tid))

name = 'hello'
value = '258'
HEADING_ATTRIBUTE_TMPL = """<p class='attribute'><strong>%(name)s:</strong> %(value)s</p>"""

temp = HEADING_ATTRIBUTE_TMPL % dict(value=value, name=name)

print('this is a test temp = ', temp)

test = [('Start Time', '2018-10-26 11:31:04'), ('Duration', '0:08:53.921090'), ('Status', 'Failure 2')]
print(type(test), type(test[0]))
for name, value in [test[0]]:

    daf = 123
    print(name, value)