"""Communicate from server to raspberry pi."""
import socket
import sys
import queue
import threading
from TopsidesGlobals import GLOBALS

# Change IP addresses for a production or development environment
if ((len(sys.argv) > 1) and (sys.argv[1] == "--dev")):
    ipSend = GLOBALS['ipSend-dev']
    ipHost = GLOBALS['ipHost-dev']
else:
    ipSend = GLOBALS['ipSend']
    ipHost = GLOBALS['ipHost']

portSend = GLOBALS['portSend']
portHost = GLOBALS['portHost']

received = queue.Queue()
# Try opening a socket for communication
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print("Failed To Create Socket")
    sys.exit()
except Exception as e:
    print("failed")
# Bind the ip and port of topsides to the socket and loop coms
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((ipHost, portHost))

# Queue to hold send commands to be read by simulator
simulator = queue.Queue()


# This function sends data to the ROV
def sendData(inputData):
    global s
    s.sendto(inputData.encode('utf-8'), (ipSend, portSend))


keep = [0]

# This function is constantly trying to receive data from the ROV
def receiveData():
    global s
    while True:
        outputData, addr = s.recvfrom(1024)
        outputData = outputData.decode("utf-8")
        if (outputData == "exit"):
            break
        print(outputData)
        received.put(outputData)


def putMessage(msg):
    sendData(msg)
    simulator.put(msg, timeout=0.005)


# Setup threading for receiving data
t = threading.Thread(target=receiveData)
t.start()

if __name__ == "__main__":
    import time
    for x in range(0,100):
        sendData(input())
        time.sleep(1);
