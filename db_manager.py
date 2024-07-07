import json


class DBManager:
    def __init__(self, ):
        """Initializes the DBManager by loading users from a JSON file."""

        self.json_file = "database.json"

        self.data = {
            "users": {},
            "connections": []
        }
        self.load_users()

    def load_users(self):
        """Loads users and connections from the JSON file."""

        try:
            with open(self.json_file, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            print("File not found")
            self.data = {
                "users": {},
                "connections": []
            }

    def save_users(self):
        with open(self.json_file, 'w') as f:
            json.dump(self.data, f)

    def register(self, username, password):
        if username in self.data["users"]:
            return False
        print(self.data)
        self.data["users"][username] = password
        self.save_users()
        return True

    def login(self, username, password):
        print(self.data)
        return self.data["users"].get(username) == password

    def logout(self, username):
        self.data["connections"] = [conn for conn in self.data["connections"] if conn["username"] != username]
        self.save_users()

    def add_connection(self, address, username):
        """Adds a new connection for a user.

        Args:
            address (tuple): The address of the connection.
            username (str): The username of the user.
        """

        self.data["connections"].append({"address": address, "username": username})
        self.save_users()

    def get_online_users(self):
        return self.data["connections"]

    def get_user_port(self, username):
        for conn in self.data["connections"]:
            if conn["username"] == username:
                return conn["address"][1]