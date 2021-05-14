from colorama import Fore, init
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
    name = input("Please enter your name as 'FIRST_NAME LAST_NAME':")
    email = input("Please enter your email id:")
    age = int(input("Please enter your age:"))
    phone = input("Please enter your phone number:")
    gender = input("Please enter your gender:")

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

    # TODO: Get email
    # TODO: Find account in DB, set as logged in.

    print(" -------- NOT IMPLEMENTED -------- ")


def register_room():
    print(' ****************** REGISTER ROOM **************** ')

    # TODO: Require an account
    # TODO: Get info about room
    # TODO: Save the room to DB.

    print(" -------- NOT IMPLEMENTED -------- ")


def list_rooms(supress_header=False):
    if not supress_header:
        print(' ****************** Your rooms **************** ')

    # TODO: Require an account
    # TODO: Get rooms, list details

    print(" -------- NOT IMPLEMENTED -------- ")


def update_availability():
    print(' ****************** Add available date **************** ')

    # TODO: Require an account
    # TODO: list rooms
    # TODO: Choose room
    # TODO: Set dates, save to DB.

    print(" -------- NOT IMPLEMENTED -------- ")


def view_bookings():
    print(' ****************** Your bookings **************** ')

    # TODO: Require an account
    # TODO: Get rooms, and nested bookings as flat list
    # TODO: Print details for each

    print(" -------- NOT IMPLEMENTED -------- ")


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
