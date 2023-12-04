# forecast_model_container.py
from forecast.forecast_models.base_model_a import ModelASustainable, ModelANonSustainable, GenerateBaseModelAArray, \
    BaseModelAChartVariables


class ForecastModelContainer:

    def __init__(self,
                 forecast_base_model: str,
                 forecast_timeframe: float):
        self.forecast_models = []
        self.simulated_models = []
        self.chartVariables = BaseModelAChartVariables(forecast_timeframe).__dict__
        if forecast_base_model == "A":
            self.forecast_models = GenerateBaseModelAArray(forecast_timeframe).array

    def run(self):
        o = []
        for model in self.forecast_models:
            model.simulate_model()
            self.simulated_models.append(model.__dict__)
        o.append(self.chartVariables)
        o.append(self.simulated_models)
        return o
