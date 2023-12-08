# c.py
import math
import utils
from forecast.models.template import Template, GenerateArray, \
    ChartVariables
from models import ModelRequestObj


class CArray(GenerateArray):

    def __init__(self, q: ModelRequestObj):
        super().__init__()
        self.array.append(C1(q))


class CChartVariables(ChartVariables):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.title += "C"
        self.yAxisTitleText = "{placeholder}"


class C(Template):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.amplitude = 5.0
        self.frequency = (2 * math.pi) / 1000
        self.phase = 0.0


class C1(C):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.frequency_multiplier = 2.0
        self.multiplier_iterations = 4

    def iterate(self, index):
        super().iterate(index)
        self.data_point = self.method(self.amplitude, self.frequency, self.phase, index)

    def method(self, a, f, p, x):
        y = utils.sine_f(a, f, p, x)
        sine = False
        for i in range(0, self.multiplier_iterations):
            f = self.frequency_multiplier * f
            if sine:
                y = y * utils.sine_f(a, f, p, x)
                sine = False
            else:
                y = y * utils.cosine_f(a, f, p, x)
                sine = True
        return y
