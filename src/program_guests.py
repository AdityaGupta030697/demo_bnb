from dateutil import parser
from datetime import datetime

from infra.switchlang import switch
import program_hosts as hosts
import infra.state as state
import services.db_services as db_svc


def run():
    print(' ****************** Welcome guest ****************\n')

    show_commands()

    while True:
        action = hosts.get_action()

        with switch(action) as s:
            s.case('c', hosts.create_account)
            s.case('l', hosts.log_into_account)

            s.case('a', add_guest)
            s.case('y', view_guests)
            s.case('b', book_room)
            s.case('v', view_bookings)
            s.case('m', lambda: 'change_mode')

            s.case('?', show_commands)
            s.case('', lambda: None)
            s.case(['x', 'bye', 'exit', 'exit()'], hosts.exit_app)

            s.default(hosts.unknown_command)

        state.reload_account()

        if s.result == 'change_mode':
            return


def show_commands():
    print('What would you like to do?')
    print('[c]reate an account')
    print('[l]ogin to your account')
    print('[b]ook a room')
    print('[a]dd a guest')
    print('View [y]our guests')
    print('[v]iew your bookings')
    print('[m]ain menu')
    print('e[x]it app')
    print('[?] Help (this info)\n')


def add_guest():
    print(' ****************** Add a guest **************** ')
    # Require an active account
    if not state.active_account:
        hosts.error_msg("Please login first to register a guest!")
        return

    # Get guest info from guest
    name = input("Please enter guest name as 'FIRST_NAME LAST_NAME':")
    email = input("Please enter guest  email id:").lower().strip()
    age = int(input("Please enter guest  age:"))
    phone = input("Please enter guest  phone number:")
    gender = input("Please enter guest  gender:")

    # Create the guest in the DB.
    guest = db_svc.add_guest(state.active_account, name, email, age, phone,
                             gender)
    state.reload_account()
    hosts.success_msg("Added {} {} as a guest".format(guest.first_name,
                                                      guest.last_name))


def view_guests():
    # Require an active account
    if not state.active_account:
        hosts.error_msg("Please login first to register a guest!")
        return

    # Get guests from DB, show details list
    guests = db_svc.find_guests_for_user(state.active_account.email)
    print(' ****************** {}\'s Guests ****************'.
          format(state.active_account.first_name))
    for i, guest in enumerate(guests):
        print("{}. {} {} is a guest with age {}, email {}, "
              "gender {}, and phone {}".format(i+1, guest.first_name,
                                               guest.last_name,
                                               guest.age,
                                               guest.email,
                                               guest.gender,
                                               guest.phone_number))
    print(" ****************** END **************** ")


def book_room():
    print(' ****************** Book a room **************** ')
    # Require an active account
    if not state.active_account:
        hosts.error_msg("Please login first to register a guest!")
        return

    guests = db_svc.find_guests_for_user(state.active_account.email)
    # Verify they have a guest
    if not guests:
        hosts.error_msg("Please add a guest first!")
        return

    print("Lets start finding rooms..")
    # Get dates and select guest
    start_date = input("Enter Check in date [YYYY-MM-DD]: ").strip()
    if not start_date:
        hosts.error_msg("Cancelled!")
        return
    start_date = parser.parse(start_date)
    end_date = parser.parse(input("Enter Check out date [YYYY-MM-DD]: "))

    if start_date >= end_date:
        hosts.error_msg("Check in can't be on/after Checkout date")
        return

    print("Please choose available guest from the list: ")
    view_guests()
    guest_no = int(input("Chosen Guest no?: ").strip())
    guest = guests[guest_no-1]

    # Find rooms available across date range
    allow_pets = bool(input("Does this guest has pet(s)? [y/n]: ")
                      .strip().startswith('y'))
    rooms = db_svc.get_available_rooms(start_date, end_date, allow_pets)

    if not rooms:
        hosts.error_msg("Sorry, there are no rooms available for that date!")
        return

    print("You have {} rooms.".format(len(rooms)))
    for idx, room in enumerate(rooms):
        print("{} Room {}, {} type is priced at Rs.{} with pets {}\n"
              .format(idx+1, room.number, room.rtype, room.price,
                      "allowed" if room.allow_pets else "not allowed"))
        for b in room.bookings:
            print('      * Booking: {}, {} days, booked? {}'.format(
                b.check_in_date,
                (b.check_out_date - b.check_in_date).days,
                'YES' if b.booked_date is not None else 'no'
            ))
    # Let user select room to book.
    selected_room = rooms[int(input("Pick a room: "))-1]
    db_svc.book_room(state.active_account, guest, selected_room,
                     start_date, end_date)
    hosts.success_msg("Room {} booked successfully at Rs.{}/night!"
                      .format(selected_room.number, selected_room.price))


def view_bookings():
    print(' ****************** Your bookings **************** ')
    # Require an active account
    if not state.active_account:
        hosts.error_msg("Please login first to register a guest!")
        return

    guests = {g.id: g for g in
              db_svc.find_guests_for_user(state.active_account.email)}
    bookings = db_svc.get_bookings_for_user(state.active_account.email)

    print("You have {} bookings.".format(len(bookings)))
    for b in bookings:
        # noinspection PyUnresolvedReferences
        print(' * Guest: {} {} is booked at {} from {} for {} days.'.format(
            guests.get(b.guest_id).first_name,
            guests.get(b.guest_id).last_name,
            b.room.number,
            b.check_in_date.date(),
            b.duration_in_days
        ))

