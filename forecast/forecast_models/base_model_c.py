# base_model_a.py
import math
import forecast_utils
from forecast.forecast_models.forecast_model_template import ForecastModelTemplate, GenerateBaseModelArray, \
    BaseModelChartVariables


class GenerateBaseModelCArray(GenerateBaseModelArray):

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        super().__init__(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier)
        self.array.append(C1(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier))


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


class C1(BaseModelC):

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        super().__init__(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier)

        self.multiplier = 2.0
        self.multiplier_iterations = 4

    def iterate(self, index):
        super().iterate(index)
        self.data_point = self.method(self.amplitude, self.frequency, self.phase, index)

    def method(self, a, f, p, x):
        m = self.multiplier
        m_i = self.multiplier_iterations
        y = forecast_utils.sine_f(a, f, p, x)
        sine = False
        for i in range(0, m_i):
            a = m * a
            f = m * f
            p = m * p
            if sine:
                y = y * forecast_utils.sine_f(a, f, p, x)
                sine = False
            else:
                y = y * forecast_utils.cosine_f(a, f, p, x)
                sine = True
        return y
