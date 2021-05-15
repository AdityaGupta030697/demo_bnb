from colorama import Fore, init
from dateutil import parser
from datetime import datetime

from infra.switchlang import switch
import infra.state as state
import services.db_services as db_svc


def run():
    init()
    print(' ****************** Welcome host ****************\n')
    show_commands()

    while True:
        action = get_action()

        with switch(action) as s:
            s.case('c', create_account)
            s.case('a', log_into_account)
            s.case('l', list_rooms)
            s.case('r', register_room)
            s.case('u', update_availability)
            s.case('v', view_bookings)
            s.case('m', lambda: 'change_mode')
            s.case(['x', 'bye', 'exit', 'exit()'], exit_app)
            s.case('?', show_commands)
            s.case('', lambda: None)
            s.default(unknown_command)

        if s.result == 'change_mode':
            return


def show_commands():
    print('What would you like to do?')
    print('[c]reate an account')
    print('Login to your [a]ccount')
    print('[l]ist your rooms')
    print('[r]egister a room')
    print('[u]pdate room availability')
    print('[v]iew your bookings')
    print('Change [m]ode (guest or host)')
    print('e[x]it app')
    print('[?] Help (this info) \n')


def create_account():
    print(' ****************** REGISTER **************** ')
    # Get owner details
    name = input("Please enter your name as 'FIRST_NAME LAST_NAME': ")
    email = input("Please enter your email id: ").lower().strip()
    age = int(input("Please enter your age: "))
    phone = input("Please enter your phone number: ")
    gender = input("Please enter your gender: ")

    # Check for old account
    old_account = db_svc.find_account_by_email(email)
    if old_account:
        error_msg("Account already exists with email".format(email))
        return

    # Create a new one and set it as active account
    state.active_account = db_svc.create_account(name, email, age,
                                                 phone, gender)
    success_msg("Successfully created an account with email: {}".format(email))


def log_into_account():
    print(' ****************** LOGIN **************** ')

    email = input("Please enter your email id:").lower().strip()
    # Get existing account and set as active account
    account = db_svc.find_account_by_email(email)

    if not account:
        error_msg("Account doesn't exists! Please create a new one...")
        return

    state.active_account = account
    success_msg("Successfully logged into account with email: {}".format(email))


def register_room():
    print(' ****************** REGISTER ROOM **************** ')

    # Require an active account
    if not state.active_account:
        error_msg("Please login first to register a room!")
        return

    # Get info about room
    number = input("Please enter room number: ")
    rtype = input("Please enter room type: ")
    price = float(input("Please enter room's price: "))
    area = input("Please enter room's area: ")
    if area:
        area = float(area)
    allow_pets = input("Allow pets? [y/n]: ").lower().startswith("y")
    # Register the room
    room = db_svc.register_room(state.active_account, number, rtype, price,
                                area, allow_pets)
    success_msg("Room {} registered successfully!".format(room.number))

    # Fetch the new details in the active account
    state.reload_account()


def list_rooms(suppress_header=False):
    # Require an active account
    if not state.active_account:
        error_msg("Please login first to register a room!")
        return
    if not suppress_header:
        print(' ****************** Your rooms **************** ')

    # Get rooms, list details
    rooms = db_svc.find_rooms_for_user(state.active_account)
    print(Fore.YELLOW + "You have {} room(s)".format(len(rooms)) + Fore.WHITE)
    for idx, room in enumerate(rooms):
        print("{} Room {}, {} type is priced at Rs.{} with pets {}"
              .format(idx+1, room.number, room.rtype, room.price,
                      "allowed" if room.allow_pets else "not allowed"))
        for b in room.bookings:
            print('     * Booking: {}, {} days, booked? {}'.format(
                b.check_in_date,
                (b.check_out_date - b.check_in_date).days,
                'YES' if b.booked_date is not None else 'NO'
            ))
    print(' ****************** END ****************')


def update_availability():
    print(' ****************** Add available date **************** ')

    if not state.active_account:
        error_msg("Please login first to register a room!")
        return

    # List rooms
    list_rooms()

    # Choose room
    room_number = input("Enter desired room number Ex: S101, "
                        "[Enter to cancel]: ").strip()
    if not room_number:
        error_msg("Cancelled!\n")
        return

    room = db_svc.find_room_by_number(room_number)

    # Set dates, save to DB.
    start_date = parser.parse(input("Enter Starting date [YYYY-MM-DD]: "))
    num_days = int(input("Enter the availability in days: "))

    db_svc.update_room_availability_date(room, start_date, num_days)
    success_msg("Room {} availability updated!".format(room.number))


def view_bookings():
    print(' ****************** Your bookings **************** ')
    if not state.active_account:
        error_msg("You must log in first to register a cage")
        return

    rooms = db_svc.find_rooms_for_user(state.active_account)

    bookings = [
        (c, b)
        for c in rooms
        for b in c.bookings
        if b.booked_date is not None
    ]

    print("You have {} bookings.".format(len(bookings)))
    for c, b in bookings:
        print(' * Room: {}, booked date: {}, from {} for {} days.'.format(
            c.number,
            b.booked_date.date(),
            b.check_in_date.date(),
            b.duration_in_days
        ))


def exit_app():
    print()
    print('Bye...')
    raise KeyboardInterrupt()


def get_action():
    text = '> '
    if state.active_account:
        text = '{} {}> '.format(state.active_account.first_name,
                                state.active_account.last_name)

    action = input(text)
    return action.strip().lower()


def unknown_command():
    print("Sorry we didn't understand that command...\n")


def success_msg(text):
    print(Fore.LIGHTGREEN_EX + text + Fore.WHITE)


def error_msg(text):
    print(Fore.LIGHTRED_EX + text + Fore.WHITE)
