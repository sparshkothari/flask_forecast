# base_model_a.py
import math
from random import Random

from forecast.forecast_models.forecast_model_template import ForecastModelTemplate, GenerateBaseModelArray, \
    BaseModelChartVariables


class GenerateBaseModelCArray(GenerateBaseModelArray):

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        super().__init__(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier)
        self.array.append(C1(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier))
        self.array.append(C2(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier))
        # self.array.append(C3(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier))


class BaseModelCChartVariables(BaseModelChartVariables):

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        super().__init__(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier)
        self.title += "C"
        self.yAxisTitleText = "{placeholder}"


class BaseModelC(ForecastModelTemplate):

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        super().__init__(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier)
        self.base_model = "C"

        self.initial_data_point = math.pow(10, 5)
        self.data_point = self.initial_data_point

        self.amplitude = 5.0
        self.frequency = (2 * math.pi) / 365
        self.phase = 0.0

        self.cosine = False
        self.sine = False

    def iterate(self, index):
        if self.cosine and self.sine:
            self.tan_f(index)
        elif self.cosine:
            self.cosine_f(index)
        elif self.sine:
            self.sine_f(index)

    def tan_f(self, index):
        self.data_point = self.amplitude * math.tan((self.frequency * index) + self.phase)

    def cosine_f(self, index):
        self.data_point = self.amplitude * math.cos((self.frequency * index) + self.phase)

    def sine_f(self, index):
        self.data_point = self.amplitude * math.sin((self.frequency * index) + self.phase)


class C1(BaseModelC):

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        super().__init__(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier)

        self.lineSeriesName = "example—model-cosine " + self.__class__.__name__

        self.cosine = True
        self.sine = False


class C2(BaseModelC):

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        super().__init__(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier)

        self.lineSeriesName = "example—model-sine " + self.__class__.__name__

        self.cosine = False
        self.sine = True


class C3(BaseModelC):

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        super().__init__(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier)

        self.lineSeriesName = "example—model-tan " + self.__class__.__name__

        self.cosine = True
        self.sine = True
