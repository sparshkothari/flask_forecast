from mongoengine import Document, StringField, IntField


class ModelRequestObj(Document):
    base_model = StringField(required=True)
    index_start = IntField(required=True)
    index_stop = IntField(required=True)
    increment = IntField(required=True)


class DataObj(Document):
    data_string = StringField(required=True)
