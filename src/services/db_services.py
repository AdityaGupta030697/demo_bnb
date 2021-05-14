from typing import List
from datetime import datetime, timedelta

from data.owners import Owner
from data.rooms import Room
from data.bookings import Booking


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


