# template.py
import math

from models import ModelRequestObj


class GenerateArray:

    def __init__(self):
        self.array = []
        pass


class ChartVariables:

    def __init__(self, q: ModelRequestObj):
        self.title = ""
        self.lineSeriesValueX = Template(q).lineSeriesValueX
        self.xAxisTitleText = self.lineSeriesValueX
        self.yAxisTitleText = ""


class Template:

    def __init__(self, q: ModelRequestObj):
        self.model = self.__class__.__name__
        self.title = self.model
        self.lineSeriesValueX = "value_x_"
        self.lineSeriesValueY = "value_y_" + self.model
        self.lineSeriesName = self.lineSeriesValueY
        self.timeframe = -1
        self.timeframe_increment = -1
        if q.timeframe_unit == 0:
            self.timeframe = int(q.timeframe_multiplier * 365)
            self.timeframe_increment = q.timeframe_increment_multiplier * 365
            self.lineSeriesValueX += "day"

        if q.timeframe_increment_multiplier == 0.0:
            self.timeframe_increment = 1.0

        self.index_start = 0
        self.data_point = 0.0
        self.data = []

    def simulate_model(self):
        for i in range(self.index_start, self.timeframe):
            self.iterate(i)
            if math.floor(i % self.timeframe_increment) == 0:
                data_item = {self.lineSeriesValueX: i, self.lineSeriesValueY: self.data_point}
                self.data.append(data_item)

    def iterate(self, index):
        pass
