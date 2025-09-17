import sys
from os.path import isfile
from typing import List
from globals import GLOBALS
from base_events import handle_base_events, initBuffers, get_max_digit_number, getch
from ui import clear, render,enter_fullscreen,exit_fullscreen
from modules import handle_modules

from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import TerminalFormatter

def openFile(filename: str,line_index: int = 0):
    if not isfile(filename):
        open(filename,"w").close()

    GLOBALS["FILENAME"]=filename
    with open(filename,"r") as f:
        GLOBALS["BUFFER"] = f.read().split("\n")

    GLOBALS["LINE_INDEX"] = line_index
    GLOBALS["NUMBER_OF_DIGITS"] = get_max_digit_number(len(GLOBALS["BUFFER"]))
    GLOBALS["IS_FILE_SAVED"] = True

    GLOBALS["COLUMN_INDEX"] = []
    for line in GLOBALS["BUFFER"]:
        GLOBALS["COLUMN_INDEX"].append(len(line))

    GLOBALS["LEXER"] = get_lexer_for_filename(filename)
    initBuffers()

def init(argv: List[str]):
    if len(argv) > 1:   filename = argv[1]
    else:   filename = "newfile"

    if len(argv) > 2:   line_index = max(0,int(argv[2])-1)
    else:   line_index = 0

    openFile(filename,line_index)

def main(argv: List[str]):
    init(argv)
    
    enter_fullscreen()

    render()
    
    run = True

    while run:
        char = getch()

        override = handle_modules(char)
        
        if not override:
            run = handle_base_events(char)
        
        render()
    
    exit_fullscreen()
    # if GLOBALS["IS_FILE_SAVED"]:
    #     print(highlight("\n".join(GLOBALS["BUFFER"]),GLOBALS["LEXER"],TerminalFormatter()))

if __name__ == "__main__":
    main(sys.argv)