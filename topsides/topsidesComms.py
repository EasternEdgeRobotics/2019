"""Communicate from server to raspberry pi"""
import socket
import sys
import queue
import time
import threading
from TopsidesGlobals import GLOBALS

received = queue.Queue()
# try opening a socket for communication
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #s.settimeout(1)
except socket.error:
    # TODO: Change to ouput on gui
    print("Failed To Create Socket")
    sys.exit()
except Exception as e:
    print("failed")
# bind the ip and port of topsides to the socket and loop coms
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((GLOBALS['ipHost'], GLOBALS['portHost']))

#queue to hold send commands to be read by simulator
simulator = queue.Queue()

def sendData(inputData):
    global s
    s.sendto(inputData.encode('utf-8'), (GLOBALS['ipSend'], GLOBALS['portSend']))
        
def receiveData():
    global s
    while True:
        try:
            print("started")
            outputData, addr = s.recvfrom(1024)
        except socket.timeout as e:
            print('response timeout')
            continue
        outputData = outputData.decode("utf-8")
        print(outputData)
        received.put(outputData)

def putMessage(msg):
    sendData(msg)
    simulator.put(msg, timeout=0.005)

# Setup threading for communications
t = threading.Thread(target=receiveData)
t.start()