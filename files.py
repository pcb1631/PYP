import os

#File paths, will be relative to this files.py file and is compatible with all os
ACCOUNTS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "userData", "accounts.json")
ACCOUNTS_LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "accounts.log")