# base_model_a.py
from random import Random

from forecast.forecast_models.forecast_model_template import ForecastModelTemplate, GenerateBaseModelArray, \
    BaseModelChartVariables


class GenerateBaseModelAArray(GenerateBaseModelArray):

    def __init__(self, forecast_timeframe: float):
        super().__init__(forecast_timeframe)
        self.array.append(A1(forecast_timeframe))
        self.array.append(A2(forecast_timeframe))
        self.array.append(A3(forecast_timeframe))


class BaseModelAChartVariables(BaseModelChartVariables):

    def __init__(self, forecast_timeframe: float):
        super().__init__(forecast_timeframe)
        self.title += "A"
        self.xAxisTitleText = "Day"
        self.yAxisTitleText = "Water (cubic inches)"
        self.lineSeriesValueX = BaseModelA(-1.0).lineSeriesValueX
        self.axis_data_points = int(forecast_timeframe * 365)


class BaseModelA(ForecastModelTemplate):

    def __init__(self, forecast_timeframe: float):
        super().__init__(forecast_timeframe)
        self.base_model = "A"
        self.forecast_timeframe = int(forecast_timeframe * 365)
        self.lineSeriesValueX += "day"
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

    def __init__(self, forecast_timeframe: float):
        super().__init__(forecast_timeframe)
        self.model = self.__class__.__name__
        self.lineSeriesName = "highly sustainable"
        self.lineSeriesValueY += str(self.__class__.__name__)

        self.average_daily_water_consumption = 500.0
        self.daily_rainfall_probability = 0.2
        self.average_water_collection_per_rainfall = 10000.0
        self.daily_water_import_probability = 0.15
        self.average_water_collection_per_import = 1000.0
        self.daily_contamination_probability = 0.1
        self.average_percent_water_lost_during_contamination = 0.05


class A2(BaseModelA):

    def __init__(self, forecast_timeframe: float):
        super().__init__(forecast_timeframe)
        self.model = self.__class__.__name__
        self.lineSeriesName = "sustainable"
        self.lineSeriesValueY += str(self.__class__.__name__)

        self.average_daily_water_consumption = 500.0
        self.daily_rainfall_probability = 0.1
        self.average_water_collection_per_rainfall = 10000.0
        self.daily_water_import_probability = 0.1
        self.average_water_collection_per_import = 750.0
        self.daily_contamination_probability = 0.1
        self.average_percent_water_lost_during_contamination = 0.05


class A3(BaseModelA):

    def __init__(self, forecast_timeframe: float):
        super().__init__(forecast_timeframe)
        self.model = self.__class__.__name__
        self.lineSeriesName = "non-sustainable"
        self.lineSeriesValueY += str(self.__class__.__name__)

        self.average_daily_water_consumption = 500.0
        self.daily_rainfall_probability = 0.05
        self.average_water_collection_per_rainfall = 10000.0
        self.daily_water_import_probability = 0.1
        self.average_water_collection_per_import = 500.0
        self.daily_contamination_probability = 0.1
        self.average_percent_water_lost_during_contamination = 0.1
