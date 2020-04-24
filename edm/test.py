'''
@Description: 
@Author: FlyingRedPig
@Date: 2020-04-23 21:44:12
@LastEditors: FlyingRedPig
@LastEditTime: 2020-04-24 11:40:42
@FilePath: \EDM\edm\test.py
'''


def f(*args):
    return type(args)


def g(**kwargs):
    return type(kwargs)


def add(x):
    return x + 1


m = list(map(add, (1, 3, 4)))
print(m)
print(type(m))
