from typing import List, Optional
from datetime import datetime, timedelta

from data.owners import Owner
from data.rooms import Room
from data.bookings import Booking
from data.guests import Guest


def create_account(name: str, email: str, age: int,
                   phone: str, gender: str) -> Owner:
    owner = Owner()
    owner.first_name = name.split(" ")[0]
    owner.last_name = name.split(" ")[1]
    owner.email = email
    owner.age = age
    owner.phone_number = phone
    owner.gender = gender
    owner.save()
    return owner


def find_account_by_email(email: str) -> Owner:
    return Owner.objects(email=email).first()


def register_room(account: Owner, number: str, rtype: str, price: float,
                  area: float, allow_pets: bool) -> Room:
    room = Room()
    room.number = number
    room.rtype = rtype
    room.price = price
    room.area = area
    room.allow_pets = allow_pets
    # Save the room to DB.
    room.save()

    # Get latest owner info from the db
    account = find_account_by_email(account.email)
    # Append it to the list of rooms
    account.room_ids.append(room.id)
    account.save()

    return room


def find_rooms_for_user(account: Owner) -> List[Room]:
    return list(Room.objects(id__in=account.room_ids))


def find_room_by_number(room_number: str) -> Room:
    return Room.objects(number=room_number).first()


def update_room_availability_date(room: Room,
                                  start_date: datetime, num_days: int) -> Room:
    booking = Booking()
    booking.check_in_date = start_date
    booking.check_out_date = start_date + timedelta(days=num_days)

    selected_room = find_room_by_number(room.number)
    selected_room.bookings.append(booking)
    selected_room.save()
    return selected_room


def add_guest(account, name, email, age, phone, gender) -> Guest:
    guest = Guest()
    guest.first_name = name.split(" ")[0]
    guest.last_name = name.split(" ")[1]
    guest.age = age
    guest.email = email
    guest.gender = gender
    guest.phone_number = phone
    guest.save()

    owner = find_account_by_email(account.email)
    owner.guest_ids.append(guest.id)
    owner.save()

    return guest


def find_guests_for_user(email):
    owner = Owner.objects(email=email).first()
    return list(Guest.objects(id__in=owner.guest_ids).all())


def get_available_rooms(start_date: datetime, end_date: datetime,
                        allow_pets: bool) -> List[Room]:
    query = Room.objects().filter(bookings__check_in_date__lte=start_date)\
        .filter(bookings__check_out_date__gte=end_date)
    if allow_pets:
        query = query.filter(allow_pets=True)

    rooms = list(query.order_by('price', '-area'))

    for room in rooms:
        for booking in room.bookings:
            if (booking.check_in_date > start_date) and booking.check_out_date \
                    < end_date and booking.guest_id is not None:
                rooms.remove(room)

    return rooms


def book_room(account: Owner, guest: Guest, selected_room: Room,
              start_date: datetime, end_date: datetime):
    booking: Optional[Booking] = None
    for b in selected_room.bookings:
        if b.check_in_date <= start_date and b.check_out_date >= end_date \
                and b.guest_id is None:
            booking = b
            break
    booking.guest_owner_id = account.id
    booking.guest_id = guest.id
    booking.booked_date = datetime.now()
    booking.check_in_date = start_date
    booking.check_out_date = end_date

    selected_room.save()


def get_bookings_for_user(email: str) -> List[Booking]:
    account = find_account_by_email(email)

    booked_rooms = Room.objects() \
        .filter(bookings__guest_owner_id=account.id) \
        .only('bookings', 'number')

    def map_cage_to_booking(room, booking):
        booking.room = room
        return booking

    bookings = [
        map_cage_to_booking(room, booking)
        for room in booked_rooms
        for booking in room.bookings
        if booking.guest_owner_id == account.id
    ]

    return bookings
