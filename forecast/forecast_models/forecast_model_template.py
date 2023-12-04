# forecast_model_template.py


class GenerateBaseModelArray:

    def __init__(self, forecast_timeframe: float):
        self.array = []
        pass


class BaseModelChartVariables:

    def __init__(self, forecast_timeframe: float):
        self.title = ""
        self.xAxisTitleText = ""
        self.yAxisTitleText = ""
        self.forecast_timeframe = ""


class ForecastModelTemplate:

    def __init__(self, forecast_timeframe: float):
        self.forecast_base_model = ""
        self.forecast_environment_number = ""
        self.forecast_environment = ""
        self.forecast_timeframe = -1
        self.lineSeriesValueX = ""
        self.lineSeriesValueY = ""
        self.lineSeriesName = ""
        self.current_water_reserves = 0.0
        self.data = []
        self.forecast_data_key = "water_reserves_"

    def simulate_model(self):
        for i in range(0, self.forecast_timeframe):
            self.iterate()
            data_item = {"day": i, self.lineSeriesValueY: self.current_water_reserves}
            self.data.append(data_item)

    def iterate(self):
        pass
