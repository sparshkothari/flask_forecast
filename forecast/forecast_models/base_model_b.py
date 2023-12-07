# base_model_a.py
import math
from random import Random

from forecast.forecast_models.forecast_model_template import ForecastModelTemplate, GenerateBaseModelArray, \
    BaseModelChartVariables


class GenerateBaseModelBArray(GenerateBaseModelArray):

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        super().__init__(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier)
        self.array.append(B1(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier))
        self.array.append(B2(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier))


class BaseModelBChartVariables(BaseModelChartVariables):

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        super().__init__(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier)
        self.title += "B"
        self.yAxisTitleText = "Population (# of people)"


class BaseModelB(ForecastModelTemplate):

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        super().__init__(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier)
        self.base_model = "B"

        self.initial_data_point = math.pow(10, 5)
        self.data_point = self.initial_data_point

        self.birth_rate_daily = 0.0
        self.death_rate_daily = 0.0

        self.small_calamity_probability = 0.0
        self.large_calamity_probability = 0.0

        self.percentage_population_lost_small_calamity = 0.0005
        self.percentage_population_lost_large_calamity = 0.001

    def iterate(self, index):
        super().iterate(index)
        self.birth()
        self.death()
        self.small_calamity()
        self.large_calamity()

    def birth(self):
        self.data_point += (self.birth_rate_daily *
                            self.data_point)

    def death(self):
        self.data_point -= (self.death_rate_daily *
                            self.data_point)

    def small_calamity(self):
        if Random().random() < self.small_calamity_probability:
            self.data_point -= (self.percentage_population_lost_small_calamity *
                                self.data_point)

    def large_calamity(self):
        if Random().random() < self.large_calamity_probability:
            self.data_point -= (self.percentage_population_lost_large_calamity *
                                self.data_point)


class B1(BaseModelB):

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        super().__init__(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier)

        self.lineSeriesName = "sustainable—model " + self.__class__.__name__

        self.birth_rate_daily = 0.0004
        self.death_rate_daily = 0.0004
        self.small_calamity_probability = 0.001
        self.large_calamity_probability = 0.0005


class B2(BaseModelB):

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        super().__init__(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier)

        self.lineSeriesName = "sustainable—model " + self.__class__.__name__

        self.birth_rate_daily = 0.000401
        self.death_rate_daily = 0.0004
        self.small_calamity_probability = 0.001
        self.large_calamity_probability = 0.0005
