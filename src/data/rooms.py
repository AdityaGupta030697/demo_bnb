import mongoengine
from datetime import datetime
from data.mongo_setup import MONGODB_ALIAS_CORE

import data.bookings


class Room(mongoengine.Document):
    registration_date = mongoengine.DateTimeField(default=datetime.now)
    number = mongoengine.StringField(min_length=1, required=True)
    price = mongoengine.FloatField(min_value=0.0, required=True)
    area = mongoengine.FloatField(min_value=0.0)
    allow_pets = mongoengine.BooleanField(default=False)
    rtype = mongoengine.StringField(required=True)

    bookings = mongoengine.EmbeddedDocumentListField(data.bookings.Booking)

    meta = {'db_alias': MONGODB_ALIAS_CORE, 'collection': 'rooms'}
