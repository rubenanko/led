from globals import GLOBALS
from base_events import get_max_digit_number
from os import get_terminal_size

def clear():
    print("\x1b[2J",end="",flush=True)

def render():
    colmuns_number = get_terminal_size().columns
    save_status_char = "\x1b[1;32m~\x1b[0;0m" if GLOBALS["IS_FILE_SAVED"] else "\x1b[1;35m~\x1b[0;0m"
    current_digit_number = get_max_digit_number(GLOBALS["LINE_INDEX"]+1)
    cursor_coordinates = f'\x1b[{1 + (GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]]) // colmuns_number};{1 + (GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]] + GLOBALS["NUMBER_OF_DIGITS"] + 3) % colmuns_number}f'
    print(f'\x1b[1;1f\x1b[0;33m{GLOBALS["LINE_INDEX"]+1}\x1b[0;0m{" " * (GLOBALS["NUMBER_OF_DIGITS"] - current_digit_number)} {save_status_char} {GLOBALS["LINE_BUFFER_LEFT"]}{GLOBALS["LINE_BUFFER_RIGHT"]}{" " * (GLOBALS["LINE_LENGTH"] - len(GLOBALS["LINE_BUFFER_LEFT"]) + len(GLOBALS["LINE_BUFFER_RIGHT"]))}{cursor_coordinates}',end="",flush=True)