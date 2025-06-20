
def NOT(func):
    def f(x):
        return not func(x)
    return f

def OR(func1, func2):
    def f(x):
        return func1(x) or func2(x)
    return f

def AND(func1, func2):
    def f(x):
        return func1(x) and func2(x)
    return f

def EQ(f_name, value):
    def f(x):
        return x[f_name] == value
    return f

def LESS_THAN(f_name, value):
    def f(x):
        return x[f_name] < value
    return f
