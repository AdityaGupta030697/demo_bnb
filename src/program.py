import sys
from enum import Enum
from colorama import Fore, init
from infra.switchlang import switch
import program_guests
import program_hosts


class UserIntent(Enum):
    BOOK = 0
    OFFER = 1


def main():
    # TODO: Setup mongoengine global values

    print_header()

    try:
        while True:
            user_intent = find_user_intent()
            if user_intent == UserIntent.BOOK:
                program_guests.run()
            elif user_intent == UserIntent.OFFER:
                program_hosts.run()
            else:
                program_hosts.unknown_command()
    except KeyboardInterrupt:
        sys.exit(0)


def print_header():
    init()
    demo = \
        """
 _ .-') _    ('-. _   .-')                     .-. .-')      .-') _.-. .-')   
( (  OO) ) _(  OO( '.( OO )_                   \  ( OO )    ( OO ) \  ( OO )  
 \     .'_(,------,--.   ,--..-'),-----.        ;-----.\,--./ ,--,' ;-----.\  
 ,`'--..._)|  .---|   `.'   ( OO'  .-.  '       | .-.  ||   \ |  |\ | .-.  |  
 |  |  \  '|  |   |         /   |  | |  |       | '-' /_|    \|  | )| '-' /_) 
 |  |   ' (|  '--.|  |'.'|  \_) |  |\|  |       | .-. `.|  .     |/ | .-. `.  
 |  |   / :|  .--'|  |   |  | \ |  | |  |       | |  \  |  |\    |  | |  \  | 
 |  '--'  /|  `---|  |   |  |  `'  '-'  '       | '--'  |  | \   |  | '--'  / 
 `-------' `------`--'   `--'    `-----'        `------'`--'  `--'  `------'  
        """

    print(Fore.WHITE + '*' * 40 + 'Demo BnB' + '*' * 40)
    print(Fore.GREEN + demo)
    print(Fore.WHITE + '*' * 90)
    print("Welcome to Demo BnB! \nWhy are you here?")


def find_user_intent():
    print("[g] Book a room \n[h] Offer extra space \nE[x]it App")
    choice = input("Are you a [g]uest or a [h]ost? ").lower()

    with switch(choice) as intent:
        intent.case('h', lambda: UserIntent.OFFER)
        intent.case('g', lambda: UserIntent.BOOK)
        intent.case('x', program_hosts.exit_app)
        intent.default(lambda: None)
    return intent.result


if __name__ == '__main__':
    main()
