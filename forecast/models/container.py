# container.py
from forecast.models.c import CChartVariables, CArray
from forecast.models.d import DChartVariables, DArray
from forecast.models.e import EChartVariables, EArray
from models import ModelRequestObj


class Container:

    def __init__(self, q: ModelRequestObj):
        self.models = []
        self.simulated_models = []
        self.chartVariables = {}
        if q.base_model == "C":
            self.chartVariables = CChartVariables(q).__dict__
            self.models = CArray(q).array
        elif q.base_model == "D":
            self.chartVariables = DChartVariables(q).__dict__
            self.models = DArray(q).array
        elif q.base_model == "E":
            self.chartVariables = EChartVariables(q).__dict__
            self.models = EArray(q).array

    def run(self):
        o = []
        for model in self.models:
            model.simulate_model()
            self.simulated_models.append(model.__dict__)
        o.append(self.chartVariables)
        o.append(self.simulated_models)
        return o
