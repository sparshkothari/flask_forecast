# forecast_model_container.py
from forecast.forecast_models.base_model_a import ModelASustainable, ModelANonSustainable


class ForecastModelContainer:

    def __init__(self,
                 forecast_base_model: str,
                 forecast_environment_number: int,
                 forecast_timeframe: float):
        self.forecast_models = []
        self.forecast_timeframe = int(forecast_timeframe * 365)
        if forecast_base_model == "A":
            if forecast_environment_number == 0:
                self.forecast_models.append(ModelASustainable(forecast_timeframe))
                self.forecast_models.append(ModelANonSustainable(forecast_timeframe))
            elif forecast_environment_number == 1:
                self.forecast_models.append(ModelASustainable(forecast_timeframe))
            elif forecast_environment_number == 2:
                self.forecast_models.append(ModelANonSustainable(forecast_timeframe))

    def run(self):
        response = []
        for model in self.forecast_models:
            model.simulate_model()
            response.append(model.__dict__)
        return response
