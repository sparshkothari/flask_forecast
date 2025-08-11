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


def sinc_f(x: float = 0.0):
    o = math.pi * x
    return math.sin(o) / o


class TrigT:

    def __init__(self,
                 amplitude: float = 0.0,
                 frequency: float = 0.0,
                 phase_shift: float = 0.0,
                 k_vertical_shift: float = 0.0):
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase_shift = phase_shift
        self.k_vertical_shift = k_vertical_shift

    def populate(self,
                 amplitude: float,
                 frequency: float,
                 phase_shift: float,
                 k_vertical_shift: float):
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase_shift = phase_shift
        self.k_vertical_shift = k_vertical_shift

    def method(self, x):
        pass


class TanF(TrigT):

    def method(self, x):
        super().method(x)
        return tan_f(self.amplitude, self.frequency, self.phase_shift, self.k_vertical_shift, x)


class CosineF(TrigT):

    def method(self, x):
        super().method(x)
        return cosine_f(self.amplitude, self.frequency, self.phase_shift, self.k_vertical_shift, x)


class SineF(TrigT):

    def method(self, x):
        super().method(x)
        return sine_f(self.amplitude, self.frequency, self.phase_shift, self.k_vertical_shift, x)


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


'''
Units (Label)
'''


class UnitsLabel:
    time_nano_seconds = "t (nanoseconds)"
    time_micro_seconds = "t (microseconds)"
    time_milli_seconds = "t (milliseconds)"
    time_seconds = "t (seconds)"
    time_minutes = "t (minutes)"
    time_hours = "t (hours)"
    time_days = "t (days)"
    time_weeks = "t (weeks)"
    time_months = "t (months)"
    time_years = "t (years)"

    people_thousands = "people (thousands)"

    milliliters = "milliliters (mL)"
    liters = "liters (L)"

    units = "units"

    frequency_hertz = "frequency (hertz)"


class Waveform:
    square = "square_wave"
    triangle = "triangle_wave"
    parabola = "parabola_wave"
    exponential = "exponential"
    cubic = "cubic"
    aperiodic_pulse = "aperiodic pulse"
    dirac_delta_rect = "dirac delta rectangular"
