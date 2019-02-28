"""Communicate from server to raspberry pi."""
import socket
import sys
import queue
import threading
from TopsidesGlobals import GLOBALS

ipSendThruster = '255.255.255.255'
portSendThruster = GLOBALS['portSendThruster']
ipSendSensor = '255.255.255.255'
portSendSensor = GLOBALS['portSendSensor']
ipHost = '0.0.0.0'
portHost = GLOBALS['portHost']

received = queue.Queue()
# Try opening a socket for communication
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
except socket.error:
    print("Failed To Create Socket")
    sys.exit()
except Exception as e:
    print("failed")
# Bind the ip and port of topsides to the socket and loop coms
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((ipHost, portHost))
s.sendto(("register").encode('utf-8'), (ipSendThruster, portSendThruster))
s.sendto(("register").encode('utf-8'), (ipSendSensor, portSendSensor))
data, addr = s.recvfrom(1024)
data = data.decode("utf-8")
if data == "sensorPi":
    print("Sensor Pi: " + str(addr))
    ipSendSensor = addr
elif data == "thrusterPi":
    print("Thruster Pi: " + str(addr))
    ipSendThruster = addr
data, addr = s.recvfrom(1024)
data = data.decode("utf-8")
if data == "sensorPi":
    print("Sensor Pi: " + str(addr))
    ipSendSensor = addr
elif data == "thrusterPi":
    print("Thruster Pi: " + str(addr))
    ipSendThruster = addr

# Queue to hold send commands to be read by simulator
simulator = queue.Queue()


# This function sends data to the ROV
def sendData(inputData):
    global s
    s.sendto(inputData.encode('utf-8'), (ipSend, portSend))


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
    command = input()
    while command != "exit":
        sendData(command)
        command = input()
    sendData(command)
    while t.is_alive():
        continue
