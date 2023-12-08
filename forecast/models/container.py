# container.py
from forecast.models.c import CChartVariables, CArray
from forecast.models.d import DChartVariables, DArray


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
            self.models = CArray(timeframe_multiplier,
                                 timeframe_unit,
                                 timeframe_increment_multiplier).array
        elif base_model == "D":
            self.chartVariables = DChartVariables(timeframe_multiplier,
                                                  timeframe_unit,
                                                  timeframe_increment_multiplier).__dict__
            self.models = DArray(timeframe_multiplier,
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
