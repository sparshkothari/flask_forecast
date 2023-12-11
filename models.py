from mongoengine import Document, StringField, FloatField, IntField


class ModelRequestObj(Document):
    base_model = IntField(required=True)
    index_start = FloatField(required=True)
    index_stop = FloatField(required=True)
    increment = FloatField(required=True)


class DataObj(Document):
    data_string = StringField(required=True)
