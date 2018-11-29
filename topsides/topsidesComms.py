"""Communicate from server to raspberry pi"""
import socket
import sys
import queue
from TopsidesGlobals import GLOBALS

send = queue.Queue()
received = queue.Queue()


def startComms():
    """
    Comms start.

    This function starts the comms and runs the comms loop.
    While the loop is running it will check the send queue for
    messages to send to the ROV. It can send messages back using recieved
    """
    # TODO: Change to raspi ip
    ipSend = GLOBALS['ipSend']
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
    received.put("bound")
    while True:
        # TODO: change from getting data from user to getting data from queue
        # send data to the raspi
        inputData = input()
        s.sendto(inputData.encode('utf-8'), (ipSend, portSend))
        if inputData == "exit":
            break
        # TODO: Change to saving to log file on error
        # receive response from raspi and log if error
        outputData, addr = s.recvfrom(1024)
        outputData = outputData.decode("utf-8")
        print(outputData, file=sys.stderr)
        received.put(outputData)

startComms()