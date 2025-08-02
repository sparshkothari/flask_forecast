# water.py
from utils import UtilsJSONEncoder, CosineF, SineF, LineT
from forecast.models.template import Template, GenerateArray, \
    ChartVariables
from models import ModelRequestObj


class WaterArray(GenerateArray):

    def __init__(self, q: ModelRequestObj):
        super().__init__()
        self.array.append(Water1(q))
        self.array.append(Water2(q))
        self.array.append(Water3(q))


class WaterChartVariables(ChartVariables):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.title += "Water"
        self.xAxisTitleText = "Time"
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

    def __init__(self, c: float = 0.0):
        self.c = c

    def populate(self, c: float):
        self.c = c

    def method(self, x):
        return abs(self.c * x)


class Water(Template):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.consume = Consume()
        self.rain = Rain()
        self.import_w = ImportW()
        self.contaminate = Contaminate()
        self.recycle = Recycle()

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

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)

        t = UtilsJSONEncoder()
        t.encode(self.rain)
        t.encode(self.import_w)
        t.encode(self.contaminate)

        self.consume.populate(0.0, -2.0)
        self.rain.populate(3.0, 2.0, 1.0, 3.0)
        self.import_w.populate(3.0, 2.0, 1.0, 3.0)
        self.contaminate.populate(3.0, 2.0, 1.0, -3.0)
        self.recycle.populate(0.4)


class Water2(Water):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)

        t = UtilsJSONEncoder()
        t.encode(self.rain)
        t.encode(self.import_w)
        t.encode(self.contaminate)

        self.consume.populate(0.0, -5.0)
        self.rain.populate(3.0, 2.0, 1.0, 3.0)
        self.import_w.populate(3.0, 2.0, 1.0, 3.0)
        self.contaminate.populate(3.0, 2.0, 1.0, -3.0)
        self.recycle.populate(0.4)


class Water3(Water):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)

        t = UtilsJSONEncoder()
        t.encode(self.rain)
        t.encode(self.import_w)
        t.encode(self.contaminate)

        self.consume.populate(0.0, -8.0)
        self.rain.populate(3.0, 2.0, 1.0, 3.0)
        self.import_w.populate(3.0, 2.0, 1.0, 3.0)
        self.contaminate.populate(3.0, 2.0, 1.0, -3.0)
        self.recycle.populate(0.4)
