from mongoengine import Document, StringField, FloatField, IntField


class ModelRequestObj(Document):
    base_model = StringField(required=True)
    timeframe_multiplier = FloatField(required=True)
    timeframe_increment_multiplier = FloatField(required=True)
    timeframe_unit = IntField(required=True)


class DataObj(Document):
    data_string = StringField(required=True)
