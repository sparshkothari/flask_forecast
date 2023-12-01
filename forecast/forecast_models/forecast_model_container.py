# forecast_model_container.py
from forecast.forecast_models.base_model_a import ModelASustainable, ModelANonSustainable


class ForecastModelContainer:

    def __init__(self,
                 forecast_base_model: str,
                 forecast_environment: int,
                 forecast_timeframe: float):
        self.forecast_model = ""
        if forecast_base_model == "A":
            if forecast_environment == 1:
                self.forecast_model = ModelASustainable(forecast_timeframe)
            elif forecast_environment == 2:
                self.forecast_model = ModelANonSustainable(forecast_timeframe)

    def run(self):
        self.forecast_model.simulate_model()
        return self.forecast_model.__dict__
