import kb
import shutil
import os
import difflib
from commands import clear  
from colors import RED, WHITE, RESET

def TUI(COLOR=WHITE, prompt="", args=[], verbose=False): # color must be a constant from colors.py, *args should be a string array 
    options = args              
    selection = 0               # user's selection 
    buffer = []                 # what to print after every "refresh"
                                # verbose is Whether to return full string or just number
    '''
    TODO:  search options
    
    '''
    if options == []:
        print(RED + "Error: Options are empty!" + RESET)
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
        start_idx = max(0, min(selection, l - display_count))
        end_idx = min(start_idx + display_count, l)
        
        # Adjust start if we need to show more items at the bottom
        if end_idx - start_idx < display_count:
            start_idx = max(0, end_idx - display_count)
        
        for i in range(start_idx, end_idx):
            if i == selection:
                buffer.append(COLOR + options[i] + RESET)
            else:
                buffer.append(options[i])

        buffer.append(f'query:{query} >{match}')

        print('\n'.join(buffer))
        # get user input
        if os.name == 'nt': # Windows
            while True:
                try:
                    key = kb.get_key()
                    if key != None:
                        break
                    else:
                        continue
                except KeyboardInterrupt:
                    return None

            if key != None:

                if key == b'\xe0': # arrow keys will start with this char
                    key = key + kb.get_key()

                    if key == b'\xe0H' or key == b'\xe0K': # up or left
                        selection = max(0, selection - 1)

                    if key == b'\xe0P' or key == b'\xe0M': # down or right
                        selection = min(l-1, selection + 1)
                
                if key == b'\r': # enter
                    if verbose is True:
                        return options[selection]
                    else:
                        return selection
                    
                if key == b'\x08': # backspace
                    query = query[:-1]
                    if difflib.get_close_matches(query, options, 1):
                        match = difflib.get_close_matches(query, options, n=1, cutoff=0)[0]
                        selection = options.index(match)
                    else:
                        match = ""
                    continue

                if key.isascii() and len(key) == 1:
                    key = key.decode("utf-8") # since its a bytes string, i need to convert to normal str
                    query += key
                    if difflib.get_close_matches(query, options, 1):
                        match = difflib.get_close_matches(query, options, n=1, cutoff = 0)[0]
                        selection = options.index(match)
                    else:
                        match = ""
                    continue

        else: #linux
            key = kb.get_key()

            if key == "\x03": # CTRL+C
                return None
            
            if key == "\x1b[A" or key == "\x1b[D": # UP or LEFT
                selection = max(0, selection - 1)
            
            if key == "\x1b[B" or key == "\x1b[C": # DOWN or RIGHT
                selection = min(l - 1, selection + 1)
            
            if key == "\x1b": # ESC
                return None
            
            if key == "\r": # ENTER
                if verbose is True:
                    return options[selection]
                else:
                    return selection
            
            if key == "\x7f": # BACKSPACE
                query = query[:-1]
                if difflib.get_close_matches(query, options, 1):
                    match = difflib.get_close_matches(query, options, n=1, cutoff=0)[0]
                    selection = options.index(match)
                else:
                    match = ""
                continue
            
            if key.isascii() and len(key) == 1:
                query += key
                if difflib.get_close_matches(query, options, 1):
                    match = difflib.get_close_matches(query, options, n=1, cutoff = 0)[0]
                    selection = options.index(match)
                else:
                    match = ""
                continue
            

# Example usage
options = ["option1", "option2", "option3"]
prompt = "Choose an option: "
verbose = True

selected_option = TUI(WHITE, prompt, options, verbose)