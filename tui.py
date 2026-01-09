import kb
import shutil
import os
import difflib
from datetime import datetime, timedelta
import calendar
import time
from colors import *
from utils import conflict
import files

if os.name == 'nt':
    keymap = {
        b"\r": "enter",
        b"\xe0H": "up",
        b"\xe0P": "down",
        b"\xe0K": "left",
        b"\xe0M": "right",
        b"\x08": "backspace"
    }
else:
    keymap = {
        "\r": "enter",
        "\x1b[A": "up",
        "\x1b[B": "down",
        "\x1b[C": "right",
        "\x1b[D": "left",
        "\x7f": "backspace"
    }

def clear():                    # clear console
    """
    Clears the console
    """
    if os.name == 'nt':         # For Windows
        _ = os.system('cls')
    else:                       # For macOS and Linux
        _ = os.system('clear')  # _ means idgaf about the return value

def TUI(COLOR=BG_MAGENTA, prompt="", args=[], verbose=False, idx=0): # color must be a constant from colors.py, *args should be a string array 
    """
    Simple option selector TUI 
    
    :param COLOR: What to highlight the selection with
    :type COLOR: str
    :param prompt: Prompt to display on top
    :type prompt: str
    :param args: List of options
    :type args: list[str]
    :param verbose: Whether to return string or index
    :type verbose: bool
    :param idx: Starting index, if TUI() is run in a while loop and index persistence is needed
    :type idx: int
    :return: index of user selection if verbose is False, string of user selection if verbose is True, None if user pressed CTRL + C
    :rtype: int or str or None
    """
    options = args              
    selection = idx               # user's selection 
    buffer = []                 # what to print after every "refresh"
                                # verbose is Whether to return full string or just number
    if options == []:
        print(RED + "Error: Options are empty!" + RESET)
        time.sleep(1)
        return None
    
    l = len(options)

    query = ""
    match = ""

    while True:
        # get terminal size
        if os.name == 'nt': # Windows
            cols, lines = shutil.get_terminal_size()
        else: # Linux and macOS
            cols, lines = shutil.get_terminal_size()
        
        clear()
        key = ""
        buffer = []

        buffer.append(prompt)

        # Calculate display range
        display_count = min(lines - 3, l)  # Leave 2 lines for prompt, 1 line for query
        start_idx = min(selection, l - display_count)
        end_idx = min(start_idx + display_count, l)
        
        for i in range(start_idx, end_idx):
            if i == selection:
                buffer.append(COLOR + options[i] + RESET)
            else:
                buffer.append(options[i])

        buffer.append(f'query:{query} >{match}')

        print('\n'.join(buffer))
        
        key = kb.get_key()
        
        if os.name == 'nt':
            if key == b'\x03':
                return None
        else:
            if key == "\x03": # CTRL + C 
                return None
        
        if key in keymap:
            key = keymap[key]

        match key:
            case "up":
                selection = (selection - 1) % l
            case "down":
                selection = (selection + 1) % l
            case "enter":
                if verbose is True:
                    return options[selection]
                else:
                    return selection
            case "backspace":
                query = query[:-1]
                if difflib.get_close_matches(query, options, 1):
                    match = difflib.get_close_matches(query, options, n=1, cutoff=0)[0]
                    selection = options.index(match)
                else:
                    match = ""
                continue
            case _ if key.isascii() and len(key) == 1:
                if os.name == "nt":
                    key = key.decode('utf-8')

                query += key
                if difflib.get_close_matches(query, options, 1):
                    match = difflib.get_close_matches(query, options, n=1, cutoff=0)[0]
                    selection = options.index(match)
                else:
                    match = ""
                continue

def timeTUI(timestamp=int(datetime.now().timestamp()), prompt="", username=""):
    """
    TUI to pick a certain time

    Because nobody wants to manually type dd mm yy or UNIX timestamp.

    :param int timestamp: The timestamp to start from
    :param str prompt: The prompt to display
    :param str username: The username to check for time slot conflicts
    :return: The selected time in UNIX timestamp / Epoch
    :rtype: int
    """
    selection = 0
    
    date_time = datetime.fromtimestamp(timestamp)
    
    while True:
        timestamp = date_time.timestamp()

        time = [date_time.day, date_time.month, date_time.year, date_time.hour, date_time.minute] # for displaying only
        clear()
        buffer = []
        buffer.append(prompt+"\n")

        for i in range(5):
            if i == selection:
                buffer.append(BG_MAGENTA + str(time[i]) + RESET + " ")
            else:
                buffer.append(str(time[i]) + " ")
        
        conflict_slot = conflict(username, timestamp)
        if conflict_slot is not None:
            buffer.append("\n")
            buffer.append(f"{RED}In conflict with slot: {conflict_slot}{RESET}")

        print(''.join(buffer))
        
        key = kb.get_key()
        
        if os.name == 'nt':
            if key == b'\x03':
                return None
        else:
            if key == "\x03": # CTRL + C 
                return None

        if key in keymap:
            key = keymap[key]
    
        mod = 0

        match key:
            case "left":
                selection = (selection - 1) % 5
            case "right":
                selection = (selection + 1) % 5
            case "up":
                mod = 1
            case "down":
                mod = -1
            case "enter":
                timestamp = date_time.timestamp()
                return timestamp

        match selection: # because im worried about leap years and months with different days
            case 0:
                date_time += timedelta(days=mod)
            case 1:
                date_time += timedelta(days=calendar.monthrange(date_time.year, date_time.month)[1] * mod)
            case 2:
                date_time += timedelta(days=365 * mod)
            case 3:
                date_time += timedelta(hours=mod)
            case 4:
                date_time += timedelta(minutes=mod)
