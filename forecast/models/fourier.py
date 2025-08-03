# fourier.py

import math
from utils import UtilsJSONEncoder, UnitsLabel
from forecast.models.template import Template, GenerateArray, \
    ChartVariables
from models import ModelRequestObj


class FourierArray(GenerateArray):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        q.index_start = 0.0
        q.index_stop = 50.0
        q.increment = 0.01
        self.array.append(Fourier1(q))
        self.array.append(Fourier2(q))
        self.array.append(Fourier3(q))


class FourierChartVariables(ChartVariables):

    def __init__(self):
        super().__init__()
        self.title += "Fourier Series"
        self.xAxisTitleText = UnitsLabel.time_months
        self.yAxisTitleText = UnitsLabel.units


class Fourier(Template):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.wave = Wave()

        t = UtilsJSONEncoder()
        t.encode(self.wave)

    def iterate(self, index):
        super().iterate(index)
        x = index
        self.data_point = self.wave.method(x)


class Fourier1(Fourier):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.wave = SquareWave()

        t = UtilsJSONEncoder()
        t.encode(self.wave)

        self.wave.populate(3)


class Fourier2(Fourier):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.wave = SquareWave()

        t = UtilsJSONEncoder()
        t.encode(self.wave)

        self.wave.populate(5)


class Fourier3(Fourier):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.wave = SquareWave()

        t = UtilsJSONEncoder()
        t.encode(self.wave)

        self.wave.populate(20)


class Wave:

    def __init__(self, n_sum_limit: int = 0):
        self.n_sum_limit = n_sum_limit
        self.a_initial = 0.0

    def populate(self, n_sum_limit: int = 0):
        self.n_sum_limit = n_sum_limit

    def method(self, time: float = 0.0):
        v = 0.0
        v += self.a_initial
        for i in range(1, self.n_sum_limit):
            v += self.method_impl(float(i), time)
        return v

    def method_impl(self, i: float = 0.0, time: float = 0.0):
        return time


class SquareWave(Wave):

    def __init__(self, n_sum_limit: int = 0):
        super().__init__(n_sum_limit)
        self.a_initial = 0.5

    def populate(self, n_sum_limit: int = 0):
        super().populate(n_sum_limit)

    def method_impl(self, i: float = 0.0, time: float = 0.0):
        super().method_impl(i, time)
        t = time
        h = (2 * i) - 1
        h1 = 2 / (h * math.pi)
        return h1 * math.sin(h * t)
