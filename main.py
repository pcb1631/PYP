

import json

def login(users):
    username = input("Enter username: ")
    password = input("Enter password: ")
    if username in users and users[username]["password"] == password:
        print("Login successful!")
    else:
        print("Invalid username or password.")

def register(users):
    username = input("Enter new username: ")
    if username in users:
        print("Username already exists.")
        return users
    password = input("Enter password: ")
    email = input("Enter email: ")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    user_type = input("Enter user type (e.g., Admin, Member): ")
    users[username] = {
        "password": password,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "user_type": user_type
    }
    print("Registration successful!")
    return users

def main():  # This function will be run first
    with open("userData/users.json", "r") as f:
        data = json.load(f)
    users = data["users"]

    while True:
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            login(users)
        elif choice == "2":
            users = register(users)
            with open("userData/users.json", "w") as f:
                json.dump(data, f, indent=4)
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

