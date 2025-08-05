from mongoengine import Document, StringField, FloatField, IntField, BooleanField


class ModelRequestObj(Document):
    base_model = IntField(required=True)
    index_start = FloatField(required=True)
    index_stop = FloatField(required=True)
    increment = FloatField(required=True)
    limit_bounds = BooleanField(required=True)


class DataObj(Document):
    data_string = StringField(required=True)
