# template.py
import math


class GenerateArray:

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        self.array = []
        pass


class ChartVariables:

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        self.title = "Model: "
        self.lineSeriesValueX = Template(-1, timeframe_unit, -1).lineSeriesValueX
        self.xAxisTitleText = self.lineSeriesValueX
        self.yAxisTitleText = ""


class Template:

    def __init__(self, timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        self.base_model = ""
        self.model = self.__class__.__name__
        self.lineSeriesValueX = "value_x_"
        self.lineSeriesValueY = "value_y_" + self.model
        self.lineSeriesName = ""
        self.timeframe = -1
        self.timeframe_increment = -1
        if timeframe_unit == 0:
            self.timeframe = int(timeframe_multiplier * 365)
            self.timeframe_increment = timeframe_increment_multiplier * 365
            self.lineSeriesValueX += "day"

        if timeframe_increment_multiplier == 0.0:
            self.timeframe_increment = 1.0

        self.data_point = 0.0
        self.initial_data_point = 0.0
        self.final_differential = 0.0
        self.data = []

    def simulate_model(self):
        for i in range(0, self.timeframe):
            self.iterate(i)
            if math.floor(i % self.timeframe_increment) == 0:
                data_item = {self.lineSeriesValueX: i, self.lineSeriesValueY: self.data_point}
                self.data.append(data_item)
        self.final_differential = self.data_point - self.initial_data_point

    def iterate(self, index):
        pass
