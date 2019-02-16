"""Communicate from server to raspberry pi"""
import socket
import sys
import queue
import serial
import syslog
import time
import math
sys.path.append('../raspi/libraries')
import maestro
from pidh import pid

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





send = queue.Queue()
received = queue.Queue()

depth = pid(); ## make a depth object of the pid class
angular = pid();
## initialize depth pid constants

#The following line is for serial over GPIO
port = '/dev/cu.usbmodem14201'

"""  PID constants must be tuned to prevent oscillation"""
def depth_PID_init():
    depth.kP = 0.775 ## don't go any higher than 0.9 otherwise, oscillation increases by about 10%
    depth.kI = 0.0454
    depth.kD = 0.025

## .88.2

def depth_PID(cDepth):

    depth_PID_init() ## initialize PID constants
    depth.intError = 0.5 ## increases or decrease based on magnitude of oscillation
    depth.error = depth.target - abs(cDepth) ## Keep current depth at an absolute value

    ## increase integral if the error does not zero out as power decreases
    if(abs(depth.error) < depth.intError):
        depth.integral += 0.03
    else:
        depth.integral = 0

    depth.integral = 0 if depth.error == 0 else depth.integral
    depth.derivative = depth.error - depth.last_error
    depth.last_error = depth.error

    power = (depth.error*depth.kP)+(depth.integral*depth.kI)+(depth.derivative*depth.kD)

    print('Power = ',power, "Error = ",depth.error, "Current D = ",cDepth, "target = ", depth.target)
    return power;


def angular_PID_init():
    angular.KP = 0.0
    angular.KI = 0.0
    angular.kD = 0.0

def angular_PID(angle):

    angular_PID_init();
    angular.intError = 20

    angular.error = angular.target - abs(angle) ## Keep current depth at an absolute value

    ## increase integral if the error does not zero out as power decreases
    if(abs(angular.error) < angular.intError):
        angular.integral += 5
    else:
        angular.integral = 0

    angular.integral = 0 if angular.error == 0 else angular.integral
    angular.derivative = angular.error - angular.last_error
    angular.last_error = angular.error

    power = (angular.error*angular.kP)+(angular.integral*angular.kI)+(angular.derivative*angular.kD)

    print('Power = ',power, "Error = ",depth.error, "Current D = ",cDepth, "target = ", depth.target)
    return power;




def run_angular_PID(yaw=None, pitch=None, roll=None):

    if(yaw != None):
        angular.target = yaw
        ## run rov now

        while True:
            c_yaw = float(startComms(["192.168.88.4","getGyro.py"]));
            power = angular_PID(c_yaw);

            print('power: '+power)

            setThruster = [-power,-power,-power,0.0,0.0,-power,0.0,0.0] ## wrong ports right now
            for x in range(len(setThruster)):
                startComms(["192.168.88.5","fControl.py " + str(x) + " " + str(setThruster[x])])

    elif(pitch != None):
        angular.target = pitch
        ## run rov now

        while True:
            c_pitch = float(startComms(["192.168.88.4","getGyro.py"]));
            power = angular_PID(c_pitch);

            print('power: '+power)

            setThruster = [-power,-power,-power,0.0,0.0,-power,0.0,0.0] ## wrong ports right now
            for x in range(len(setThruster)):
                startComms(["192.168.88.5","fControl.py " + str(x) + " " + str(setThruster[x])])

    elif(roll != None):

        angular.target = roll
        ## run rov now

        while True:
            c_roll = float(startComms(["192.168.88.4","getGyro.py"]));
            power = angular_PID(c_roll);

            print('power: '+power)

            setThruster = [-power,-power,-power,0.0,0.0,-power,0.0,0.0] ## wrong ports right now
            for x in range(len(setThruster)):
                startComms(["192.168.88.5","fControl.py " + str(x) + " " + str(setThruster[x])])


def getAndSendVals():
    depth.target = float(input("Input target: "))
    cDepth = float(startComms(["192.168.88.4","readSerialArd.py"]));
    while True:
        ## get pressure sensor value
        cDepth = float(startComms(["192.168.88.4","readSerialArd.py"]));

        power = 0.0

        power = depth_PID(cDepth)
        setThruster = [-power,-power,-power,0.0,0.0,-power,0.0,0.0]
        print(power)


        ## send to thrusters now
        for x in range(len(setThruster)):
            startComms(["192.168.88.5","fControl.py " + str(x) + " " + str(setThruster[x])])


# Setup threading for receiving data
t = threading.Thread(target=receiveData)
t.start()

if __name__ == "__main__":
    while 1:
        sendData("readSerialArd.py")
        cDepth = received.get()

        power = 0.0

        power = depth_PID(cDepth)
        setThruster = [-power,-power,-power,0.0,0.0,-power,0.0,0.0]
        print(power)


        ## send to thrusters now
        for x in range(len(setThruster)):
            sendData(["192.168.88.5","fControl.py " + str(x) + " " + str(setThruster[x])])
