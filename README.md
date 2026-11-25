# A Simple Bulletin Board Using Socket Programming

**CS4065 – Computer Networks**

**Group Members:**

- Jovan Jose Asker Fredy
- Raagya Gehlot
- Andrew Johnson

---

## Summary

This project is a client-server bulletin board built with plain unicast TCP sockets. No other networking libraries are used. It has three files:

| File            | Language | What it does                                                     |
| --------------- | -------- | ---------------------------------------------------------------- |
| `server.py`   | Python   | Multithreaded server with one thread per TCP connection          |
| `Client.java` | Java     | Console client that connects to the server with a socket         |
| `gui.py`      | Python   | Window (tkinter) that runs the Java client and sends it commands |

### Part 1 – Public Message Board

- Every client joins one public group and picks a unique username.
- The server tracks all connected users and tells everyone when a user joins or leaves.
- A new user sees the list of current users and the **last 2 messages** posted on the board.
- Messages are shown as: `Message ID, Sender, Post Date, Subject`.
- Users can fetch the full content of a message by its ID.

### Part 2 – Multiple Private Groups

- The server offers **5 groups**, and users can join them by ID or by name.
- A user can belong to several groups at once.
- Users and messages in one group can't be seen from other groups.
- Parts 1 and 2 run in the same session, so users can switch between them without disconnecting.

---

## Requirements

- **Java** JDK 11 or newer (client)
- **Python** 3.8 or newer with tkinter (server and GUI). tkinter comes with most Python installs.

No extra packages are needed.

## How to Run

### Testing alone on one computer

Open **3 terminals** in the project folder:

| Terminal | Command | What it does |
| -------- | ------------- | ----------------------- |
| 1 | `make server` | Starts the server |
| 2 | `make client` | First user (console) |
| 3 | `make client` | Second user (console) |

For the GUI, use `make gui` instead of `make client` in terminal 2 or 3.

In each client, type `%connect localhost 6789`, then pick a different username for each one. Both users need to `%join` the same board to see each other with `%users`.

Only start the server once. Each server has its own users and messages, so clients on different servers can't see each other.

### Step by step

Start the server first:

```bash
python3 server.py [port]      # default port is 6789
```

Then start one client for each user. Use either the GUI or the console.

**GUI.** It compiles and starts the Java client by itself:

```bash
python3 gui.py
```

**Console:**

```bash
javac Client.java
java Client
```

**With the Makefile:**

```bash
make            # compile the Java client
make server     # start the server (make server PORT=7000 for another port)
make client     # start the console client
make gui        # start the GUI
make clean      # remove compiled files
```

## Using the GUI

1. Enter the server address, port and username, then click **Connect**. If the username is taken, type another one in the **Command** box and press Enter.
2. Pick a board on the left (Public or one of the 5 groups), then click **Join**, **Leave** or **Users**.
3. Fill in **Subject** and **Message** and click **Post** to post to the selected board. Enter a **Message ID** and click **Read** to see a message's full content.
4. Any `%` command below can also be typed into the **Command** box.

In the console client, type `%connect <host> <port>` first, then your username when asked.

---

## Commands

### Part 1

| Command                       | Description                                |
| ----------------------------- | ------------------------------------------ |
| `%connect <address> <port>` | Connect to a running bulletin board server |
| `%join`                     | Join the public message board              |
| `%post <subject> \| <body>`  | Post a message to the public board         |
| `%users`                    | List users in the public group             |
| `%leave`                    | Leave the public group                     |
| `%message <id>`             | Show the content of a message              |
| `%exit`                     | Disconnect and exit the client             |

### Part 2

| Command                                   | Description                              |
| ----------------------------------------- | ---------------------------------------- |
| `%groups`                               | List all groups you can join             |
| `%groupjoin <group>`                    | Join a group by ID or name               |
| `%grouppost <group> <subject> \| <body>` | Post a message to a group                |
| `%groupusers <group>`                   | List users in a group                    |
| `%groupleave <group>`                   | Leave a group                            |
| `%groupmessage <group> <id>`            | Show the content of a message in a group |

**Differences from the suggested commands:**

- In `%post` and `%grouppost`, a `|` separates the subject from the body, so the subject can contain spaces.
- `<group>` can be the group's ID (1–5) or its name (Sports, Movies, Music, Tech, Travel).
- `%help` lists all commands.

---

## Protocol

Messages are plain text, one per line, with fields separated by a TAB. The first field is the message type and the rest are its arguments. Below, `<group>` is a group ID or name. The public board is group `0`, and groups `1`–`5` are the private groups.

### Requests and responses

| Client → Server | Server → Client | Sent to others in the group |
| --- | --- | --- |
| *(on connect)* | `WELCOME <text>` | |
| `NAME <username>` | `NAME_OK <username>` then `GROUPS <g1> … <g5>`, or `NAME_BAD <reason>` | |
| `GROUPS` | `GROUPS <g1> <g2> <g3> <g4> <g5>` | |
| `JOIN <group>` | `JOINED <group>`, `USERS <group> <user list>`, then up to 2 `POST` lines (the last 2 messages) | `USER_JOINED <group> <username>` |
| `LEAVE <group>` | `LEFT <group>` | `USER_LEFT <group> <username>` |
| `USERS <group>` | `USERS <group> <user list>` | |
| `POST <group> <subject> <body>` | `POST <group> <id> <sender> <date> <subject>` | the same `POST` line |
| `MESSAGE <group> <id>` | `CONTENT <group> <id> <sender> <date> <subject> <body>` | |
| `EXIT` | the server closes the connection | `USER_LEFT <group> <username>` for each group the user was in |

The `<user list>` is one field with names separated by `, `. Dates use the format `YYYY-MM-DD HH:MM`.

### Errors

Any request that fails gets `ERROR <reason>`, for example:

- a request sent before choosing a username
- an unknown group
- a group action from a user who isn't in that group
- a missing or invalid message ID
- a post without a subject or body

---

## Issues Encountered

- **Server notifications arriving while the user types.** The Java client reads from the socket on a separate thread, so messages appear right away.
- **Connecting the Python GUI to the Java client.** The GUI runs `java Client` as a child process. It writes commands to the client's input and shows the client's output.
- **Several server threads changing shared data.** A single lock protects the groups and the client list.
- **Tabs in user text breaking the protocol.** The client replaces them with spaces before sending.
- **Clients closing without `%exit`.** The server notices the dropped connection, removes the user from every group, and notifies the other members.
