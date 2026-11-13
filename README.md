# A Simple Bulletin Board Using Socket Programming

**CS4065 – Computer Networks** 

**Group Members:**

- Jovan Jose Asker Fredy
- Raagya Gehlot
- Andrew Johnson

---

## Summary

This project is a client-server bulletin board built with plain unicast TCP sockets. No other networking libraries are used. It has three files:

| File | Language | What it does |
| ---- | -------- | ------------ |
| `server.py` | Python | Multithreaded server with one thread per TCP connection |
| `Client.java` | Java | Console client that connects to the server with a socket |
| `gui.py` | Python | Window (tkinter) that runs the Java client and sends it commands |

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

| Command                                 | Description                              |
| --------------------------------------- | ---------------------------------------- |
| `%groups`                             | List all groups you can join             |
| `%groupjoin <group>`                  | Join a group by ID or name               |
| `%grouppost <group> <subject> \| <body>` | Post a message to a group             |
| `%groupusers <group>`                 | List users in a group                    |
| `%groupleave <group>`                 | Leave a group                            |
| `%groupmessage <group> <id>`          | Show the content of a message in a group |

**Differences from the suggested commands:**
- In `%post` and `%grouppost`, a `|` separates the subject from the body, so the subject can contain spaces.
- `<group>` can be the group's ID (1–5) or its name (Sports, Movies, Music, Tech, Travel).
- `%help` lists all commands.

---

## Protocol

Messages are plain text, one per line, with fields separated by a TAB.

| Client → Server | Server → Client |
|-----------------|-----------------|
| `NAME`, `GROUPS`, `JOIN`, `LEAVE`, `USERS`, `POST`, `MESSAGE`, `EXIT` | `WELCOME`, `NAME_OK`, `NAME_BAD`, `GROUPS`, `JOINED`, `LEFT`, `USERS`, `USER_JOINED`, `USER_LEFT`, `POST`, `CONTENT`, `ERROR` |

The public board is group `0`. Groups `1`–`5` are the private groups.

---

## Issues Encountered

- **Server notifications arriving while the user types.** The Java client reads from the socket on a separate thread, so messages appear right away.
- **Connecting the Python GUI to the Java client.** The GUI runs `java Client` as a child process. It writes commands to the client's input and shows the client's output.
- **Several server threads changing shared data.** A single lock protects the groups and the client list.
- **Tabs in user text breaking the protocol.** The client replaces them with spaces before sending.
- **Clients closing without `%exit`.** The server notices the dropped connection, removes the user from every group, and notifies the other members.
