"""Communicate from server to raspberry pi"""
import socket
import sys
import queue
import time
from TopsidesGlobals import GLOBALS

send = queue.Queue()
received = queue.Queue()


def startComms(start_flag):
    """
    Comms start.

    This function starts the comms and runs the comms loop.
    While the loop is running it will check the send queue for
    messages to send to the ROV. It can send messages back using recieved
    """
    # get ports and local ip address from global file
    portSend = GLOBALS['portSend']
    ipHost = GLOBALS['ipHost']
    portHost = GLOBALS['portHost']

    # try opening a socket for communication
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        # TODO: Change to ouput on gui
        print("Failed To Create Socket")
        sys.exit()
    except Exception as e:
        print("failed")

    # bind the ip and port of topsides to the socket and loop coms
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ipHost, portHost))
    # notify the server that the comms have been started
    start_flag.set()
    while True:
        # TODO: change from getting data from user to getting data from queue
        # send data to the raspi
        ipSend, inputData = send.get()
        s.sendto(inputData.encode('utf-8'), (ipSend, portSend))
        if inputData == "exit":
            break
        # TODO: Change to saving to log file on error
        # receive response from raspi and log if error
        outputData, addr = s.recvfrom(1024)
        outputData = outputData.decode("utf-8")
        print(outputData)
        received.put(outputData)