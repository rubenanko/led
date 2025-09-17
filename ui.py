from globals import GLOBALS
from base_events import get_max_digit_number
from sys import platform
from os import get_terminal_size,system
from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import TerminalFormatter

def clear():
    system("clear")

def enter_fullscreen():
    print("\x1b[?1049h",end="",flush=True)

def exit_fullscreen():
    print("\x1b[?1049l",end="",flush=True)

def fill_line(strlen:int,columns_number:int):
    return " " * (columns_number - (strlen % columns_number))

def render(updateBuffer:bool = True):
    columns_number = get_terminal_size().columns
    lines_number = get_terminal_size().lines
    save_status_char = "\x1b[1;32m~\x1b[0;0m" if GLOBALS["IS_FILE_SAVED"] else "\x1b[1;35m~\x1b[0;0m"
    current_digit_number = get_max_digit_number(GLOBALS["LINE_INDEX"]+1)
    cursor_coordinates = f'\x1b[{1 + (GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]]) // columns_number};{1 + (GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]] + GLOBALS["NUMBER_OF_DIGITS"] + 3) % columns_number}f'
    highlighted_buffer = highlight(GLOBALS["LINE_BUFFER_LEFT"] + GLOBALS["LINE_BUFFER_RIGHT"],GLOBALS["LEXER"],TerminalFormatter())[:-1]

    inf = max(0,GLOBALS["LINE_INDEX"]-(lines_number//3))
    sup = min(len(GLOBALS["BUFFER"]),GLOBALS["LINE_INDEX"]+(lines_number//3))
    # top_file_buffer = "\n".join(GLOBALS["BUFFER"][inf:GLOBALS["LINE_INDEX"]])
    # bottom_file_buffer = "\n".join(GLOBALS["BUFFER"][GLOBALS["LINE_INDEX"]+1:sup])

    top_file_buffer = ""
    for index in range(inf,GLOBALS["LINE_INDEX"]):
        top_file_buffer += f'\x1b[0;33m{index+1}\x1b[0;0m{" " * (GLOBALS["NUMBER_OF_DIGITS"] - get_max_digit_number(index+1))}\x1b[1;34m ~\x1b[0;0m {highlight(GLOBALS["BUFFER"][index],GLOBALS["LEXER"],TerminalFormatter())[:-1]}{fill_line(len(GLOBALS["BUFFER"][index])+ 3 + GLOBALS["NUMBER_OF_DIGITS"],columns_number)}\n'
            
    bottom_file_buffer = ""
    for index in range(GLOBALS["LINE_INDEX"]+1,sup):
        bottom_file_buffer += f'\x1b[0;33m{index+1}\x1b[0;0m{" " * (GLOBALS["NUMBER_OF_DIGITS"] - get_max_digit_number(index+1))}\x1b[1;34m ~\x1b[0;0m {highlight(GLOBALS["BUFFER"][index],GLOBALS["LEXER"],TerminalFormatter())[:-1]}{fill_line(len(GLOBALS["BUFFER"][index])+ 3 + GLOBALS["NUMBER_OF_DIGITS"],columns_number)}\n'

    file_highlighted_buffer = f'{top_file_buffer if len(top_file_buffer) > 0 else ""}\x1b[1;31m{GLOBALS["LINE_INDEX"]+1}{" " * (GLOBALS["NUMBER_OF_DIGITS"] - get_max_digit_number(GLOBALS["LINE_INDEX"]+1))} > \x1b[7;39m{GLOBALS["BUFFER"][GLOBALS["LINE_INDEX"]]}{fill_line(len(GLOBALS["BUFFER"][GLOBALS["LINE_INDEX"]])+ 3 + GLOBALS["NUMBER_OF_DIGITS"],columns_number)}\n{bottom_file_buffer}'

    print(f'\x1b[1;1f\x1b[0;33m{GLOBALS["LINE_INDEX"]+1}\x1b[0;0m{" " * (GLOBALS["NUMBER_OF_DIGITS"] - current_digit_number)} {save_status_char} {highlighted_buffer}{" " * ((columns_number - 5 - len(GLOBALS["LINE_BUFFER_LEFT"] + GLOBALS["LINE_BUFFER_RIGHT"])) % columns_number)}\n{"-"*columns_number}\n{file_highlighted_buffer}{cursor_coordinates}',end="",flush=True)