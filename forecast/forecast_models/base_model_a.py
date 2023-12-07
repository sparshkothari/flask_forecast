# base_model_a.py
import math
from random import Random

from forecast.forecast_models.forecast_model_template import ForecastModelTemplate, GenerateBaseModelArray, \
    BaseModelChartVariables


class GenerateBaseModelAArray(GenerateBaseModelArray):

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        super().__init__(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier)
        self.array.append(A1(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier))
        self.array.append(A2(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier))
        self.array.append(A3(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier))


class BaseModelAChartVariables(BaseModelChartVariables):

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        super().__init__(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier)
        self.title += "A"
        self.yAxisTitleText = "Water (cubic inches)"


class BaseModelA(ForecastModelTemplate):

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        super().__init__(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier)
        self.base_model = "A"

        self.initial_data_point = math.pow(10, 5)
        self.data_point = self.initial_data_point

        self.average_daily_water_consumption = 0.0

        self.daily_rainfall_probability = 0.0
        self.average_water_collection_per_rainfall = 0.0

        self.daily_water_import_probability = 0.0
        self.average_water_collection_per_import = 0.0

        self.daily_contamination_probability = 0.0
        self.average_percent_water_lost_during_contamination = 0.0

    def iterate(self, index):
        super().iterate(index)
        self.consume()
        self.rainfall()
        self.import_water()
        self.contaminate()

    def consume(self):
        self.data_point -= self.average_daily_water_consumption

    def rainfall(self):
        if Random().random() < self.daily_rainfall_probability:
            self.data_point += self.average_water_collection_per_rainfall

    def import_water(self):
        if Random().random() < self.daily_water_import_probability:
            self.data_point += self.average_water_collection_per_import

    def contaminate(self):
        if Random().random() < self.daily_contamination_probability:
            self.data_point -= (self.average_percent_water_lost_during_contamination *
                                self.data_point)


class A1(BaseModelA):

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        super().__init__(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier)

        self.lineSeriesName = "highly sustainable"

        self.average_daily_water_consumption = 500.0

        self.daily_rainfall_probability = 0.2
        self.average_water_collection_per_rainfall = 10000.0

        self.daily_water_import_probability = 0.15
        self.average_water_collection_per_import = 1000.0

        self.daily_contamination_probability = 0.1
        self.average_percent_water_lost_during_contamination = 0.05


class A2(BaseModelA):

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        super().__init__(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier)

        self.lineSeriesName = "sustainable"

        self.average_daily_water_consumption = 500.0
        self.daily_rainfall_probability = 0.1
        self.average_water_collection_per_rainfall = 10000.0
        self.daily_water_import_probability = 0.1
        self.average_water_collection_per_import = 750.0
        self.daily_contamination_probability = 0.1
        self.average_percent_water_lost_during_contamination = 0.05


class A3(BaseModelA):

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        super().__init__(timeframe_multiplier, timeframe_unit, timeframe_increment_multiplier)

        self.lineSeriesName = "non-sustainable"

        self.average_daily_water_consumption = 500.0
        self.daily_rainfall_probability = 0.05
        self.average_water_collection_per_rainfall = 10000.0
        self.daily_water_import_probability = 0.1
        self.average_water_collection_per_import = 500.0
        self.daily_contamination_probability = 0.1
        self.average_percent_water_lost_during_contamination = 0.1
