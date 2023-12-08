# d.py
import utils
from forecast.models.template import Template, GenerateArray, \
    ChartVariables


class DArray(GenerateArray):

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        super().__init__(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier)
        self.array.append(D1(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier))


class DChartVariables(ChartVariables):

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        super().__init__(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier)
        self.title += "D"
        self.yAxisTitleText = "{placeholder}"


class D(Template):

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        super().__init__(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier)
        self.a = 0.0
        self.h = 0.0
        self.k = 0.0
        self.p = 0.0

    def iterate(self, index):
        self.data_point = utils.exp_f(self.a, self.h, self.k, self.p, index)


class D1(D):

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        super().__init__(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier)
        self.index_start = -1 * self.timeframe
        self.a = 1.0
        self.p = 3.0
