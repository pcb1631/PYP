import time

from tui import TUI
from colors import *
import files
from utils import *

def transaction_history_self(current_user):
    options = []

    with open(files.TRANSACTION_PATH, "r") as f:
        transactions = f.read().splitlines()
        for transaction in transactions:
            line = transaction.split(" ")
            if line[1] == "#":
                continue
            if line[1] == current_user["username"]:
                time = epoch_to_readable(float(line[0]))
                options.append(f"{BLUE}{time}{RESET} {GREEN}RM{line[2]}{RESET}")
    while True:
        _ = TUI(BG_PURPLE + BOLD, "Transaction History", options, False)
        if _ is None:
            break


def membership_renewal(current_user):
    pass

def buy_membership(current_user):
    user_data = load_json(files.ACCOUNTS_PATH)
    if user_data is None:
        return

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
    user_data = load_json(files.ACCOUNTS_PATH)
    if user_data is None:
        return
    
    tier = user_data["users"][current_user["username"]]["membership_tier"]
    if tier is None:
        print(RED + "You do not have a membership" + RESET)
        return
    
    if tier == "Student":
        pass
    elif tier == "Standard":
        pass
    elif tier == "Premium":
        print(RED + "You are already upgraded to Premium." + RESET)

def cancel_membership(current_user):
    user_data = load_json(files.ACCOUNTS_PATH)
    if user_data is None:
        return
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
    user_data = load_json(files.ACCOUNTS_PATH)
    if user_data is None:
        return
    try:
        if amount is None:
            amount = float(input("Enter top up amount (RM): "))
        else:
            amount = float(amount)

        if amount < 0:
            print(RED + "Invalid amount. Please enter a positive amount." + RESET)
            return
    except ValueError:
        print(RED + "Invalid input. Please enter a number." + RESET)
        return

    user_data["users"][current_user["username"]]["balance - RM"] += amount
    balance = user_data["users"][current_user["username"]]["balance - RM"]
        
    if save_json(files.ACCOUNTS_PATH, user_data, current_user):
        print(GREEN + f"Top up successful. New balance: RM{balance}." + RESET)
    else:
        print(RED + "Failed to top up balance." + RESET)
