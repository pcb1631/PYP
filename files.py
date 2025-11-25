import os
#File paths, will be relative to this files.py file and is compatible with all os

def path(*args):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), *args)

ACCOUNTS_PATH = path("userData", "accounts.json")   #userdata/accounts.json
ACCOUNTS_LOG_PATH = path("logs", "accounts.log")    #logs/accounts.log
CHECKIN_LOG_PATH = path("logs", "checkin.log")      #logs/checkin.log

pass