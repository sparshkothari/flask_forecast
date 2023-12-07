# container.py
from forecast.forecast_models.c import CChartVariables, GenerateCArray


class Container:

    def __init__(self,
                 base_model: str,
                 timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        self.models = []
        self.simulated_models = []
        self.chartVariables = {}
        if base_model == "C":
            self.chartVariables = CChartVariables(timeframe_multiplier,
                                                           timeframe_unit,
                                                           timeframe_increment_multiplier).__dict__
            self.models = GenerateCArray(timeframe_multiplier,
                                                  timeframe_unit,
                                                  timeframe_increment_multiplier).array

    def run(self):
        o = []
        for model in self.models:
            model.simulate_model()
            self.simulated_models.append(model.__dict__)
        o.append(self.chartVariables)
        o.append(self.simulated_models)
        return o
