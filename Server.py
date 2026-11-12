# The following file follows the traditional socket programming format of socket() -> connect() -> Read/Write Data -> close(),
# where the Read/Write Data from the Server is interfaced with the Read/Write Data of the Client

# program server
# declare: connected clients, public users, public messages, next public message id

#create 5 groups: each group with name, members, next message id

# read port number
# create TCP socket

# bind socket to port

#listen for clients

# while(TRUE)
#   accept client connection
#   create thread
#   thread executes handle_client
# end while

#handle_client(client socket)
#   receive username
#   if username already exists
#       send error
#       close client socket
#       return
#   end if
#
#   add username to connected_clients
#   broadcast "username connected"
#   while connection exists
#       Receive a Part 1 or Part 2 command from the main command loop in Client.java, and use if-statements to sort out the commands
#       and then implement each of the commands inside of the if-statement functions. ****
#   end while

#   remove username from public users

#   for every group
#       remove username from group.members
#   end for

#   remove username from connected_clients

#   broadcast "username is disconnected"

#   close socket

# end handle_client

# end program