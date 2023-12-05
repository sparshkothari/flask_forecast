from mongoengine import Document, StringField


class ForecastObj(Document):
    data_string = StringField(required=True)
