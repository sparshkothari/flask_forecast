# utils.py
import math
from json import JSONEncoder

'''
json
'''


class UtilsJSONEncoder(JSONEncoder):

    def default(self, o):
        return o.__dict__


'''
Trigonometric Functions
'''


def tan_f(a, f, p, k, x):
    return a * math.tan(f * (x - p)) + k


def cosine_f(a, f, p, k, x):
    return a * math.cos(f * (x - p)) + k


def sine_f(a, f, p, k, x):
    return a * math.sin(f * (x - p)) + k


class TrigT:

    def __init__(self,
                 a: float = 0.0,
                 f: float = 0.0,
                 p: float = 0.0,
                 k: float = 0.0):
        self.a = a
        self.f = f
        self.p = p
        self.k = k

    def populate(self,
                 a: float,
                 f: float,
                 p: float,
                 k: float):
        self.a = a
        self.f = f
        self.p = p
        self.k = k

    def method(self, x):
        pass


class TanF(TrigT):

    def method(self, x):
        super().method(x)
        return tan_f(self.a, self.f, self.p, self.k, x)


class CosineF(TrigT):

    def method(self, x):
        super().method(x)
        return cosine_f(self.a, self.f, self.p, self.k, x)


class SineF(TrigT):

    def method(self, x):
        super().method(x)
        return sine_f(self.a, self.f, self.p, self.k, x)


'''
Exponential Functions
'''


def exp_f(a, h, k, p, x):
    return (a * math.pow(x - h, p)) + k


def exp2_f(c: [], x):
    n = len(c)
    p = 0
    f = 0
    while p < n:
        f = f + (c[p] * math.pow(x, p))
        p += 1
    return f


'''
Linear Functions
'''


def line_f(m, b, x):
    return (m * x) + b


class LineT:

    def __init__(self,
                 m: float = 0.0,
                 b: float = 0.0):
        self.m = m
        self.b = b

    def populate(self, m: float, b: float):
        self.m = m
        self.b = b

    def method(self, x):
        return line_f(self.m, self.b, x)
