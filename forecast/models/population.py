# population.py
import math

from utils import UtilsJSONEncoder, CosineF, SineF, LineT
from forecast.models.template import Template, GenerateArray, \
    ChartVariables
from models import ModelRequestObj


class PopulationArray(GenerateArray):

    def __init__(self, q: ModelRequestObj):
        super().__init__()
        self.array.append(Population1(q))
        self.array.append(Population2(q))


class PopulationChartVariables(ChartVariables):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.title += "Population"
        self.xAxisTitleText = "Time"
        self.yAxisTitleText = "{placeholder}"


class Population(Template):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.growth = Growth()

        t = UtilsJSONEncoder()
        t.encode(self.growth)

    def iterate(self, index):
        super().iterate(index)
        x = index
        self.data_point = self.growth.method(x)


class Population1(Population):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.growth = LogisticGrowth()

        t = UtilsJSONEncoder()
        t.encode(self.growth)

        self.growth.populate(100.0, 1.0, 0.2)


class Population2(Population):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.growth = LogisticGrowth()

        t = UtilsJSONEncoder()
        t.encode(self.growth)

        self.growth.populate(100.0, 1.0, 0.7)


class Growth:

    def __init__(self):
        pass

    def populate(self):
        pass

    def method(self, time: float = 0.0):
        return time


class LogisticGrowth(Growth):

    def __init__(self, carrying_capacity: float = 0.0, initial_population: float = 0.0, growth_constant: float = 0.0):
        super().__init__()
        self.carrying_capacity = carrying_capacity
        self.initial_population = initial_population
        self.growth_constant = growth_constant

    def populate(self, carrying_capacity: float = 0.0, initial_population: float = 0.0, growth_constant: float = 0.0):
        super().populate()
        self.carrying_capacity = carrying_capacity
        self.initial_population = initial_population
        self.growth_constant = growth_constant

    def method(self, time: float = 0.0):
        super().method(time)
        t = time
        a = (self.carrying_capacity - self.initial_population) / self.initial_population
        e = math.e
        return self.carrying_capacity / (1 + (a * math.pow(e, -1.0 * self.growth_constant * t)))
