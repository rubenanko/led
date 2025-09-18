import sys, os
sys.path.append(os.path.abspath(os.path.join(__file__,"../..")))

from base_events import handle_left_arrow, handle_right_arrow, handle_top_arrow, handle_bottom_arrow, handle_ctrl_left_arrow, handle_ctrl_right_arrow, handle_begining_key
from globals import GLOBALS

OPENING_BRACKETS = ["(","[","{","'",'"']
CLOSING_BRACKETS = [")","]","}","'",'"']

def entrypoint(char: bytes)->bool:
    if char == GLOBALS["CTRL_W_KEY"]:
        if len(GLOBALS["LINE_BUFFER_RIGHT"]):
            jump = 1
            while jump < (len(GLOBALS["LINE_BUFFER_RIGHT"])-1) and (not GLOBALS["LINE_BUFFER_RIGHT"][jump-1] in OPENING_BRACKETS) and (not GLOBALS["LINE_BUFFER_RIGHT"][jump] in CLOSING_BRACKETS):
                jump += 1



            # if jump < (len(GLOBALS["LINE_BUFFER_RIGHT"])) and GLOBALS["LINE_BUFFER_RIGHT"][jump-1] in OPENING_BRACKETS or GLOBALS["LINE_BUFFER_RIGHT"][jump] in CLOSING_BRACKETS:
            if jump < (len(GLOBALS["LINE_BUFFER_RIGHT"])):
                GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]] += jump
                GLOBALS["LINE_BUFFER_LEFT"] += GLOBALS["LINE_BUFFER_RIGHT"][:jump]
                GLOBALS["LINE_BUFFER_RIGHT"] = GLOBALS["LINE_BUFFER_RIGHT"][jump:]
        else:
            handle_begining_key()
            entrypoint(char)
        return True
    elif char == GLOBALS["CTRL_K_KEY"]:
        handle_left_arrow()
        return True
    elif char == GLOBALS["CTRL_P_KEY"]:
        handle_right_arrow()
        return True
    elif char == GLOBALS["CTRL_L_KEY"]:
        handle_bottom_arrow()
        return True
    elif char == GLOBALS["CTRL_O_KEY"]:
        handle_top_arrow()
        return True
    elif char == GLOBALS["CTRL_Q_KEY"]:
        handle_ctrl_left_arrow()
        return True
    elif char == GLOBALS["CTRL_D_KEY"]:
        handle_ctrl_right_arrow()
        return True