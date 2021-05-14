import mongoengine
from datetime import datetime
from data.mongo_setup import PhoneField, MONGODB_ALIAS_CORE


class Owner(mongoengine.Document):
    registration_date = mongoengine.DateTimeField(default=datetime.now)
    email = mongoengine.EmailField(required=True)
    age = mongoengine.IntField(min_value=1)
    first_name = mongoengine.StringField(min_length=1, required=True)
    gender = mongoengine.StringField(min_length=1, default="UNKNOWN")
    last_name = mongoengine.StringField(min_length=1, required=True)
    phone_number = PhoneField(default="UNKNOWN")

    guest_ids = mongoengine.ListField()
    room_ids = mongoengine.ListField()

    meta = {'db_alias': MONGODB_ALIAS_CORE, 'collection': 'owners'}
