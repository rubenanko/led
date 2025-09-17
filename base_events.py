import sys
from globals import GLOBALS

if sys.platform == "win32":
    import msvcrt
else:
    import termios, tty

def initBuffers():
    GLOBALS["LINE_BUFFER_LEFT"] = GLOBALS["BUFFER"][GLOBALS["LINE_INDEX"]][:GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]]]
    GLOBALS["LINE_BUFFER_RIGHT"] = GLOBALS["BUFFER"][GLOBALS["LINE_INDEX"]][GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]]:] 


def get_max_digit_number(integer: int)->int:
    if integer < 10:  return 1
    elif integer < 100:   return 2
    elif integer < 1000:   return 3
    elif integer < 10000:   return 4
    elif integer < 100000:   return 5
    elif integer < 1000000:   return 6
    elif integer < 10000000:   return 7
    elif integer < 100000000:   return 8
    elif integer < 1000000000:   return 9
    else:   return None

def getch(nb_chars_to_read: int = 1):
    if sys.platform == "win23":
        buffer = b""
        for i in range(nb_chars_to_read):
            buffer += msvcrt.getch()
        return buffer
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)  # mode raw = touche par touche
            ch = sys.stdin.read(nb_chars_to_read)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch.encode()


def handle_left_arrow():
    if GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]] > 0:
        GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]] -= 1
        GLOBALS["LINE_BUFFER_RIGHT"] = GLOBALS["LINE_BUFFER_LEFT"][-1] + GLOBALS["LINE_BUFFER_RIGHT"]
        GLOBALS["LINE_BUFFER_LEFT"] = GLOBALS["LINE_BUFFER_LEFT"][:-1]

def handle_right_arrow():
    if GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]] < len(GLOBALS["LINE_BUFFER_LEFT"] + GLOBALS["LINE_BUFFER_RIGHT"]):
        GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]] += 1
        GLOBALS["LINE_BUFFER_LEFT"] += GLOBALS["LINE_BUFFER_RIGHT"][0]
        GLOBALS["LINE_BUFFER_RIGHT"] = GLOBALS["LINE_BUFFER_RIGHT"][1:]

def handle_bottom_arrow():
    if GLOBALS["LINE_INDEX"] < len(GLOBALS["BUFFER"])-1:
        GLOBALS["BUFFER"][GLOBALS["LINE_INDEX"]] = GLOBALS["LINE_BUFFER_LEFT"] + GLOBALS["LINE_BUFFER_RIGHT"]
        GLOBALS["LINE_INDEX"] += 1
        if GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]] > len(GLOBALS["BUFFER"][GLOBALS["LINE_INDEX"]]):
            GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]] = len(GLOBALS["BUFFER"][GLOBALS["LINE_INDEX"]])
        GLOBALS["NEW_LINE_LENGTH"] = len(GLOBALS["BUFFER"][GLOBALS["LINE_INDEX"]])
        initBuffers()

def handle_top_arrow():
    if GLOBALS["LINE_INDEX"] > 0:
        GLOBALS["BUFFER"][GLOBALS["LINE_INDEX"]] = GLOBALS["LINE_BUFFER_LEFT"] + GLOBALS["LINE_BUFFER_RIGHT"]
        GLOBALS["LINE_INDEX"] -= 1
        if GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]] > len(GLOBALS["BUFFER"][GLOBALS["LINE_INDEX"]]):
            GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]] = len(GLOBALS["BUFFER"][GLOBALS["LINE_INDEX"]])
        GLOBALS["NEW_LINE_LENGTH"] = len(GLOBALS["BUFFER"][GLOBALS["LINE_INDEX"]])
        initBuffers()

def handle_ctrl_left_arrow():
    if GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]] > 0:
        if not GLOBALS["LINE_BUFFER_LEFT"][-1].isalnum():
            while GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]] > 0 and not GLOBALS["LINE_BUFFER_LEFT"][-1].isalnum():
                GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]] -= 1
                GLOBALS["LINE_BUFFER_RIGHT"] = GLOBALS["LINE_BUFFER_LEFT"][-1] + GLOBALS["LINE_BUFFER_RIGHT"]
                GLOBALS["LINE_BUFFER_LEFT"] = GLOBALS["LINE_BUFFER_LEFT"][:-1]
        else:
            while GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]] > 0 and GLOBALS["LINE_BUFFER_LEFT"][-1].isalnum():
                GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]] -= 1
                GLOBALS["LINE_BUFFER_RIGHT"] = GLOBALS["LINE_BUFFER_LEFT"][-1] + GLOBALS["LINE_BUFFER_RIGHT"]
                GLOBALS["LINE_BUFFER_LEFT"] = GLOBALS["LINE_BUFFER_LEFT"][:-1]

