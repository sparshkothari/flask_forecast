# forecast_utils.py
import math


def tan_f(a, f, p, x):
    return a * math.tan((f * x) + p)


def cosine_f(a, f, p, x):
    return a * math.cos((f * x) + p)


def sine_f(a, f, p, x):
    return a * math.sin((f * x) + p)
