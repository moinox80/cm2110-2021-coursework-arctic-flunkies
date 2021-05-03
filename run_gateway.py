import gateway
import threading
import time

gw = gateway.Gateway()

while True:
    """command = input("Please enter a command ")
    command = command.split(" ")

    if command[0] == "send":
        gw.send_to_feed(command[1], command[2])
    elif command[0] == "get":
        print(gw.data(command[1]))"""