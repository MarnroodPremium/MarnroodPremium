from os import get_terminal_size

from colorama import Fore, Back
from hotel import Hotel

def main():
    hotel = Hotel()

    LINE_WIDTH = get_terminal_size().columns

    entries = [
        'Check if a room is available',
        'Manually check-in guests',
        'Manually check-out guests',
        'Print all rooms with guest',
        'Print all rooms with no guest',
        'Export as csv',
        'Initialize new hotel',
    ]

    LONGEST_ENTRY = max(map(len, entries))
    LEFT_PAD = int((LINE_WIDTH - LONGEST_ENTRY - 2) / 2)

    LINE_SEPERATOR = '='

    while True:
        print(LINE_SEPERATOR * LINE_WIDTH)

        print(f'{'Marnrood Premium':^{LINE_WIDTH}}')
        print()

        for index, entry in enumerate(entries, 1):
            print(f'{' '*LEFT_PAD}{index} {entry}')

        print(f'{' '*LEFT_PAD}q Exit program')

        print(LINE_SEPERATOR * LINE_WIDTH)

        option_string = input(f'{' '*LEFT_PAD}Select an option : ')

        if option_string == 'q':
            return

        try:
            option = int(option_string)
            match option:
                case 1:
                    pass
                case 2:
                    hotel.manual_insert()
                case 3:
                    pass
                case 4:
                    hotel.print_room_inorder()
                case 5:
                    hotel.print_missing_rooms_inorder()
                case 6:
                    filename = input(f'{' '*LEFT_PAD}Enter filename : ')
                    hotel.export_csv(filename)
                case 7:
                    hotel = Hotel()
                case _:
                    raise ValueError('Invalid option')

        except Exception as exc:
            print(f'{Back.RED}Error: {exc}{Back.RESET}')

main()
