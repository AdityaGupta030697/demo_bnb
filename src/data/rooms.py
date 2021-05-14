import mongoengine
from datetime import datetime
from mongo_setup import PhoneField, MONGODB_ALIAS_CORE

import data.bookings


class Room(mongoengine.Document):
    registration_date = mongoengine.DateTimeField(default=datetime.now)
    id = mongoengine.ObjectIdField()
    price = mongoengine.FloatField(min_value=0.0, required=True)
    area = mongoengine.FloatField(min_value=0.0, required=True)
    allow_pets = mongoengine.BooleanField(default=False)
    type = mongoengine.StringField(required=True)

    bookings = mongoengine.EmbeddedDocumentListField(data.bookings.Booking)

    meta = {'db_alias': MONGODB_ALIAS_CORE, 'collection': 'rooms'}
