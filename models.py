from mongoengine import Document, StringField


class DataObj(Document):
    data_string = StringField(required=True)
