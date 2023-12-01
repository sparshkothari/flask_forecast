# rainfall.py
from random import Random


class WaterForecast:

    def __init__(self, water_forecast_model: int):
        if water_forecast_model == 1:
            self.average_daily_water_consumption = 500.0
            self.daily_rainfall_probability = 0.2
            self.average_water_collection_per_rainfall = 10000.0
            self.daily_water_import_probability = 0.15
            self.average_water_collection_per_import = 1000
            self.daily_contamination_probability = 0.1
            self.average_percent_water_lost_during_contamination = 0.05
            self.duration_number_of_days = 365
        self.current_water_reserves = 0.0
        self.water_reserves_data = []

    def run(self):
        for i in range(0, self.duration_number_of_days):
            self.consume()
            self.rainfall()
            self.import_water()
            self.contaminate()
            data_item = {"day": i, "water_reserves": self.current_water_reserves}
            self.water_reserves_data.append(data_item)

        return self.__dict__

    def consume(self):
        self.current_water_reserves -= self.average_daily_water_consumption

    def rainfall(self):
        if Random().random() < self.daily_rainfall_probability:
            self.current_water_reserves += self.average_water_collection_per_rainfall

    def import_water(self):
        if Random().random() < self.daily_water_import_probability:
            self.current_water_reserves += self.average_water_collection_per_import

    def contaminate(self):
        if Random().random() < self.daily_contamination_probability:
            self.current_water_reserves -= (self.average_percent_water_lost_during_contamination *
                                            self.current_water_reserves)