# Bulletin board GUI. It runs the Java client and sends it commands. Run: python3 gui.py
import os
import queue
import subprocess
import threading
import tkinter as tk
from tkinter import ttk

# Folder with Client.java, and the boards shown on the left
FOLDER = os.path.dirname(os.path.abspath(__file__))
BOARDS = ["Public", "Sports", "Movies", "Music", "Tech", "Travel"]


# The window. Buttons build % commands and send them to the Java client.
class BulletinBoardGUI:
    # Sets up the window and starts checking for client output
    def __init__(self, root):
        self.root = root
        self.client = None
        self.lines = queue.Queue()
        root.title("Bulletin Board")
        root.geometry("950x580")
        root.protocol("WM_DELETE_WINDOW", self.close)
        self.build()
        self.root.after(100, self.show_output)

    # Builds the window layout
    def build(self):
        # Top row: server, port and username
        top = ttk.Frame(self.root, padding=8)
        top.pack(side="top", fill="x")
        self.host = self.entry(top, "Server", "localhost", 12)
        self.port = self.entry(top, "Port", "6789", 6)
        self.username = self.entry(top, "Username", "", 12)
        ttk.Button(top, text="Connect", command=self.connect).pack(side="left", padx=6)
        ttk.Button(top, text="Exit", command=self.close).pack(side="left")

        # Bottom row: type any % command
        command_row = ttk.Frame(self.root, padding=8)
        command_row.pack(side="bottom", fill="x")
        ttk.Label(command_row, text="Command").pack(side="left", padx=(8, 2))
        self.command = ttk.Entry(command_row)
        self.command.pack(side="left", fill="x", expand=True)
        self.command.bind("<Return>", lambda event: self.send_command_box())

        # Row above it: post and read messages
        post_row = ttk.Frame(self.root, padding=(8, 0))
        post_row.pack(side="bottom", fill="x")
        self.subject = self.entry(post_row, "Subject", "", 14)
        self.body = self.entry(post_row, "Message", "", 36)
        ttk.Button(post_row, text="Post", command=self.post).pack(side="left", padx=6)
        self.message_id = self.entry(post_row, "Message ID", "", 4)
        ttk.Button(post_row, text="Read", command=self.read).pack(side="left", padx=6)

        middle = ttk.Frame(self.root, padding=8)
        middle.pack(side="top", fill="both", expand=True)

        # Left side: pick a board, then join, leave or list users
        side = ttk.LabelFrame(middle, text="Board", padding=8)
        side.pack(side="left", fill="y")
        self.board = tk.StringVar(value="Public")
        for name in BOARDS:
            ttk.Radiobutton(side, text=name, value=name, variable=self.board).pack(anchor="w", pady=2)
        ttk.Separator(side).pack(fill="x", pady=8)
        ttk.Button(side, text="Join", command=lambda: self.board_command("%join", "%groupjoin")).pack(fill="x", pady=2)
        ttk.Button(side, text="Leave", command=lambda: self.board_command("%leave", "%groupleave")).pack(fill="x", pady=2)
        ttk.Button(side, text="Users", command=lambda: self.board_command("%users", "%groupusers")).pack(fill="x", pady=2)
        ttk.Button(side, text="All groups", command=lambda: self.send("%groups")).pack(fill="x", pady=2)

        # Output from the client
        self.output = tk.Text(middle, state="disabled", wrap="word", font=("Menlo", 12),
                              bg="#1e2130", fg="#e8e8e8", padx=10, pady=10, borderwidth=0)
        scroll = ttk.Scrollbar(middle, command=self.output.yview)
        self.output["yscrollcommand"] = scroll.set
        scroll.pack(side="right", fill="y")
        self.output.pack(side="left", fill="both", expand=True, padx=(8, 0))

    # Adds a label and a text box
    def entry(self, parent, label, value, width):
        ttk.Label(parent, text=label).pack(side="left", padx=(8, 2))
        box = ttk.Entry(parent, width=width)
        box.insert(0, value)
        box.pack(side="left")
        return box

    # Adds text to the output box
    def write(self, text):
        self.output.config(state="normal")
        self.output.insert("end", text)
        self.output.see("end")
        self.output.config(state="disabled")

    # Compiles Client.java if needed and starts it
    def start_client(self):
        java_file = os.path.join(FOLDER, "Client.java")
        class_file = os.path.join(FOLDER, "Client.class")
        if not os.path.exists(class_file) or os.path.getmtime(class_file) < os.path.getmtime(java_file):
            subprocess.run(["javac", "Client.java"], cwd=FOLDER)
        self.client = subprocess.Popen(["java", "Client"], cwd=FOLDER, text=True, bufsize=1,
                                       stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        threading.Thread(target=self.read_client, args=(self.client,), daemon=True).start()

    # Runs on its own thread and queues the client's output
    def read_client(self, client):
        for line in client.stdout:
            self.lines.put(line)
        self.lines.put("Client closed.\n")

    # Moves queued output into the window every 100 ms
    def show_output(self):
        while not self.lines.empty():
            self.write(self.lines.get())
        self.root.after(100, self.show_output)

    # Sends one line to the Java client, starting it if needed
    def send(self, text):
        if self.client is None or self.client.poll() is not None:
            self.start_client()
        self.write("> " + text + "\n")
        try:
            self.client.stdin.write(text + "\n")
            self.client.stdin.flush()
        except OSError:
            self.write("Could not talk to the Java client.\n")

    # Connects and sends the username if one was typed
    def connect(self):
        self.send("%connect " + self.host.get().strip() + " " + self.port.get().strip())
        if self.username.get().strip():
            self.send(self.username.get().strip())

    # Uses the public command for Public and the group command otherwise
    def board_command(self, public_command, group_command, extra=""):
        if self.board.get() == "Public":
            self.send((public_command + " " + extra).strip())
        else:
            self.send((group_command + " " + self.board.get() + " " + extra).strip())

    # Posts to the selected board
    def post(self):
        self.board_command("%post", "%grouppost", self.subject.get() + " | " + self.body.get())
        self.subject.delete(0, "end")
        self.body.delete(0, "end")

    # Reads a message from the selected board
    def read(self):
        self.board_command("%message", "%groupmessage", self.message_id.get().strip())
        self.message_id.delete(0, "end")

    # Sends whatever is in the Command box
    def send_command_box(self):
        if self.command.get().strip():
            self.send(self.command.get().strip())
        self.command.delete(0, "end")

    # Exits the client and closes the window
    def close(self):
        if self.client is not None and self.client.poll() is None:
            self.send("%exit")
        self.root.destroy()


# Start the GUI
root = tk.Tk()
BulletinBoardGUI(root)
root.mainloop()
