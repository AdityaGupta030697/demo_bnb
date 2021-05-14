class Room:
    registration_date = None
    name = None
    price = None
    area = None
    allow_pets = None
    type = None

    bookings = list()

    meta = {'db_alias': 'core', 'collection': 'rooms'}
