#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/11/6


"""
# 推荐-Yes
# 方式一：与起始变量对齐
foo = long_function_name(var_one, var_two,
                         var_three, var_four)

# 方式二：字典中与起始值对齐
foo = {
    long_dictionary_key: value1 +
                         value2,
    ...
}

# 方式三：4个空格缩进，第一行不需要
foo = long_function_name(
    var_one, var_two, var_three,
    var_four)

# 方式四：字典中4个空格缩进
foo = {
    long_dictionary_key:
        long_dictionary_value,
    ...
}


# 不推荐-No
# 第一行有空格是禁止的
foo = long_function_name(var_one, var_two,
    var_three, var_four)

# 2个空格是禁止的
foo = long_function_name(
  var_one, var_two, var_three,
  var_four)

# 字典中没有处理缩进



# 空格

# 推荐-Yes
spam(ham[1], {eggs: 2}, [])

# 不推荐-No
spam( ham[ 1 ], { eggs: 2 }, [ ] )




# 推荐-Yes
if x == 4:
    print(x, y)
    x, y = y, x

# 不推荐-No
if x == 4 :
    print(x , y)
    x , y = y , x




# 推荐-Yes
spam(1)
dict['key'] = list[index]

# 不推荐-No
spam (1)
dict ['key'] = list [index]


# 推荐-Yes
def complex(real, imag=0.0):
    return magic(r=real, i=imag)
# 不推荐-No
def complex(real, imag = 0.0):
    return magic(r = real, i = imag)

# 推荐-Yes
foo = 1000  # 注释
long_name = 2  # 注释不需要对齐
dictionary = {
    "foo": 1,
    "long_name": 2,
}

# 不推荐-No
foo       = 1000  # 注释
long_name = 2  # 注释不需要对齐
dictionary = {
    "foo": 1,
    "long_name": 2,
}
"""

# 推荐-Yes
def main():
    ...


if __name__ == '__main__':
    main()

"""
print('this is draft222222222222 .py')

if __name__ == '__main__':
    print('this is draft.py: main11111111111111')



# 推荐-Yes
foo_bar(self, width, height, color='black', design=None, x='foo',
        emphasis=None, highlight=0)

if (width == 0 and height == 0 and
    color == 'red' and emphasis == 'strong'):

x = ('这是一个非常长非常长非常长非常长 '
     '非常长非常长非常长非常长非常长非常长的字符串')

# 不推荐-No



# 推荐-Yes
if foo:
    bar()

while x:
    x = bar()

if x and y:
    bar()

if not x:
    bar()
return foo

for (x, y) in dict.items(): ...


# 不推荐-No
if (x):
    bar()

if not(x):
    bar()
return (foo)


class ParentClass(object):
    pass


# 推荐-Yes
class SampleClass(object):
    pass

class OuterClass(object):
    class InnerClass(object):
        pass

# 不推荐-No
class SampleClass:
    pass

class OuterClass:
    class InnerClass:
        pass

a, b, imperative, expletive, name, n = 0

# 推荐-Yes
with open("hello.txt") as hello_file:
    for line in hello_file:
        print(line)




# 不推荐-No
x = '%s%s' % (imperative, expletive)
x = '{}{}'.format(imperative, expletive)
x = imperative + ', ' + expletive + '!'
x = 'name: ' + name + '; score: ' + str(n)


# 推荐-Yes
# TODO(zk@wwl.com): Use a "*" here for string repetition.
# TODO(Zach) Change this to use relations.

# 不推荐-No
"""

# 推荐-Yes
import os
import sys

# 不推荐-No
# import os, sys
"""
users,i=0

# 推荐-Yes
if not users:
    print('no users')

if foo == 0:
    self.handle_zero()

if i % 10 == 0:
    self.handle_multiple_of_ten()

def f(x=None):
    if x is None:
        x = []

# 不推荐-No
if len(users) == 0:
    print('no users')

if foo is not None and not foo:
    self.handle_zero()

if not i % 10:
    self.handle_multiple_of_ten()

def f(x=None):
    x = x or []
"""

# 推荐-Yes
# 不推荐-No


# 推荐-Yes
# 不推荐-No



# 推荐-Yes
# 不推荐-No


"""
#Import Library
from sklearn.ensemble import GradientBoostingClassifier
#Assumed you have, X (predictor) and Y (target) for training data set and x_test(predictor) of test_dataset
# Create Gradient Boosting Classifier object
model= GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0)
# Train the model using the training sets and check score
model.fit(X, y)
#Predict Output
predicted= model.predict(x_test)
"""













