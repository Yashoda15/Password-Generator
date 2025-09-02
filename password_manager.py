import random
import string
import json
import os
import base64

PASSWORD_FILE = "passwords.json"

def generate_password(length=12):
    """Generate a strong random password"""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def password_strength(password):
    """Simple password strength indicator"""
    strength = "Weak"
    if (len(password) >= 12 and any(c.islower() for c in password)
        and any(c.isupper() for c in password)
        and any(c.isdigit() for c in password)
        and any(c in string.punctuation for c in password)):
        strength = "Strong"
    elif len(password) >= 8:
        strength = "Moderate"
    return strength

def save_password(account, password):
    """Save password (encoded) to JSON file"""
    encoded = base64.b64encode(password.encode()).decode()
    data = {}
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as file:
            data = json.load(file)
    data[account] = encoded
    with open(PASSWORD_FILE, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Password for '{account}' saved successfully!")

def view_passwords():
    """View all saved passwords (decoded)"""
    if not os.path.exists(PASSWORD_FILE):
        print("No passwords saved yet.")
        return
    with open(PASSWORD_FILE, "r") as file:
        data = json.load(file)
        if not data:
            print("No passwords saved yet.")
            return
        print("\nSaved Passwords:")
        for account, encoded in data.items():
            password = base64.b64decode(encoded.encode()).decode()
            print(f"{account}: {password}")

def main():
    while True:
        print("\n==== Password Manager ====")
        print("1. Generate Password")
        print("2. View Saved Passwords")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            account = input("Enter account name: ")
            length = input("Enter password length (default 12): ")
            length = int(length) if length.isdigit() else 12
            password = generate_password(length)
            print(f"Generated Password: {password}")
            print(f"Password Strength: {password_strength(password)}")
            save_password(account, password)
        elif choice == "2":
            view_passwords()
        elif choice == "3":
            print("Exiting Password Manager.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
