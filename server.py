# Bulletin board server. Run: python3 server.py [port]
# Protocol: one line per message, fields separated by TAB.

import socket
import sys
import threading
from datetime import datetime

# Port comes from the command line, default is 6789
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 6789
GROUP_NAMES = ["Public", "Sports", "Movies", "Music", "Tech", "Travel"]  # index 0 = public board

# Shared data for all client threads. The lock protects it.
members = {name: {} for name in GROUP_NAMES}    # group -> {username: client}
messages = {name: [] for name in GROUP_NAMES}   # group -> list of messages
clients = []
lock = threading.Lock()


# Finds a group by its number or name
def find_group(key):
    key = key.strip().lower()
    for number, name in enumerate(GROUP_NAMES):
        if key == str(number) or key == name.lower():
            return name
    return None


# One thread per connected client
class Client(threading.Thread):
    def __init__(self, conn):
        super().__init__(daemon=True)
        self.conn = conn
        self.username = None

    # Sends one protocol line to this client
    def send(self, *fields):
        try:
            self.conn.sendall(("\t".join(str(f) for f in fields) + "\n").encode())
        except OSError:
            pass

    # Sends a line to everyone else in the group
    def tell_group(self, group, *fields):
        for client in members[group].values():
            if client is not self:
                client.send(*fields)

    # Reads lines from the client until it exits or disconnects
    def run(self):
        self.send("WELCOME", "Welcome to the bulletin board!")
        try:
            for line in self.conn.makefile("r", encoding="utf-8"):
                parts = line.rstrip("\r\n").split("\t")
                if parts[0] == "EXIT":
                    break
                with lock:
                    self.handle(parts[0], parts[1:])
        except (OSError, UnicodeDecodeError):
            pass
        # Clean up: leave every group and remove the client
        with lock:
            for group in GROUP_NAMES:
                if self.username in members[group]:
                    self.leave(group)
            if self in clients:
                clients.remove(self)
        self.conn.close()
        print("Disconnected:", self.username)

    # Checks the command and calls the matching method
    def handle(self, command, args):
        if command == "NAME":
            self.set_name(args[0].strip() if args else "")
            return
        if self.username is None:
            self.send("ERROR", "Enter a username first.")
            return
        if command == "GROUPS":
            self.send("GROUPS", *GROUP_NAMES[1:])
            return

        # The rest need a group, and all but JOIN need you to be in it
        group = find_group(args[0]) if args else None
        if group is None:
            self.send("ERROR", "No such group.")
        elif command == "JOIN":
            self.join(group)
        elif self.username not in members[group]:
            self.send("ERROR", "You are not in " + group + ".")
        elif command == "LEAVE":
            self.leave(group)
        elif command == "USERS":
            self.send("USERS", group, ", ".join(members[group]))
        elif command == "POST" and len(args) == 3:
            self.post(group, args[1], args[2])
        elif command == "MESSAGE" and len(args) == 2:
            self.read(group, args[1])
        else:
            self.send("ERROR", "Bad command.")

    # Saves the username if it is valid and not taken
    def set_name(self, name):
        if self.username is not None:
            self.send("ERROR", "You already have a username.")
        elif name == "" or "," in name:
            self.send("NAME_BAD", "Invalid username.")
        elif any(c.username == name for c in clients):
            self.send("NAME_BAD", "Username " + name + " is taken.")
        else:
            self.username = name
            clients.append(self)
            self.send("NAME_OK", name)
            self.send("GROUPS", *GROUP_NAMES[1:])  # Part 2: list the 5 groups on connect
            print("Connected:", name)

    # Adds the user, sends them the users and last 2 posts, and tells the group
    def join(self, group):
        if self.username in members[group]:
            self.send("ERROR", "You are already in " + group + ".")
            return
        members[group][self.username] = self
        self.send("JOINED", group)
        self.send("USERS", group, ", ".join(members[group]))
        for message in messages[group][-2:]:
            self.send("POST", group, *message[:4])
        self.tell_group(group, "USER_JOINED", group, self.username)

    # Removes the user and tells the group
    def leave(self, group):
        del members[group][self.username]
        self.send("LEFT", group)
        self.tell_group(group, "USER_LEFT", group, self.username)

    # Saves the post and sends it to everyone in the group
    def post(self, group, subject, body):
        if not subject.strip() or not body.strip():
            self.send("ERROR", "A post needs a subject and a body.")
            return
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        message = [len(messages[group]) + 1, self.username, date, subject, body]
        messages[group].append(message)
        for client in members[group].values():
            client.send("POST", group, *message[:4])

    # Sends the full content of one message
    def read(self, group, message_id):
        if not message_id.isdigit() or not 1 <= int(message_id) <= len(messages[group]):
            self.send("ERROR", "No message with ID " + message_id + " in " + group + ".")
            return
        self.send("CONTENT", group, *messages[group][int(message_id) - 1])


# Start the server and give each new connection its own thread
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("", PORT))
server.listen()
print("Server listening on port", PORT)
try:
    while True:
        conn, address = server.accept()
        Client(conn).start()
except KeyboardInterrupt:
    print("Server stopped.")
