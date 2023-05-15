import json
from historique_liste import CommandHistory
from threading import Lock


class ProtectedCommandHistory:
    def __init__(self):
        self.user_histories = {}
        self.access_lock = Lock()

    def append(self, data, user_id):
        with self.access_lock:
            if user_id not in self.user_histories:
                self.user_histories[user_id] = CommandHistory()
            self.user_histories[user_id].append(data, user_id)

    def save_to_text(self, filename):
        with open(filename, "w") as file:
            for user_id, user_history in self.user_histories.items():
                file.write(f"User ID: {user_id}\n")
                for command_data in user_history.get_user_commands(user_id):
                    file.write(f"Command: {command_data}\n")
                file.write("\n")

    def load_from_text(self, filename):
        self.clear_history()  # Efface l'historique actuel avant de charger les nouvelles données

        with open(filename, "r") as file:
            user_id = None

            for line in file:
                line = line.strip()

                if line.startswith("User ID: "):
                    user_id = int(line.split(": ", 1)[1])
                    self.request_access(user_id)  # Demande l'accès pour l'utilisateur

                elif line.startswith("Command: ") and user_id is not None:
                    command_data = line.split(": ", 1)[1]
                    self.append(command_data, user_id)

                elif line == "":
                    user_id = None


    def get_user_commands(self, user_id):
        with self.access_lock:
            if user_id in self.user_histories:
                return self.user_histories[user_id].get_user_commands(user_id)
            else:
                return []

    def move_forward(self, user_id):
        with self.access_lock:
            if user_id in self.user_histories:
                return self.user_histories[user_id].move_forward()
            else:
                return None

    def move_backward(self, user_id):
        with self.access_lock:
            if user_id in self.user_histories:
                return self.user_histories[user_id].move_backward()
            else:
                return None

    def clear_history(self, user_id=None):
        with self.access_lock:
            if user_id is not None and user_id in self.user_histories:
                del self.user_histories[user_id]
            else:
                self.user_histories = {}

    def request_access(self, user_id):
        with self.access_lock:
            if user_id not in self.user_histories:
                self.user_histories[user_id] = CommandHistory()

    def release_access(self, user_id):
        pass

    def is_access_granted(self, user_id):
        return True