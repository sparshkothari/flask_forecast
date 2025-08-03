# template.py
import numpy as np
from models import ModelRequestObj


class TemplateDefaultValues:

    def __init__(self):
        self.lineSeriesValueX = "x"


class GenerateArray:

    def __init__(self, q: ModelRequestObj):
        self.array = []
        pass


class ChartVariables:

    def __init__(self):
        self.title = ""
        self.lineSeriesValueX = TemplateDefaultValues().lineSeriesValueX
        self.xAxisTitleText = self.lineSeriesValueX
        self.yAxisTitleText = ""


class Template:

    def __init__(self, q: ModelRequestObj):
        self.model = self.__class__.__name__
        self.title = self.model
        self.lineSeriesValueX = TemplateDefaultValues().lineSeriesValueX
        self.lineSeriesValueY = "y_" + self.model
        self.lineSeriesName = self.lineSeriesValueY

        self.index_start = q.index_start
        self.index_stop = q.index_stop
        self.increment = q.increment

        self.data_point = 0.0
        self.data = []

    def simulate_model(self):
        for i in np.arange(self.index_start, self.index_stop + 1, self.increment):
            self.iterate(i)
            data_item = {self.lineSeriesValueX: i, self.lineSeriesValueY: self.data_point}
            self.data.append(data_item)

    def iterate(self, index):
        pass
