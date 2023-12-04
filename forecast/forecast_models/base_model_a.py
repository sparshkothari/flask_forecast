# base_model_a.py
from random import Random

from forecast.forecast_models.forecast_model_template import ForecastModelTemplate, GenerateBaseModelArray, \
    BaseModelChartVariables


class GenerateBaseModelAArray(GenerateBaseModelArray):

    def __init__(self, forecast_timeframe: float):
        super().__init__(forecast_timeframe)
        self.array.append(ModelASustainable(forecast_timeframe))
        self.array.append(ModelANonSustainable(forecast_timeframe))


class BaseModelAChartVariables(BaseModelChartVariables):

    def __init__(self, forecast_timeframe: float):
        super().__init__(forecast_timeframe)
        self.title = "Model A"
        self.xAxisTitleText = "Day"
        self.yAxisTitleText = "Water (cubic inches)"
        self.forecast_timeframe = int(forecast_timeframe * 365)


class BaseModelA(ForecastModelTemplate):

    def __init__(self, forecast_timeframe: float):
        super().__init__(forecast_timeframe)
        self.forecast_base_model = "A"
        self.lineSeriesValueX = "day"
        self.forecast_timeframe = int(forecast_timeframe * 365)
        self.average_daily_water_consumption = 0.0
        self.daily_rainfall_probability = 0.0
        self.average_water_collection_per_rainfall = 0.0
        self.daily_water_import_probability = 0.0
        self.average_water_collection_per_import = 0.0
        self.daily_contamination_probability = 0.0
        self.average_percent_water_lost_during_contamination = 0.0

    def iterate(self):
        self.consume()
        self.rainfall()
        self.import_water()
        self.contaminate()

    def consume(self):
        self.current_water_reserves -= self.average_daily_water_consumption

    def rainfall(self):
        if Random().random() < self.daily_rainfall_probability:
            self.current_water_reserves += self.average_water_collection_per_rainfall

    def import_water(self):
        if Random().random() < self.daily_water_import_probability:
            self.current_water_reserves += self.average_water_collection_per_import

    def contaminate(self):
        if Random().random() < self.daily_contamination_probability:
            self.current_water_reserves -= (self.average_percent_water_lost_during_contamination *
                                            self.current_water_reserves)


class ModelASustainable(BaseModelA):

    def __init__(self, forecast_timeframe: float):
        super().__init__(forecast_timeframe)
        self.forecast_environment_number = 1
        self.forecast_environment = "sustainable"
        self.forecast_data_key += str(self.forecast_environment_number)
        self.lineSeriesValueY = self.forecast_data_key
        self.lineSeriesName = self.forecast_environment

        self.average_daily_water_consumption = 500.0
        self.daily_rainfall_probability = 0.2
        self.average_water_collection_per_rainfall = 10000.0
        self.daily_water_import_probability = 0.15
        self.average_water_collection_per_import = 1000.0
        self.daily_contamination_probability = 0.1
        self.average_percent_water_lost_during_contamination = 0.05


class ModelANonSustainable(BaseModelA):

    def __init__(self, forecast_timeframe: float):
        super().__init__(forecast_timeframe)
        self.forecast_environment_number = 2
        self.forecast_environment = "non-sustainable"
        self.forecast_data_key += str(self.forecast_environment_number)
        self.lineSeriesValueY = self.forecast_data_key
        self.lineSeriesName = self.forecast_environment

        self.average_daily_water_consumption = 500.0
        self.daily_rainfall_probability = 0.05
        self.average_water_collection_per_rainfall = 10000.0
        self.daily_water_import_probability = 0.1
        self.average_water_collection_per_import = 500.0
        self.daily_contamination_probability = 0.1
        self.average_percent_water_lost_during_contamination = 0.1
