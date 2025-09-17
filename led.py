import sys
from os.path import isfile
from typing import List
from globals import GLOBALS
from base_events import handle_base_events, initBuffers, get_max_digit_number, getch
from ui import clear, render
from modules import handle_modules

def openFile(filename: str):
    if not isfile(filename):
        open(filename,"w").close()

    GLOBALS["FILENAME"]=filename
    with open(filename,"r") as f:
        GLOBALS["BUFFER"] = f.read().split("\n")
    GLOBALS["LINE_LENGTH"] = len(GLOBALS["BUFFER"][GLOBALS["LINE_INDEX"]])
    GLOBALS["NEW_LINE_LENGTH"] = GLOBALS["LINE_LENGTH"]
    GLOBALS["NUMBER_OF_DIGITS"] = get_max_digit_number(len(GLOBALS["BUFFER"]))
    GLOBALS["IS_FILE_SAVED"] = True
    GLOBALS["COLUMN_INDEX"] = [0] * len(GLOBALS["BUFFER"])
    initBuffers()

def init(filename: str):
    openFile(filename)

def main(argv: List[str]):
    if len(argv) > 1:   init(argv[1])
    else:   init("newfile")
    
    clear()
    render()
    
    run = True

    while run:
        char = getch()

        override = handle_modules(char)
        
        if not override:
            run = handle_base_events(char)
        
        render()
        GLOBALS["LINE_LENGTH"] = GLOBALS["NEW_LINE_LENGTH"]
    clear()

if __name__ == "__main__":
    main(sys.argv)