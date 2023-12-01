# forecast_model_template.py


class ForecastModelTemplate:

    def __init__(self, forecast_timeframe: float):
        self.forecast_model_name = self.__class__.__name__
        self.duration_number_of_days = int(forecast_timeframe * 365)
        self.current_water_reserves = 0.0
        self.water_reserves_data = []

    def simulate_model(self):
        for i in range(0, self.duration_number_of_days):
            self.iterate()
            data_item = {"day": i, "water_reserves": self.current_water_reserves}
            self.water_reserves_data.append(data_item)

    def iterate(self):
        pass
