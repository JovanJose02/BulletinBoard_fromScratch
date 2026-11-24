# Bulletin board Makefile
# make         compile the Java client
# make server  start the server (make server PORT=7000 for another port)
# make client  start the console client
# make gui     start the GUI
# make clean   remove compiled files

PORT ?= 6789

all: Client.class

Client.class: Client.java
	javac Client.java

server:
	python3 server.py $(PORT)

client: Client.class
	java Client

gui: Client.class
	python3 gui.py

clean:
	rm -f *.class
	rm -rf __pycache__

.PHONY: all server client gui clean
