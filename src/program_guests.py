from infra.switchlang import switch
import program_hosts as hosts
import infra.state as state


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
    # TODO: Require an account
    # TODO: Get guest info from user
    # TODO: Create the guest in the DB.

    print(" -------- NOT IMPLEMENTED -------- ")


def view_guests():
    print(' ****************** Your guests **************** ')

    # TODO: Require an account
    # TODO: Get guests from DB, show details list

    print(" -------- NOT IMPLEMENTED -------- ")


def book_room():
    print(' ****************** Book a room **************** ')
    # TODO: Require an account
    # TODO: Verify they have a guest
    # TODO: Get dates and select guest
    # TODO: Find rooms available across date range
    # TODO: Let user select room to book.

    print(" -------- NOT IMPLEMENTED -------- ")


def view_bookings():
    print(' ****************** Your bookings **************** ')
    # TODO: Require an account
    # TODO: List booking info along with guests info

    print(" -------- NOT IMPLEMENTED -------- ")
