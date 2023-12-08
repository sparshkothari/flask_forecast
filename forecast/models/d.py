# d.py
import utils
from forecast.models.template import Template, GenerateArray, \
    ChartVariables
from models import ModelRequestObj


class DArray(GenerateArray):

    def __init__(self, q: ModelRequestObj):
        super().__init__()
        self.array.append(D1(q))
        self.array.append(D2(q))


class DChartVariables(ChartVariables):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.title += "D"
        self.yAxisTitleText = "{placeholder}"


class D(Template):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.a = 0.0
        self.h = 0.0
        self.k = 0.0
        self.p = 0.0

    def iterate(self, index):
        super().iterate(index)
        self.data_point = utils.exp_f(self.a, self.h, self.k, self.p, index)


class D1(D):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.a = 1.0
        self.p = 3.0


class D2(D):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.a = 1.0
        self.h = 100.0
        self.p = 3.0
