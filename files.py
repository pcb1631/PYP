import os
#File paths, will be relative to this files.py file and is compatible with all os

def path(*args):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), *args)

# examples:
# FILE_PATH = path("folder1", "folder2", "file")
# FILE_PATH = path("file")

ACCOUNTS_PATH = path("userData", "accounts.json")   #userdata/accounts.json
ACCOUNTS_LOG_PATH = path("logs", "accounts.log")    #logs/accounts.log
CHECKIN_LOG_PATH = path("logs", "checkin.log")      #logs/checkin.log
MESSAGES_LOG_PATH = path("logs", "messages.log")    #logs/messages.log
COMMENTS_LOG_PATH = path("logs", "comments.log")
BANNED_PATH = path("banned.txt") 
BOOKING_PATH = path("userData", "booking.json")
ONLINE_PATH  = path("online")