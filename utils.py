# utils.py
import math

'''
Trigonometric Functions
'''


def tan_f(a, f, p, x):
    return a * math.tan((f * x) + p)


def cosine_f(a, f, p, x):
    return a * math.cos((f * x) + p)


def sine_f(a, f, p, x):
    return a * math.sin((f * x) + p)


'''
Exponential Functions
'''


def exp_f(a, h, k, p, x):
    return (a * math.pow(x-h, p)) + k


def exp2_f(c: [], x):
    n = len(c)
    p = 0
    f = 0
    while p < n:
        f = f + (c[p] * math.pow(x, p))
        p += 1
    return f


"""
Linear Functions
"""


def line_f(m: float, b: float, x: float):
    return (m * x) + b
