from mongoengine import Document, StringField


class ForecastObj(Document):
    model_obj_dict_string = StringField(required=True)
