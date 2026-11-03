# Project 2 Checklist

## Part 1 – Public Message Board (40%)

### Server (Python)

- [ ] Uses plain TCP sockets only (no other networking libraries)
- [ ] Listens on a non-system port (above 1024) and keeps running
- [ ] Starts one thread per client connection
- [ ] Keeps a list of all connected client sockets
- [ ] Keeps each connection open until the client leaves or exits
- [ ] Rejects a username that's already taken and asks again
- [ ] Tracks which users have joined and left the public group
- [ ] Tells all other clients when a user **joins**
- [ ] Tells all other clients when a user **leaves**
- [ ] Sends a new user the list of current users when they join
- [ ] Sends a new user the **last 2 messages** posted on the board
- [ ] Stores messages with an ID, sender, post date, subject and body
- [ ] Sends each new post to everyone in the group as `Message ID, Sender, Post Date, Subject`
- [ ] Returns a message's content when asked for it by ID
- [ ] Handles a bad or missing message ID
- [ ] Handles a client that disconnects suddenly by removing it and notifying the others
- [ ] Uses locks on shared data so threads don't conflict

### Client (Java)

- [ ] Uses plain `Socket` only (no other networking libraries)
- [ ] Runs a separate thread that listens for server notifications while the user types
- [ ] `%connect <address> <port>`
- [ ] Asks for a username and retries if it's taken
- [ ] `%join`
- [ ] `%post <subject> <body>`
- [ ] `%users`
- [ ] `%leave`
- [ ] `%message <id>`
- [ ] `%exit` (disconnects cleanly and quits)
- [ ] Shows clear errors for bad commands or arguments
- [ ] Shows errors for commands used before connecting or joining

### Protocol

- [ ] Agree on one message format (plain text or JSON) for both sides
- [ ] Write down the request and response format for every command
- [ ] Keep notifications the server pushes separate from replies to requests

---

## Part 2 – Multiple Private Groups (30%)

### Server (Python)

- [ ] Sets up **5 groups**, each with an ID and a name
- [ ] Sends the list of groups when a client connects
- [ ] Lets users join a group by **ID or name**
- [ ] Lets a user be in **several groups at once**
- [ ] Keeps a separate user list for each group
- [ ] Keeps a separate message board for each group
- [ ] Sends join and leave notifications only to members of that group
- [ ] Sends a new group member the users and last 2 messages **for that group**
- [ ] Never shows users or messages from one group to people outside it
- [ ] Refuses group actions from users who haven't joined that group
- [ ] Handles an unknown group ID or name
- [ ] Removes a user from every group when they disconnect

### Client (Java)

- [ ] `%groups`
- [ ] `%groupjoin <group>`
- [ ] `%grouppost <group> <subject> <body>`
- [ ] `%groupusers <group>`
- [ ] `%groupleave <group>`
- [ ] `%groupmessage <group> <id>`
- [ ] Labels group notifications with the group they came from

### Integration

- [ ] Parts 1 and 2 work in the **same running program**
- [ ] Users can switch between the public board and groups without disconnecting

---

## Documentation and Submission (15%)

- [ ] Clear comments and meaningful variable names in both client and server
- [ ] README lists all 3 names at the very top
- [ ] README explains how to compile and run both programs
- [ ] README lists what to install (JDK and Python versions)
- [ ] README explains usage if it differs from the suggested commands
- [ ] README describes major issues and how we handled them
- [ ] Makefile (optional, but useful for compiling the Java client)
- [ ] Folder named `Project2-AskerFredy-GehlotJohnson` (check the last-name order with the group)
- [ ] Zip the folder without any binaries (no `.class` files) and submit it to Canvas

## Bonus

- [ ] Client and server in different languages (+~5%)
- [ ] GUI for the client (up to +5%)

## Testing Before the Demo

- [ ] Run 3 or more clients at once and check that join and leave notifications reach everyone
- [ ] Check that a client joining late sees only the last 2 messages
- [ ] Check that a taken username is rejected
- [ ] Check that a user outside a group can't see its users or messages
- [ ] Check that one user can be in several groups at once
- [ ] Close a client window suddenly and check that the server keeps running