def handle_ctrl_right_arrow():
    if GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]] < len(GLOBALS["LINE_BUFFER_LEFT"] + GLOBALS["LINE_BUFFER_RIGHT"]):
        if not GLOBALS["LINE_BUFFER_RIGHT"][0].isalnum():
            while GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]] < len(GLOBALS["LINE_BUFFER_LEFT"] + GLOBALS["LINE_BUFFER_RIGHT"]) and not GLOBALS["LINE_BUFFER_RIGHT"][0].isalnum():
                GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]] += 1
                GLOBALS["LINE_BUFFER_LEFT"] += GLOBALS["LINE_BUFFER_RIGHT"][0]
                GLOBALS["LINE_BUFFER_RIGHT"] = GLOBALS["LINE_BUFFER_RIGHT"][1:]                      
        else:
            while GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]] < len(GLOBALS["LINE_BUFFER_LEFT"] + GLOBALS["LINE_BUFFER_RIGHT"]) and GLOBALS["LINE_BUFFER_RIGHT"][0].isalnum():
                GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]] += 1
                GLOBALS["LINE_BUFFER_LEFT"] += GLOBALS["LINE_BUFFER_RIGHT"][0]
                GLOBALS["LINE_BUFFER_RIGHT"] = GLOBALS["LINE_BUFFER_RIGHT"][1:]

def handle_begining_key():
    GLOBALS["LINE_BUFFER_RIGHT"] = GLOBALS["LINE_BUFFER_LEFT"] + GLOBALS["LINE_BUFFER_RIGHT"]
    GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]] -= len(GLOBALS["LINE_BUFFER_LEFT"])
    GLOBALS["LINE_BUFFER_LEFT"] = ""

def handle_end_key():
    GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]] += len(GLOBALS["LINE_BUFFER_RIGHT"])
    GLOBALS["LINE_BUFFER_LEFT"] += GLOBALS["LINE_BUFFER_RIGHT"]
    GLOBALS["LINE_BUFFER_RIGHT"] = ""

