def f(*args):
    return type(args)

def g(**kwargs):
    return type(kwargs)

print(g(a=7))