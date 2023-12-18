from cryptography.fernet import Fernet
import json
import getpass

class PasswordManager:
    def __init__(self):
        self.master_password = None
        self.key = None
        self.passwords = {}

    def generate_key(self):
        return Fernet.generate_key()

    def encrypt(self, data):
        cipher_suite = Fernet(self.key)
        encrypted_data = cipher_suite.encrypt(data.encode())
        return encrypted_data.decode()

    def decrypt(self, encrypted_data):
        cipher_suite = Fernet(self.key)
        decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
        return decrypted_data

    def set_master_password(self, master_password):
        self.master_password = master_password
        self.key = self.generate_key()

    def save_password(self, website, username, password):
        data = {"username": username, "password": self.encrypt(password)}
        self.passwords[website] = data

    def get_password(self, website):
        data = self.passwords.get(website)
        if data:
            return data["username"], self.decrypt(data["password"])
        else:
            return None

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            data = {
                "master_password": self.master_password,
                "key": self.key.decode(),
                "passwords": self.passwords
            }
            json.dump(data, file, indent=2)

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.master_password = data.get("master_password")
                self.key = data.get("key").encode()  # Convert string to bytes
                self.passwords = data.get("passwords", {})
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False


password_manager = PasswordManager()


master_password = getpass.getpass("Set/Enter your master password: ")
if password_manager.load_from_file("passwords.json"):
   
    if master_password != password_manager.master_password:
        print("Incorrect master password. Exiting.")
        exit()
else:

    password_manager.set_master_password(master_password)

password_manager.save_password("example.com", "user123", "securePassword123")
password_manager.save_password("another-site.com", "john_doe", "anotherSecurePassword")


password_manager.save_to_file("passwords.json")


loaded_password_manager = PasswordManager()
if loaded_password_manager.load_from_file("passwords.json"):

    website = "example.com"
    credentials = loaded_password_manager.get_password(website)
    if credentials:
        print(f"For {website}: Username: {credentials[0]}, Password: {credentials[1]}")
    else:
        print(f"No credentials found for {website}")
else:
    print("Password file not found or corrupted.")

