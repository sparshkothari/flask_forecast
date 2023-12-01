# forecast_model_container.py
from water_forecast.forecast_models.base_model_a import ModelASustainable, ModelANonSustainable


class ForecastModelContainer:

    def __init__(self, forecast_model_name: str, forecast_timeframe: float):
        self.forecast_model = ""
        if forecast_model_name == "A1":
            self.forecast_model = ModelASustainable(forecast_timeframe)
        elif forecast_model_name == "A2":
            self.forecast_model = ModelANonSustainable(forecast_timeframe)

    def run(self):
        self.forecast_model.simulate_model()
        return self.forecast_model.__dict__
