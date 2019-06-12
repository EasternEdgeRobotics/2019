"""Communicate from server to raspberry pi."""
import socket
import sys
import queue
import threading
from TopsidesGlobals import GLOBALS
import botAPI
import topsidePID


# Change IP addresses for a production or development environment
if ((len(sys.argv) > 1) and (sys.argv[1] == "--dev")):
    ipSend4 = GLOBALS['ipSend-4-dev']
    ipSend5 = GLOBALS['ipSend-5-dev']
    ipSendMicro = GLOBALS['ipSendMicro-dev']
    ipHost = GLOBALS['ipHost-dev']
else:
    ipSend4 = GLOBALS['ipSend-4']
    ipSend5 = GLOBALS['ipSend-5']
    ipSendMicro = GLOBALS['ipSendMicro']
    ipHost = GLOBALS['ipHost']

portSend4 = GLOBALS['portSend-4']
portSend5 = GLOBALS['portSend-5']
portSendMicro = GLOBALS['portSendMicro']
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
def sendData(inputData, location = "raspi-5"):
    global s
    if (location == "micro"):
        s.sendto(inputData.encode('utf-8'), (ipSendMicro, portSendMicro))
    elif (location == "raspi-4"):
        s.sendto(inputData.encode('utf-8'), (ipSend4, portSend4))
    else:
        s.sendto(inputData.encode('utf-8'), (ipSend5, portSend5))
        print("sent " + inputData + " to " + str(ipSend5) + " at " + str(portSend5))


# This function is constantly trying to receive data from the ROV
def receiveData():
    global s
    while True:
        outputData, addr = s.recvfrom(1024)
        outputData = outputData.decode("utf-8")
        if (outputData == "exit"):
            break
        elif("gyro" in outputData):
            args = outputData.split()
            botAPI.data["gyroscope"]["x"] = args[1] #pitch
            botAPI.data["gyroscope"]["y"] = args[2] #roll
            botAPI.data["gyroscope"]["z"] = args[3]
            #botAPI.emitTelemetryData()
            if(botAPI.rotationLock):
                print("locked")
                topsidePID.runPitchAndRollPID(botAPI.data["gyroscope"]["x"], botAPI.data["gyroscope"]["y"])
        elif("accel" in outputData):
            args = outputData.split()
            botAPI.data["accelerometer"]["x"] = args[1]
            botAPI.data["accelerometer"]["y"] = args[2]
            botAPI.data["accelerometer"]["z"] = args[3]
            #botAPI.emitTelemetryData()

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
        if command == "motors open":
            sendData("leftmotor open", "raspi-4")
            sendData("rightmotor open", "raspi-4")
        elif command == "motors close":
            sendData("leftmotor close", "raspi-4")
            sendData("rightmotor close", "raspi-4")
        else:
            sendData(command, "raspi-4")
        command = input()
    sendData(command)
    while t.is_alive():
        continue
