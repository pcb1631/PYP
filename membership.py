import time

from tui import TUI, timeTUI
from colors import *
import files
from utils import *

def transaction_history_self(current_user):
    """
    Shows the transaction history of the current user via TUI

    :param dict current_user: The current user
    """
    options = []

    with open(files.TRANSACTION_PATH, "r") as f:
        transactions = f.read().splitlines()
        for transaction in transactions:
            line = transaction.split(" ")
            if line[0] == "#":
                continue
            if line[1] == current_user["username"]:
                time = epoch_to_readable(float(line[0]))
                options.append(BLUE + time + RESET + " " + GREEN + "RM" + line[2] + RESET)
    while True:
        _ = TUI(BG_PURPLE + BOLD, "Transaction History", options, False)
        if _ is None:
            break

def transaction_history(current_user):
    """
    Shows all transaction history via TUI

    :param dict current_user: The current user
    """
    options = []
    try:
        with open(files.TRANSACTION_PATH, "r") as f:
            transactions = f.read().splitlines()
            for transaction in transactions:
                line = transaction.split(" ")
                if line[0] == "#":
                    continue
                time = epoch_to_readable(float(line[0]))
                options.append(BLUE + time + RESET + " " + line[1] + " " + GREEN + "RM" + line[2] + RESET)
    except FileNotFoundError:
        print(RED + "Transaction history file not found." + RESET)
    except Exception as e:
        print(RED + f"An error occurred while reading the transaction history: {e}" + RESET)
    
    while True:
        _ = TUI(BG_PURPLE + BOLD, "Transaction History", options, False)
        if _ is None:
            break


def buy_membership(current_user):
    """
    Deducts balance from user and changes their membership tier

    :param dict current_user: The current user
    """
    user_data = load_json(files.ACCOUNTS_PATH)

    tier = user_data["users"][current_user["username"]]["membership_tier"]
    if tier is not None:
        print(RED + "You already have a membership" + RESET)
        return

    prices = [150, 250, 100]
    tiers = ["Standard", "Premium", "Student"]
    options = [
        f"Standard - RM{prices[0]}", 
        f"Premium - RM{prices[1]}", 
        f"Student - RM{prices[2]}"
    ]
    tier = TUI(BG_PURPLE + BOLD, "Pick a membership tier", options, False)
    if tier is None:
        return

    balance = user_data["users"][current_user["username"]]["balance - RM"]
    if balance < prices[tier]:
        print(RED + "Insufficient balance. Please top up first." + RESET)
        print("Your current balance: RM" + str(balance))
        return

    print("Your balance after purchase: RM" + str(balance - prices[tier]))
    
    confirm = input(YELLOW + "Proceed payment? (y/n): " + RESET)
    
    if confirm == "y":
        user_data["users"][current_user["username"]]["balance - RM"] -= prices[tier]
        user_data["users"][current_user["username"]]["membership_tier"] = tiers[tier]
        if save_json(files.ACCOUNTS_PATH, user_data, current_user):
            print(GREEN + "Membership has been purchased successfully." + RESET)

        expiretime = time.time() + 30 * 24 * 60 * 60  # one month
        expirytime = load_json(files.EXPIRY_PATH)
        expirytime[current_user["username"]] = expiretime
        if save_json(files.EXPIRY_PATH, expirytime, current_user):
            print(GREEN + "Membership expiry time has been set successfully." + RESET)

        log_entry = f"{epoch_to_readable(time.time())} {current_user['username']} BOUGHT MEMBERSHIP { tiers[tier] }"
        write_line(log_entry, files.ACCOUNTS_LOG_PATH)

        transaction_entry = f"{str(time.time())} {current_user['username']} {prices[tier]}"
        write_line(transaction_entry, files.TRANSACTION_PATH)
    
    
    else:
        print(RED + "Payment cancelled" + RESET)
    return

def upgrade_membership(current_user):
    """
    Upgrades the current user's membership tier

    :param dict current_user: The current user
    """
    user_data = load_json(files.ACCOUNTS_PATH)
    
    tier = user_data["users"][current_user["username"]]["membership_tier"]
    if tier is None:
        print(RED + "You do not have a membership" + RESET)
        return
    
    if tier == "Premium":
        print(RED + "Premium is the highest tier." + RESET)
        return
    
    balance = user_data["users"][current_user["username"]]["balance - RM"]
    if balance < 110:
        print(RED + "Insufficient balance. Please top up first." + RESET)
        print("Your current balance: RM" + str(balance))
        return
    else: 
        print("Your balance after purchase: RM" + str(balance - 110))
    
    confirm = input(YELLOW + "Proceed payment? (y/n): " + RESET)
    if confirm == "y":
        user_data["users"][current_user["username"]]["balance - RM"] -= 110
        user_data["users"][current_user["username"]]["membership_tier"] = "Premium"
        if save_json(files.ACCOUNTS_PATH, user_data, current_user):
            print(GREEN + "Membership has been upgraded successfully." + RESET)
        else:
            print(RED + "Failed to upgrade membership." + RESET)
            return
        
        log_entry = f"{epoch_to_readable(time.time())} {current_user['username']} UPGRADED MEMBERSHIP { tier } TO PREMIUM"
        write_line(log_entry, files.ACCOUNTS_LOG_PATH)
        
        transaction_entry = f"{str(time.time())} {current_user['username']} 110"
        write_line(transaction_entry, files.TRANSACTION_PATH)
        


    


