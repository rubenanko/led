import sys, os

sys.path.append(os.path.abspath(os.path.join(__file__,"../..")))


from base_events import initBuffers,get_max_digit_number
from globals import GLOBALS

def entrypoint(char: bytes)->bool:
    if char == GLOBALS["CTRL_C_KEY"]:
        GLOBALS["PAPERCLIP"] = GLOBALS["LINE_BUFFER_LEFT"] + GLOBALS["LINE_BUFFER_RIGHT"]
        return True

    elif char == GLOBALS["CTRL_X_KEY"]:
        GLOBALS["PAPERCLIP"] = GLOBALS["LINE_BUFFER_LEFT"] + GLOBALS["LINE_BUFFER_RIGHT"]
        GLOBALS["COLUMN_INDEX"].pop(GLOBALS["LINE_INDEX"])
        GLOBALS["BUFFER"].pop(GLOBALS["LINE_INDEX"])
        initBuffers()
        GLOBALS["NUMBER_OF_DIGITS"] = get_max_digit_number(len(GLOBALS["BUFFER"]))   
        GLOBALS["IS_FILE_SAVED"] = False
        return True

    elif char == GLOBALS["CTRL_V_KEY"]:
        new_line_buffer = GLOBALS["PAPERCLIP"]
        GLOBALS["COLUMN_INDEX"].insert(GLOBALS["LINE_INDEX"],len(new_line_buffer))
        GLOBALS["BUFFER"].insert(GLOBALS["LINE_INDEX"],new_line_buffer)
        initBuffers()
        GLOBALS["NUMBER_OF_DIGITS"] = get_max_digit_number(len(GLOBALS["BUFFER"]))
        GLOBALS["IS_FILE_SAVED"] = False
        return True
    else:   return False