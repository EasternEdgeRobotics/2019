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



#The following line is for serial over GPIO
port = '/dev/cu.usbmodem14201'

send = queue.Queue()
received = queue.Queue()

depth = pid(); ## make a depth object of the pid class
## initialize depth pid constants


"""  PID constants must be tuned to prevent oscillation"""
def depth_PID_init():
    depth.kP = 0.775 ## don't go any higher than 0.9 otherwise, oscillation increases by about 10%
    depth.kI = 0.0454
    depth.kD = 0.025

## .88.2

def depth_PID(cDepth):

    depth_PID_init() ## initialize PID constants
    intError = 0.5 ## increases or decrease based on magnitude of oscillation
    depth.error = depth.target - abs(cDepth) ## Keep current depth at an absolute value

    ## increase integral if the error does not zero out as power decreases
    if(abs(depth.error) < intError):
        depth.integral += 0.03
    else:
        depth.integral = 0

    depth.integral = 0 if depth.error == 0 else depth.integral
    depth.derivative = depth.error - depth.last_error
    depth.last_error = depth.error

    power = (depth.error*depth.kP)+(depth.integral*depth.kI)+(depth.derivative*depth.kD)

    print('Power = ',power, "Error = ",depth.error, "Current D = ",cDepth, "target = ", depth.target)
    return power;




def startComms(input):
    """
    Comms start.

    This function starts the comms and runs the comms loop.
    While the loop is running it will check the send queue for
    messages to send to the ROV. It can send messages back using recieved
    """
    # TODO: Change to raspi ip
    ipSend = input[0]
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
    # TODO: change from getting data from user to getting data from queue
    # send data to the raspi
    inputData = input ##send.get()

    s.sendto(inputData[1].encode('utf-8'), (ipSend, portSend))
    # TODO: Change to saving to log file on error
    # receive response from raspi and log if error
    outputData, addr = s.recvfrom(1024)
    outputData = outputData.decode("utf-8")
    print(outputData, file=sys.stderr)
    return outputData


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

getAndSendVals();
