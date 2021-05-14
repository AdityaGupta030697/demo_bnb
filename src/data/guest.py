import mongoengine
from data.mongo_setup import PhoneField, MONGODB_ALIAS_CORE
from datetime import datetime


class Guest(mongoengine.Document):
    age = mongoengine.IntField(min_value=1)
    email = mongoengine.EmailField(required=True)
    first_name = mongoengine.StringField(min_length=1, required=True)
    gender = mongoengine.StringField(min_length=1, default="UNKNOWN")
    last_name = mongoengine.StringField(min_length=1, required=True)
    phone_number = PhoneField(default="UNKNOWN")
    registration_date = mongoengine.DateTimeField(default=datetime.now)

    meta = {'db_alias': MONGODB_ALIAS_CORE, 'collection': 'guests'}



