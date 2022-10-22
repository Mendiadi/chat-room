import os

from user_model import User
import utils


class DataBase:
    output_file_name = "db.json"

    def __init__(self):
        self.output_file = None
        self.users = dict()

    def load(self):
        if self.output_file_name in os.listdir():
            self.users = utils.json_read(self.output_file_name)
        else:
            utils.write_to_json(self.users, self.output_file_name)
        print("[DB] loaded data.")

    def add(self, user):
        if not isinstance(user, dict):
            user_json = user.to_json()
        else:
            user = User(**user)
            user_json = user.to_json()
        if user.username not in self.users:
            self.users[user.username] = user_json
            print(f"[DB] User {user.username} Created!")
        else:
            print(f"[DB] User {user.username} Already Exists.")

    def remove(self, user):
        if user.username not in self.users:
            print(f"[DB] Cant remove! user {user.username} not Exists.")
        else:
            self.users.pop(user.username)
            print(f"[DB] User {user.username} Removed.")

    def commit(self):
        utils.write_to_json(self.users, self.output_file_name, len(self.users))
        print("[DB] commited.")
