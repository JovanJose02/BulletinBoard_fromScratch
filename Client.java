import java.io.*;
import java.net.Socket;
import java.util.Scanner;

// Bulletin board console client. Run: java Client
public class Client {
    // Connection to the server
    static Socket socket;
    static PrintWriter out;
    static volatile boolean hasName = false;

    // Reads what the user types. Lines without % are sent as the username.
    public static void main(String[] args) {
        System.out.println("Bulletin board client. Type %help for commands.");
        Scanner input = new Scanner(System.in);
        while (input.hasNextLine()) {
            String line = input.nextLine().trim();
            if (line.isEmpty()) continue;
            if (line.startsWith("%")) {
                runCommand(line);
            } else if (out != null && !hasName) {
                send("NAME", line);
            } else {
                System.out.println("Commands start with %. Type %help.");
            }
        }
        disconnect();
    }

    // Turns a % command into a protocol message. The public board is group 0.
    static void runCommand(String line) {
        String[] parts = line.split("\\s+", 2);
        String command = parts[0].toLowerCase();
        String rest = parts.length > 1 ? parts[1] : "";
        String[] words = rest.split("\\s+", 2);
        String first = words[0];
        String second = words.length > 1 ? words[1] : "";

        switch (command) {
            case "%connect":      connect(first, second); break;
            // Part 1
            case "%join":         send("JOIN", "0"); break;
            case "%post":         post("0", rest); break;
            case "%users":        send("USERS", "0"); break;
            case "%leave":        send("LEAVE", "0"); break;
            case "%message":      send("MESSAGE", "0", rest); break;
            // Part 2
            case "%groups":       send("GROUPS"); break;
            case "%groupjoin":    send("JOIN", rest); break;
            case "%grouppost":    post(first, second); break;
            case "%groupusers":   send("USERS", rest); break;
            case "%groupleave":   send("LEAVE", rest); break;
            case "%groupmessage": send("MESSAGE", first, second); break;
            case "%exit":
                disconnect();
                System.exit(0);
            case "%help":
                System.out.println("%connect <host> <port>, %join, %post <subject> | <body>, %users, %leave,");
                System.out.println("%message <id>, %groups, %groupjoin <group>, %grouppost <group> <subject> | <body>,");
                System.out.println("%groupusers <group>, %groupleave <group>, %groupmessage <group> <id>, %exit");
                break;
            default:
                System.out.println("Unknown command. Type %help.");
        }
    }

    // Subject and body are separated by "|".
    static void post(String group, String text) {
        String[] parts = text.split("\\|", 2);
        if (parts.length < 2) {
            System.out.println("Use: <subject> | <body>");
            return;
        }
        send("POST", group, parts[0].trim(), parts[1].trim());
    }

    // Opens the socket and starts a thread that listens to the server
    static void connect(String host, String port) {
        if (socket != null) {
            System.out.println("Already connected.");
            return;
        }
        try {
            socket = new Socket(host, Integer.parseInt(port));
            out = new PrintWriter(socket.getOutputStream(), true);
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            new Thread(() -> listen(in)).start();
        } catch (Exception e) {
            System.out.println("Could not connect. Use: %connect <host> <port>");
            socket = null;
        }
    }

    // Prints every line the server sends until the connection closes
    static void listen(BufferedReader in) {
        try {
            String line;
            while ((line = in.readLine()) != null) {
                show(line.split("\t", -1));
            }
        } catch (IOException e) {
            // connection closed
        }
        System.out.println("Disconnected from server.");
        socket = null;
        out = null;
        hasName = false;
    }

    // Prints a server message in a readable way
    static void show(String[] f) {
        switch (f[0]) {
            case "WELCOME":     System.out.println(f[1] + " Enter a username:"); break;
            case "NAME_BAD":    System.out.println(f[1] + " Enter a username:"); break;
            case "NAME_OK":
                hasName = true;
                System.out.println("Hi " + f[1] + "! Type %join for the public board or %groups for groups.");
                break;
            case "GROUPS":
                System.out.println("Groups: 1 " + f[1] + ", 2 " + f[2] + ", 3 " + f[3] + ", 4 " + f[4] + ", 5 " + f[5]);
                break;
            case "JOINED":      System.out.println("You joined " + f[1] + "."); break;
            case "LEFT":        System.out.println("You left " + f[1] + "."); break;
            case "USERS":       System.out.println("[" + f[1] + "] Users: " + f[2]); break;
            case "USER_JOINED": System.out.println("[" + f[1] + "] " + f[2] + " joined."); break;
            case "USER_LEFT":   System.out.println("[" + f[1] + "] " + f[2] + " left."); break;
            case "POST":        System.out.println("[" + f[1] + "] " + f[2] + ", " + f[3] + ", " + f[4] + ", " + f[5]); break;
            case "CONTENT":
                System.out.println("[" + f[1] + "] Message " + f[2] + " from " + f[3] + " on " + f[4]);
                System.out.println("  Subject: " + f[5]);
                System.out.println("  " + f[6]);
                break;
            case "ERROR":       System.out.println("Error: " + f[1]); break;
            default:            System.out.println(String.join(" ", f));
        }
    }

    // Sends the fields joined by tabs. Tabs typed by the user become spaces.
    static void send(String... fields) {
        if (out == null) {
            System.out.println("Not connected. Use %connect <host> <port>.");
            return;
        }
        for (int i = 0; i < fields.length; i++) fields[i] = fields[i].replace("\t", " ");
        out.println(String.join("\t", fields));
    }

    // Tells the server we are leaving and closes the socket
    static void disconnect() {
        if (out != null) send("EXIT");
        try {
            if (socket != null) socket.close();
        } catch (IOException e) {
            // already closed
        }
    }
}
