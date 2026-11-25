# Project 2 Checklist

## Part 1 – Public Message Board (40%)

### Server (Python)

- [x] Uses plain TCP sockets only (no other networking libraries)
- [x] Listens on a non-system port (above 1024) and keeps running
- [x] Starts one thread per client connection
- [x] Keeps a list of all connected client sockets
- [x] Keeps each connection open until the client leaves or exits
- [x] Rejects a username that's already taken and asks again
- [x] Tracks which users have joined and left the public group
- [x] Tells all other clients when a user **joins**
- [x] Tells all other clients when a user **leaves**
- [x] Sends a new user the list of current users when they join
- [x] Sends a new user the **last 2 messages** posted on the board
- [x] Stores messages with an ID, sender, post date, subject and body
- [x] Sends each new post to everyone in the group as `Message ID, Sender, Post Date, Subject`
- [x] Returns a message's content when asked for it by ID
- [x] Handles a bad or missing message ID
- [x] Handles a client that disconnects suddenly by removing it and notifying the others
- [x] Uses locks on shared data so threads don't conflict

### Client (Java)

- [x] Uses plain `Socket` only (no other networking libraries)
- [x] Runs a separate thread that listens for server notifications while the user types
- [x] `%connect <address> <port>`
- [x] Asks for a username and retries if it's taken
- [x] `%join`
- [x] `%post <subject> <body>`
- [x] `%users`
- [x] `%leave`
- [x] `%message <id>`
- [x] `%exit` (disconnects cleanly and quits)
- [x] Shows clear errors for bad commands or arguments
- [x] Shows errors for commands used before connecting or joining

### Protocol

- [x] Agree on one message format (plain text or JSON) for both sides
- [ ] Write down the request and response format for every command
- [x] Keep notifications the server pushes separate from replies to requests

---

## Part 2 – Multiple Private Groups (30%)

### Server (Python)

- [x] Sets up **5 groups**, each with an ID and a name
- [x] Sends the list of groups when a client connects
- [x] Lets users join a group by **ID or name**
- [x] Lets a user be in **several groups at once**
- [x] Keeps a separate user list for each group
- [x] Keeps a separate message board for each group
- [x] Sends join and leave notifications only to members of that group
- [x] Sends a new group member the users and last 2 messages **for that group**
- [x] Never shows users or messages from one group to people outside it
- [x] Refuses group actions from users who haven't joined that group
- [x] Handles an unknown group ID or name
- [x] Removes a user from every group when they disconnect

### Client (Java)

- [x] `%groups`
- [x] `%groupjoin <group>`
- [x] `%grouppost <group> <subject> <body>`
- [x] `%groupusers <group>`
- [x] `%groupleave <group>`
- [x] `%groupmessage <group> <id>`
- [x] Labels group notifications with the group they came from

### Integration

- [x] Parts 1 and 2 work in the **same running program**
- [x] Users can switch between the public board and groups without disconnecting

---

## Documentation and Submission (15%)

- [x] Clear comments and meaningful variable names in both client and server
- [x] README lists all 3 names at the very top
- [x] README explains how to compile and run both programs
- [x] README lists what to install (JDK and Python versions)
- [x] README explains usage if it differs from the suggested commands
- [x] README describes major issues and how we handled them
- [x] Makefile (optional, but useful for compiling the Java client)
- [ ] Folder named `Project2-AskerFredy-GehlotJohnson` (check the last-name order with the group)
- [ ] Zip the folder without any binaries (no `.class` files) and submit it to Canvas

## Bonus

- [x] Client and server in different languages (+~5%)
- [x] GUI for the client (up to +5%)

## Testing Before the Demo

- [ ] Run 3 or more clients at once and check that join and leave notifications reach everyone
- [x] Check that a client joining late sees only the last 2 messages
- [x] Check that a taken username is rejected
- [x] Check that a user outside a group can't see its users or messages
- [x] Check that one user can be in several groups at once
- [x] Close a client window suddenly and check that the server keeps running
