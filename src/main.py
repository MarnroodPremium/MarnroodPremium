from colorama import Back, Fore
from hotel import Hotel


def initialize_hotel() -> Hotel:
    print(f"{Fore.GREEN}Hotel Initialization{Fore.RESET}")
    while True:
        try:
            ex_guest = int(
                input(
                    f"{Fore.BLUE}Enter amount of peoples already in the hotel : {Fore.RESET}"
                )
            )
            channels = list(
                map(
                    int,
                    input(
                        f"{Fore.CYAN}Enter amount of peoples car boat spaceship (seperated by space) : {Fore.RESET}"
                    ).split(),
                )
            )
            hotel = Hotel(ex_guest=ex_guest, channels=channels, order=16)
            return hotel
        except Exception as exc:
            print(f"{Back.RED}Error: {exc}{Back.RESET}")
            print("Try again!")


def main():
    hotel = initialize_hotel()

    entries = [
        "Check rooms if it is available",
        "Manually check-in guests",
        "Manually check-out guests",
        "Print all rooms with guest",
        "Print all empty rooms",
        "Export as csv",
    ]

    LONGEST_ENTRY = max(map(len, entries))
    LINE_WIDTH = LONGEST_ENTRY + 8
    LEFT_PAD = int((LINE_WIDTH - LONGEST_ENTRY - 2) / 2)

    LINE_SEPERATOR = "="

    while True:
        print(LINE_SEPERATOR * LINE_WIDTH)

        print(f"{'Marnrood Premium':^{LINE_WIDTH}}")
        print()

        for index, entry in enumerate(entries, 1):
            print(f"{' '*LEFT_PAD}{index} {entry}")

        print()
        print(f"{' '*LEFT_PAD}n Initialize new hotel")
        print(f"{' '*LEFT_PAD}q Exit program")

        print(LINE_SEPERATOR * LINE_WIDTH)

        option_string = input("Select an option : ")

        if option_string == "q":
            return
        if option_string == "n":
            hotel = initialize_hotel()
            continue

        try:
            option = int(option_string)
            match option:
                case 1:
                    rooms = map(int, input("Enter room numbers : ").split())
                    for room in rooms:
                        result = hotel.search(room)
                        if result:
                            manual, channels = result
                            print(
                                f"{room} -> Manual check-in: {manual},{','.join(map(str, channels))}"
                            )
                        else:
                            print(f"{room} -> Not Found")
                case 2:
                    amount = int(input("Enter amount of people : "))
                    rooms = hotel.manual_insert(amount)
                    print(f"Checked-in at room : {' '.join(map(str, rooms))}")
                case 3:
                    rooms = map(int, input("Enter room numbers : ").split())
                    for room in rooms:
                        result = hotel.delete(room)
                        if result:
                            print(f"{room} -> Checked-out")
                        else:
                            print(f"{room} -> Not Found")
                case 4:
                    rooms = hotel.get_all_rooms()
                    if rooms is None:
                        print("Empty hotel")
                    else:
                        print("\n".join(map(str, rooms)))
                case 5:
                    rooms = hotel.get_empty_rooms()
                    if rooms is None:
                        print("Empty hotel")
                    elif not rooms:
                        print("Hotel is full up to the last room")
                    else:
                        print("\n".join(map(str, rooms)))
                        print(f'Total empty rooms : {len(rooms)}')
                case 6:
                    filename = input("Enter filename : ")
                    hotel.export_csv(filename)
                case _:
                    raise ValueError("Invalid option")

            input('Press enter to continue')
        except Exception as exc:
            print(f"{Back.RED}Error: {exc}{Back.RESET}")


if __name__ == "__main__":
    main()
else:
    raise SyntaxError
