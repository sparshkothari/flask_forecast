# water.py
import utils
from utils import UtilsJSONEncoder, CosineF, SineF, LineT
from forecast.models.template import Template, GenerateArray, \
    ChartVariables
from models import ModelRequestObj


class WaterArray(GenerateArray):

    def __init__(self, q: ModelRequestObj):
        super().__init__()
        self.array.append(Water1(q))


class WaterChartVariables(ChartVariables):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.title += "Water"
        self.yAxisTitleText = "{placeholder}"


class Consume(LineT):
    pass


class Rain(CosineF):
    pass


class ImportW(SineF):
    pass


class Contaminate(SineF):
    pass


class Recycle:

    def __init__(self, c: float):
        self.c = c

    def method(self, x):
        return self.c * x


class Water(Template):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.consume = Consume(0.0, -.0)
        self.rain = Rain(1.0, 1.0, 1.0, 1.0)
        self.import_w = ImportW(1.0, 1.0, 1.0, 1.0)
        self.contaminate = Contaminate(1.0, 1.0, 1.0, -1.0)
        self.recycle = Recycle(0.2)

        t = UtilsJSONEncoder()
        t.encode(self.consume)
        t.encode(self.rain)
        t.encode(self.import_w)
        t.encode(self.contaminate)
        t.encode(self.recycle)

    def iterate(self, index):
        super().iterate(index)
        x = index
        self.data_point += (self.consume.method(x) +
                            self.rain.method(x) +
                            self.import_w.method(x) +
                            self.contaminate.method(x) +
                            self.recycle.method(self.consume.method(x)))


class Water1(Water):
    pass
