# A Simple Bulletin Board Using Socket Programming

**CS4065 – Computer Networks and Networked Computing**

**Group Members:**
- Jovan Jose Asker Fredy
- Raagya Gehlot
- Andrew Johnson

---

## Summary

This project is a client-server bulletin board built with plain unicast TCP sockets. No other networking libraries are used. The client and server are written in different languages:

| Component | Language | Notes |
|-----------|----------|-------|
| **Client** | Java | Console client; sends commands to the server and shows server notifications |
| **Server** | Python | Standalone multithreaded server, one thread per TCP connection |

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
- **Python** 3.8 or newer (server)

## How to Run

### Server (Python)
```bash
python3 server.py [port]
```

### Client (Java)
```bash
javac Client.java
java Client
```

---

## Commands

### Part 1
| Command | Description |
|---------|-------------|
| `%connect <address> <port>` | Connect to a running bulletin board server |
| `%join` | Join the public message board |
| `%post <subject> <body>` | Post a message to the public board |
| `%users` | List users in the public group |
| `%leave` | Leave the public group |
| `%message <id>` | Show the content of a message |
| `%exit` | Disconnect and exit the client |

### Part 2
| Command | Description |
|---------|-------------|
| `%groups` | List all groups you can join |
| `%groupjoin <group>` | Join a group by ID or name |
| `%grouppost <group> <subject> <body>` | Post a message to a group |
| `%groupusers <group>` | List users in a group |
| `%groupleave <group>` | Leave a group |
| `%groupmessage <group> <id>` | Show the content of a message in a group |

---

## Issues Encountered
_To be filled in as development progresses._
