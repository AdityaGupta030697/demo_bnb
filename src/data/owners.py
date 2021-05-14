class Owner:
    registration_date = None
    email = None
    age = None
    first_name = None
    gender = None
    last_name = None
    phone_number = None

    guest_ids = list()
    room_ids = list()

    meta = {'db_alias': 'core', 'collection': 'rooms'}