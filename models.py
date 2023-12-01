from mongoengine import Document, StringField


class WaterForecastObj(Document):
    water_forecast_obj_dict_string = StringField(required=True)
