# template.py
import numpy as np
from models import ModelRequestObj


class TemplateDefaultValues:
    lineSeriesValueX = "x"


class GenerateArray:

    def __init__(self, q: ModelRequestObj):
        self.array = []
        pass


class ChartVariables:

    def __init__(self):
        self.title = ""
        self.lineSeriesValueX = TemplateDefaultValues.lineSeriesValueX
        self.xAxisTitleText = ""
        self.yAxisTitleText = ""


class Template:

    def __init__(self, q: ModelRequestObj):
        self.model = self.__class__.__name__
        self.title = self.model
        self.xAxisTitleText = ""
        self.yAxisTitleText = ""
        self.lineSeriesValueX = TemplateDefaultValues.lineSeriesValueX
        self.lineSeriesValueY = "y_" + self.model
        self.lineSeriesName = self.lineSeriesValueY

        self.index_start = q.index_start
        self.index_stop = q.index_stop
        self.increment = q.increment

        self.data_point = 0.0
        self.data = []

    def simulate_model(self):
        index = 0
        for i in np.arange(self.index_start, self.index_stop, self.increment):
            self.iterate(index, i)
            data_item = {self.lineSeriesValueX: i, self.lineSeriesValueY: self.data_point}
            self.data.append(data_item)
            index += 1

    def iterate(self, index, i):
        pass
