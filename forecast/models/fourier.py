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

        if q.base_model == 2:
            q.index_stop = 10.0
            self.array.append(FourierSquareWave3(q))
            self.array.append(FourierTriangleWave3(q))
        elif q.base_model == 3:
            q.index_stop = 10.0
            self.array.append(FourierSquareWave1(q))
            self.array.append(FourierSquareWave2(q))
            self.array.append(FourierSquareWave3(q))
        elif q.base_model == 4:
            q.index_stop = 5.0
            self.array.append(FourierTriangleWave1(q))
            self.array.append(FourierTriangleWave2(q))
            self.array.append(FourierTriangleWave3(q))


class FourierChartVariables(ChartVariables):

    def __init__(self):
        super().__init__()
        self.title += "Fourier Series"
        self.xAxisTitleText = UnitsLabel.time_nano_seconds
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


class FourierSquareWave1(Fourier):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.wave = SquareWave()

        t = UtilsJSONEncoder()
        t.encode(self.wave)

        self.wave.populate(3)


class FourierSquareWave2(Fourier):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.wave = SquareWave()

        t = UtilsJSONEncoder()
        t.encode(self.wave)

        self.wave.populate(5)


class FourierSquareWave3(Fourier):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.wave = SquareWave()

        t = UtilsJSONEncoder()
        t.encode(self.wave)

        self.wave.populate(20)


class FourierTriangleWave1(Fourier):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.wave = TriangleWave()

        t = UtilsJSONEncoder()
        t.encode(self.wave)

        self.wave.populate(2)


class FourierTriangleWave2(Fourier):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.wave = TriangleWave()

        t = UtilsJSONEncoder()
        t.encode(self.wave)

        self.wave.populate(3)


class FourierTriangleWave3(Fourier):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.wave = TriangleWave()

        t = UtilsJSONEncoder()
        t.encode(self.wave)

        self.wave.populate(10)


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

    def method_impl(self, i: float = 0.0, time: float = 0.0):
        super().method_impl(i, time)
        t = time
        h = (2.0 * i) - 1.0
        h1 = 2.0 / (h * math.pi)
        return h1 * math.sin(h * t)


class TriangleWave(Wave):

    def __init__(self, n_sum_limit: int = 0):
        super().__init__(n_sum_limit)
        self.a_initial = 0.5

    def method_impl(self, i: float = 0.0, time: float = 0.0):
        super().method_impl(i, time)
        t = time
        h = (2.0 * i) - 1.0
        h1 = 4.0 / math.pow(h * math.pi, 2)
        return h1 * math.cos(h * math.pi * t) * -1.0
