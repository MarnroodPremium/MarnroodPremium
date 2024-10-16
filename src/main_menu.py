from os import get_terminal_size

def main_menu():
    line_width = get_terminal_size().columns

    LINE_SEPERATOR = '='

    print(LINE_SEPERATOR * line_width)
    print(f'{'Marnrood Premium':^{line_width}}')
    print(LINE_SEPERATOR * line_width)

    