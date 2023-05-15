import json
class Node:
    def __init__(self, data):
        self.data = data
        self.next_node = None


class CommandHistory:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current_node = None
        self.user_commands = {}

    def append(self, data, user_id):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next_node = new_node
            self.tail = new_node
        
        if user_id in self.user_commands:
            self.user_commands[user_id].append(new_node)
        else:
            self.user_commands[user_id] = [new_node]

    def get_last_command(self):
        if self.tail is not None:
            return self.tail.data
        else:
            return None

    def get_user_commands(self, user_id):
        if user_id in self.user_commands:
            return [node.data for node in self.user_commands[user_id]]
        else:
            return []

    def move_forward(self):
        if self.current_node is None:
            self.current_node = self.tail
        elif self.current_node.next_node is not None:
            self.current_node = self.current_node.next_node

        if self.current_node is not None:
            return self.current_node.data
        else:
            return None

    def move_backward(self):
        if self.current_node is None:
            self.current_node = self.tail
        elif self.current_node == self.head:
            return None
        else:
            current = self.head
            while current.next_node != self.current_node:
                current = current.next_node
            self.current_node = current

        if self.current_node is not None:
            return self.current_node.data
        else:
            return None

    def clear_history(self, user_id=None):
        if user_id is not None:
            if user_id in self.user_commands:
                user_commands = self.user_commands[user_id]
                for node in user_commands:
                    if node == self.head:
                        self.head = node.next_node
                        node.next_node = None
                    elif node == self.tail:
                        self.tail = self.current_node
                        self.current_node.next_node = None
                        self.current_node = self.tail
                    else:
                        prev_node = self.head
                        while prev_node.next_node != node:
                            prev_node = prev_node.next_node
                        prev_node.next_node = node.next_node
                        node.next_node = None
                del self.user_commands[user_id]
        else:
            self.head = None
            self.tail = None
            self.current_node = None
            self.user_commands = {}