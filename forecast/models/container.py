# container.py
from forecast.models.water import WaterArray, WaterChartVariables
from forecast.models.population import PopulationArray, PopulationChartVariables
from models import ModelRequestObj


class Container:

    def __init__(self, q: ModelRequestObj):
        self.models = []
        self.simulated_models = []
        self.chartVariables = {}
        if q.base_model == 0:
            self.models = WaterArray(q).array
            self.chartVariables = WaterChartVariables().__dict__
        elif q.base_model == 1:
            self.models = PopulationArray(q).array
            self.chartVariables = PopulationChartVariables().__dict__

    def run(self):
        o = []
        for model in self.models:
            model.simulate_model()
            self.simulated_models.append(model.__dict__)
        o.append(self.chartVariables)
        o.append(self.simulated_models)
        return o
