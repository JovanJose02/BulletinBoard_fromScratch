// The following file follows the traditional socket programming format of socket() -> connect() -> Read/Write Data -> close(),
// where the Read/Write Data from the Server is interfaced with the Read/Write Data of the Server

// program client

// declare socket
// declare server_input_stream
// declare server_output_stream
// declare connected = FALSE

// Print a welcome message

// while connected == false
//  read user_input
//  if user_input starts with "%connect"
//      parse address and port
//      create TCP socket
//      connect to server
//      create input stream
//      create output stream
//      print "connected"
//      connected = TRUE
//      start Listener thread
//  else
//      print "you must connect first"
// end while

// listener thread
//  while socket is connected
//      receive message from server
//      display message
//  end while
// end thread

// main command loop
// while connected == true
//      read command from keyboard
//      send Part 1 and Part 2 command to server to be implemented in the handle_client in Server.py ****
//      if command == %exit
//          close I/O stream
//          close socket
//          connected = FALSE
//      end if
// end while

// print "disconnected"
// end program