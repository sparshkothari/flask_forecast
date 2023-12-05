# forecast_model_template.py


class GenerateBaseModelArray:

    def __init__(self, forecast_timeframe: float):
        self.array = []
        pass


class BaseModelChartVariables:

    def __init__(self, forecast_timeframe: float):
        self.title = "Model: "
        self.xAxisTitleText = ""
        self.yAxisTitleText = ""
        self.lineSeriesValueX = ""
        self.forecast_timeframe = ""


class ForecastModelTemplate:

    def __init__(self, forecast_timeframe: float):
        self.base_model = ""
        self.model = ""
        self.forecast_timeframe = -1
        self.lineSeriesValueX = "value_x_"
        self.lineSeriesValueY = "value_y_"
        self.lineSeriesName = ""
        self.data_point = 0.0
        self.data = []

    def simulate_model(self):
        for i in range(0, self.forecast_timeframe):
            self.iterate()
            data_item = {self.lineSeriesValueX: i, self.lineSeriesValueY: self.data_point}
            self.data.append(data_item)

    def iterate(self):
        pass