def handle_base_events(char: chr)->bool:
        GLOBALS["NEW_LINE_LENGTH"] = GLOBALS["LINE_LENGTH"]
        
        if char == GLOBALS["ESCAPE_KEY"]:
            if sys.platform == "win":   return False
            else:
                char = getch()
                if char == GLOBALS["ESCAPE_KEY"]: return False
                elif char == b"[":
                    char_decoded = getch().decode()
                    if char_decoded == GLOBALS["LINUX_RIGHT_ARROW_KEY"]:
                        handle_right_arrow()

                    elif char_decoded == GLOBALS["LINUX_LEFT_ARROW_KEY"]:
                        handle_left_arrow()

                    elif char_decoded == GLOBALS["LINUX_BOTTOM_ARROW_KEY"]: #bottom arrow
                        handle_bottom_arrow()

                    elif char_decoded == GLOBALS["LINUX_TOP_ARROW_KEY"]:
                        handle_top_arrow()

                    elif char_decoded == GLOBALS["LINUX_BEGINING_KEY"]:
                        handle_begining_key()

                    elif char_decoded == GLOBALS["LINUX_END_KEY"]:
                        handle_end_key()

                    elif char_decoded == "1":
                        char_decoded = getch(3).decode()
                        if char_decoded == GLOBALS["LINUX_CTRL_RIGHT_ARROW_KEY"]:
                            handle_ctrl_right_arrow()

                        elif char_decoded == GLOBALS["LINUX_CTRL_LEFT_ARROW_KEY"]:
                            handle_ctrl_left_arrow()

        #arrows require a special treatment
        elif char == GLOBALS["WIN_CURSOR_KEY"]:
            char_decoded = getch().decode()

            if char_decoded == GLOBALS["WIN_RIGHT_ARROW_KEY"]:
                handle_right_arrow()

            elif char_decoded == GLOBALS["WIN_LEFT_ARROW_KEY"]:
                handle_left_arrow()

            elif char_decoded == GLOBALS["WIN_BOTTOM_ARROW_KEY"]: #bottom arrow
                handle_bottom_arrow()

            elif char_decoded == GLOBALS["WIN_TOP_ARROW_KEY"]:
                handle_top_arrow()

            elif char_decoded == GLOBALS["WIN_BEGINING_KEY"]:
                handle_begining_key()

            elif char_decoded == GLOBALS["WIN_END_KEY"]:
                handle_end_key()

            elif char_decoded == GLOBALS["WIN_CTRL_RIGHT_ARROW_KEY"]:
                handle_ctrl_right_arrow()

            elif char_decoded == GLOBALS["WIN_CTRL_LEFT_ARROW_KEY"]:
                handle_ctrl_left_arrow()
                            
        elif char == GLOBALS["WIN_DELETE_KEY"] or char == GLOBALS["LINUX_DELETE_KEY"]: #delete
            if GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]] == 0:
                if GLOBALS["LINE_INDEX"] != 0:
                    GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]-1] = len(GLOBALS["BUFFER"][GLOBALS["LINE_INDEX"]-1])
                    GLOBALS["BUFFER"][GLOBALS["LINE_INDEX"]-1] += GLOBALS["LINE_BUFFER_RIGHT"]
                    GLOBALS["BUFFER"].pop(GLOBALS["LINE_INDEX"])
                    GLOBALS["COLUMN_INDEX"].pop(GLOBALS["LINE_INDEX"])
                    GLOBALS["LINE_INDEX"] -= 1
                    GLOBALS["NEW_LINE_LENGTH"] = len(GLOBALS["BUFFER"][GLOBALS["LINE_INDEX"]])
                    initBuffers()
                    GLOBALS["NUMBER_OF_DIGITS"] = get_max_digit_number(len(GLOBALS["BUFFER"]))   
                    GLOBALS["IS_FILE_SAVED"] = False
            else:
                GLOBALS["LINE_BUFFER_LEFT"] = GLOBALS["LINE_BUFFER_LEFT"][:-1]
                GLOBALS["NEW_LINE_LENGTH"] -= 1
                GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]] -= 1
                GLOBALS["IS_FILE_SAVED"] = False

        elif char == GLOBALS["NEWLINE_KEY"]: #newline
            GLOBALS["COLUMN_INDEX"].insert(GLOBALS["LINE_INDEX"]+1,0)
            GLOBALS["BUFFER"][GLOBALS["LINE_INDEX"]] = GLOBALS["LINE_BUFFER_LEFT"]
            GLOBALS["BUFFER"].insert(GLOBALS["LINE_INDEX"]+1,GLOBALS["LINE_BUFFER_RIGHT"])
            GLOBALS["LINE_INDEX"] += 1
            GLOBALS["NEW_LINE_LENGTH"] = len(GLOBALS["BUFFER"][GLOBALS["LINE_INDEX"]])
            initBuffers()
            GLOBALS["NUMBER_OF_DIGITS"] = get_max_digit_number(len(GLOBALS["BUFFER"]))
            GLOBALS["IS_FILE_SAVED"] = False

        elif char == GLOBALS["SAVE_KEY"]:
            GLOBALS["BUFFER"][GLOBALS["LINE_INDEX"]] = GLOBALS["LINE_BUFFER_LEFT"] + GLOBALS["LINE_BUFFER_RIGHT"]
            with open(GLOBALS["FILENAME"],"w") as f:
                f.write("\n".join(GLOBALS["BUFFER"]))
            GLOBALS["IS_FILE_SAVED"] = True

        elif char == GLOBALS["TAB_KEY"]:
            GLOBALS["LINE_BUFFER_LEFT"] += "    "
            GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]] += 4
            GLOBALS["NEW_LINE_LENGTH"] += 4
            GLOBALS["IS_FILE_SAVED"] = False
        else:
            GLOBALS["LINE_BUFFER_LEFT"] += char.decode("cp437","replace")
            GLOBALS["COLUMN_INDEX"][GLOBALS["LINE_INDEX"]] += 1
            GLOBALS["NEW_LINE_LENGTH"] += 1
            GLOBALS["IS_FILE_SAVED"] = False
        return True