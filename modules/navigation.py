import sys, os
sys.path.append(os.path.abspath(os.path.join(__file__,"../..")))

from base_events import initBuffers, handle_left_arrow, handle_right_arrow, handle_top_arrow, handle_bottom_arrow, handle_ctrl_left_arrow, handle_ctrl_right_arrow
from globals import GLOBALS

def entrypoint(char: bytes)->bool:
    if char == GLOBALS["CTRL_W_KEY"]:
        if len(GLOBALS["LINE_BUFFER_RIGHT"]):
            jump = 1
            while jump < (len(GLOBALS["LINE_BUFFER_RIGHT"])-1) and GLOBALS["LINE_BUFFER_RIGHT"][jump-1] != "(" and GLOBALS["LINE_BUFFER_RIGHT"][jump] != ")":
                jump += 1

            if GLOBALS["LINE_BUFFER_RIGHT"][jump-1] == "(" or GLOBALS["LINE_BUFFER_RIGHT"][jump] == ")":
                GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]] += jump
                initBuffers()
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