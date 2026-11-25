# Project 2 Checklist

## Part 1 – Public Message Board (40%)

### Server (Python)

- [X] Uses plain TCP sockets only (no other networking libraries)
- [X] Listens on a non-system port (above 1024) and keeps running
- [X] Starts one thread per client connection
- [X] Keeps a list of all connected client sockets
- [X] Keeps each connection open until the client leaves or exits
- [X] Rejects a username that's already taken and asks again
- [X] Tracks which users have joined and left the public group
- [X] Tells all other clients when a user **joins**
- [X] Tells all other clients when a user **leaves**
- [X] Sends a new user the list of current users when they join
- [X] Sends a new user the **last 2 messages** posted on the board
- [X] Stores messages with an ID, sender, post date, subject and body
- [X] Sends each new post to everyone in the group as `Message ID, Sender, Post Date, Subject`
- [X] Returns a message's content when asked for it by ID
- [X] Handles a bad or missing message ID
- [X] Handles a client that disconnects suddenly by removing it and notifying the others
- [X] Uses locks on shared data so threads don't conflict

### Client (Java)

- [X] Uses plain `Socket` only (no other networking libraries)
- [X] Runs a separate thread that listens for server notifications while the user types
- [X] `%connect <address> <port>`
- [X] Asks for a username and retries if it's taken
- [X] `%join`
- [X] `%post <subject> <body>`
- [X] `%users`
- [X] `%leave`
- [X] `%message <id>`
- [X] `%exit` (disconnects cleanly and quits)
- [X] Shows clear errors for bad commands or arguments
- [X] Shows errors for commands used before connecting or joining

### Protocol

- [X] Agree on one message format (plain text or JSON) for both sides
- [X] Write down the request and response format for every command
- [X] Keep notifications the server pushes separate from replies to requests

---

## Part 2 – Multiple Private Groups (30%)

### Server (Python)

- [X] Sets up **5 groups**, each with an ID and a name
- [X] Sends the list of groups when a client connects
- [X] Lets users join a group by **ID or name**
- [X] Lets a user be in **several groups at once**
- [X] Keeps a separate user list for each group
- [X] Keeps a separate message board for each group
- [X] Sends join and leave notifications only to members of that group
- [X] Sends a new group member the users and last 2 messages **for that group**
- [X] Never shows users or messages from one group to people outside it
- [X] Refuses group actions from users who haven't joined that group
- [X] Handles an unknown group ID or name
- [X] Removes a user from every group when they disconnect

### Client (Java)

- [X] `%groups`
- [X] `%groupjoin <group>`
- [X] `%grouppost <group> <subject> <body>`
- [X] `%groupusers <group>`
- [X] `%groupleave <group>`
- [X] `%groupmessage <group> <id>`
- [X] Labels group notifications with the group they came from

### Integration

- [X] Parts 1 and 2 work in the **same running program**
- [X] Users can switch between the public board and groups without disconnecting

---

## Documentation and Submission (15%)

- [X] Clear comments and meaningful variable names in both client and server
- [X] README lists all 3 names at the very top
- [X] README explains how to compile and run both programs
- [X] README lists what to install (JDK and Python versions)
- [X] README explains usage if it differs from the suggested commands
- [X] README describes major issues and how we handled them
- [X] Makefile (optional, but useful for compiling the Java client)
- [X] Folder named `Project2-JoseAskerFredy-Gehlot-Johnson`
- [X] Zip the folder without any binaries (no `.class` files) and submit it to Canvas

## Bonus

- [X] Client and server in different languages (+~5%)
- [X] GUI for the client (up to +5%)

## Testing Before the Demo

- [X] Run 3 or more clients at once and check that join and leave notifications reach everyone
- [X] Check that a client joining late sees only the last 2 messages
- [X] Check that a taken username is rejected
- [X] Check that a user outside a group can't see its users or messages
- [X] Check that one user can be in several groups at once
- [X] Close a client window suddenly and check that the server keeps running