def cancel_membership(current_user):
    """
    Cancels the current user's membership

    :param dict current_user: The current user
    """
    user_data = load_json(files.ACCOUNTS_PATH)
    if "membership_tier" in user_data["users"][current_user["username"]]:
        confirm = input("Cancel membership? (y/n): ")
        if confirm == "y":
            user_data["users"][current_user["username"]]["membership_tier"] = None
            if save_json(files.ACCOUNTS_PATH, user_data, current_user):
                print(GREEN + "Membership cancelled." + RESET)
            else:
                print(RED + "Failed to cancel membership." + RESET)
        else:
            print(RED + "You did not cancel membership" + RESET)
    else:
        print(RED + "You do not have a membership" + RESET)

def top_up_balance(current_user, amount=None):
    """
    Tops up the current user's balance.

    :param current_user: The current user dict
    :param amount: Optional amount to top up, prompts if None
    :type amount: float or None
    """
    user_data = load_json(files.ACCOUNTS_PATH)
    try:
        if amount is None:
            amount = float(input("Enter top up amount (RM): "))
        else:
            amount = float(amount)

        if amount < 0:
            raise ValueError("Invalid amount. Please enter a positive amount.")
    except ValueError as e:
        raise e

    user_data["users"][current_user["username"]]["balance - RM"] += amount
    balance = user_data["users"][current_user["username"]]["balance - RM"]
        
    if save_json(files.ACCOUNTS_PATH, user_data, current_user):
        print(GREEN + f"Top up successful. New balance: RM{balance}." + RESET)
    else:
        print(RED + "Failed to top up balance." + RESET)
        
def fd_top_up(current_user, username=None, amount=None):
    """
    Tops up a member's balance as front desk.

    :param current_user: The current user dict
    :param username: Optional member username, prompts if None
    :type username: str or None
    :param amount: Optional amount to top up, prompts if None
    :type amount: float or None
    """
    user_data = load_json(files.ACCOUNTS_PATH)
        
    members = []
    for user in user_data["users"]:
        if user_data["users"][user]["user_type"] == "Member":
            members.append(user)
    if username is None:
        username = TUI(BG_RED, "Select user to edit", members, verbose=True)
    
    if username not in user_data["users"]:
        print("User does not exist")
        return
    
    try:
        if amount is None:
            amount = float(input("Enter top up amount (RM): "))
        else:
            amount = float(amount)

        if amount < 0:
            raise ValueError("Invalid amount. Please enter a positive amount.")
    except ValueError as e:
        raise e

    user_data["users"][username]["balance - RM"] += amount
    balance = user_data["users"][username]["balance - RM"]
        
    if save_json(files.ACCOUNTS_PATH, user_data, current_user):
        print(GREEN + f"Top up successful. New balance: RM{balance}." + RESET)
        print("Current time: " + epoch_to_readable(time.time()))
        print("User: " + username)
        print("Amount: " + str(amount))
        print("By employee " + BLUE + current_user["username"] + RESET)
    else:
        print(RED + "Failed to top up balance." + RESET)
        
def generate_report(current_user):
    """
    Shows all transactions and total money collected in a given time range

    :param dict current_user: The current user
    """
    transactions = []
    
    try:
        with open(files.TRANSACTION_PATH, "r") as f:
            lines = f.read().splitlines()
            for line in lines:
                line = line.split(" ")
                if line[0] == "#":
                    continue
                transactions.append(line)
    except FileNotFoundError:
        print(RED + "Transaction file not found." + RESET)
        return
    except Exception as e:
        print(RED + f"Error reading transaction file: {e}" + RESET)
        return
    
    options = ["1. Report for the past month", "2. Manually define time"]
    selection = TUI(BG_RED, "Select report type", options, verbose=False)


    start = 0.0
    end = 0.0

    if selection == 0:
        start = time.time() - 30 * 24 * 60 * 60
        end = time.time()

    elif selection == 1:
        start = timeTUI(prompt="Pick start time", username = "")
        end = timeTUI(prompt="Pick end time", username = "")
        
        if start is None or end is None: # if user presses CTRL+C
            return

    report = []
    total = 0.0
    for line in transactions:
        if float(line[0]) >= start and float(line[0]) <= end:
            date = epoch_to_readable(float(line[0]))
            report.append(f"{BLUE}Time: {date}{RESET} User: {line[1]} Amount: {GREEN}{line[2]}{RESET}")
            total += float(line[2])
    
    print("\n")
    print("\n".join(report))
    print(f"Total: {total}")