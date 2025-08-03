# taylor.py

import math
from utils import UtilsJSONEncoder, UnitsLabel
from forecast.models.template import Template, GenerateArray, \
    ChartVariables
from models import ModelRequestObj


class TaylorArray(GenerateArray):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        q.index_start = 0.0
        q.index_stop = 50.0
        q.increment = 0.01

        if q.base_model == 5:
            q.index_start = -10.1
            q.index_stop = 10.1
            self.array.append(SineRegular(q))
            self.array.append(MaclaurinSine1(q))
            self.array.append(MaclaurinSine2(q))
            self.array.append(MaclaurinSine3(q))


class TaylorChartVariables(ChartVariables):

    def __init__(self):
        super().__init__()
        self.title += "Taylor Series"
        self.xAxisTitleText = UnitsLabel.time_nano_seconds
        self.yAxisTitleText = UnitsLabel.units


class SineRegular(Template):
    def __init__(self, q: ModelRequestObj):
        super().__init__(q)

    def iterate(self, index):
        super().iterate(index)
        x = index
        self.data_point = math.sin(float(x))


class Taylor(Template):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.taylor_implementation = TaylorImplementation()

        t = UtilsJSONEncoder()
        t.encode(self.taylor_implementation)

    def iterate(self, index):
        super().iterate(index)
        x = index
        self.data_point = self.taylor_implementation.method(x)


class MaclaurinSine1(Taylor):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.taylor_implementation = MaclaurinSineImplementation()

        t = UtilsJSONEncoder()
        t.encode(self.taylor_implementation)

        self.taylor_implementation.populate(2)


class MaclaurinSine2(Taylor):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.taylor_implementation = MaclaurinSineImplementation()

        t = UtilsJSONEncoder()
        t.encode(self.taylor_implementation)

        self.taylor_implementation.populate(7)


class MaclaurinSine3(Taylor):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.taylor_implementation = MaclaurinSineImplementation()

        t = UtilsJSONEncoder()
        t.encode(self.taylor_implementation)

        self.taylor_implementation.populate(10)


class TaylorImplementation:

    def __init__(self, n_sum_limit: int = 0):
        self.n_sum_limit = n_sum_limit

    def populate(self, n_sum_limit: int = 0):
        self.n_sum_limit = n_sum_limit

    def method(self, x: float = 0.0):
        v = 0.0
        for i in range(0, self.n_sum_limit):
            v += self.method_impl(float(i), x)
        return v

    def method_impl(self, i: float = 0.0, x: float = 0.0):
        return x


class MaclaurinSineImplementation(TaylorImplementation):

    def __init__(self):
        super().__init__()

    def method(self, x: float = 0.0):
        v = super().method(x)
        v_limit = 1.01
        if abs(v) > v_limit:
            if v >= 0.0:
                return v_limit
            else:
                return -1.0 * v_limit
        else:
            return v

    def method_impl(self, i: float = 0.0, x: float = 0.0):
        super().method_impl(i, x)
        o = math.pow(-1.0, i)
        h = (2.0 * i) + 1.0
        g = o/math.factorial(h)
        return g * math.pow(x, h)

