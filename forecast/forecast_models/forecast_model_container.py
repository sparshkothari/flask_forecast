# forecast_model_container.py
from forecast.forecast_models.base_model_a import GenerateBaseModelAArray, BaseModelAChartVariables
from forecast.forecast_models.base_model_b import BaseModelBChartVariables, GenerateBaseModelBArray


class ForecastModelContainer:

    def __init__(self,
                 base_model: str,
                 timeframe_multiplier: float, timeframe_unit: int, timeframe_increment_multiplier: float):
        self.models = []
        self.simulated_models = []
        self.chartVariables = {}
        if base_model == "A":
            self.chartVariables = BaseModelAChartVariables(timeframe_multiplier,
                                                           timeframe_unit,
                                                           timeframe_increment_multiplier).__dict__
            self.models = GenerateBaseModelAArray(timeframe_multiplier,
                                                  timeframe_unit,
                                                  timeframe_increment_multiplier).array
        elif base_model == "B":
            self.chartVariables = BaseModelBChartVariables(timeframe_multiplier,
                                                           timeframe_unit,
                                                           timeframe_increment_multiplier).__dict__
            self.models = GenerateBaseModelBArray(timeframe_multiplier,
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
