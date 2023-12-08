# e.py
import utils
from forecast.models.template import Template, GenerateArray, \
    ChartVariables
from models import ModelRequestObj


class EArray(GenerateArray):

    def __init__(self, q: ModelRequestObj):
        super().__init__()
        self.array.append(E1(q))
        self.array.append(E2(q))


class EChartVariables(ChartVariables):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.title += "E"
        self.yAxisTitleText = "{placeholder}"


class E(Template):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.m = 0.0
        self.b = 0.0

    def iterate(self, index):
        super().iterate(index)
        self.data_point = utils.line_f(self.m, self.b, index)


class E1(E):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.m = 3.0


class E2(E):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.m = -3.0

