# base_model_a.py
import math
import forecast_utils
from random import Random

from forecast.forecast_models.forecast_model_template import ForecastModelTemplate, GenerateBaseModelArray, \
    BaseModelChartVariables


class GenerateBaseModelCArray(GenerateBaseModelArray):

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        super().__init__(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier)
        self.array.append(C1(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier))
        self.array.append(C2(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier))
        self.array.append(C3(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier))
        self.array.append(C4(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier))


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
        self.custom = False

    def iterate(self, index):
        super().iterate(index)
        if self.cosine and self.sine:
            self.data_point = forecast_utils.tan_f(self.amplitude, self.frequency, self.phase, index)
        elif self.cosine:
            self.data_point = forecast_utils.cosine_f(self.amplitude, self.frequency, self.phase, index)
        elif self.sine:
            self.data_point = forecast_utils.sine_f(self.amplitude, self.frequency, self.phase, index)
        elif self.custom:
            self.data_point = self.custom_f(self.amplitude, self.frequency, self.phase, index)

    def custom_f(self, a, f, p, x):
        pass


class C1(BaseModelC):

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        super().__init__(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier)

        self.lineSeriesName = "example—model-cosine " + self.__class__.__name__
        self.cosine = True


class C2(BaseModelC):

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        super().__init__(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier)

        self.lineSeriesName = "example—model-sine " + self.__class__.__name__
        self.sine = True


class C3(BaseModelC):

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        super().__init__(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier)

        self.lineSeriesName = "example—model-custom " + self.__class__.__name__
        self.custom = True
        self.multiplier = 0.5

    def custom_f(self, a, f, p, x):
        super().custom_f(a, f, p, x)
        y = forecast_utils.sine_f(a, f, p, x)
        m = self.multiplier
        y = y * forecast_utils.cosine_f(m * a, m * f, m * p, m * x)
        return y


class C4(C3):

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        super().__init__(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier)
        self.multiplier = 2
