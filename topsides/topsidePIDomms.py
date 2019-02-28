"""Communicate from server to raspberry pi"""
import socket
import sys
import queue
import serial
import syslog
import time
import math
import threading
sys.path.append('../raspi/libraries')
import maestro
from pidh import pid

from TopsidesGlobals import GLOBALS
#import topsidesComms


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
    s.sendto(inputData.encode('utf-8'), ("192.168.88.5", portSend))

# TESTING
def sendDataB(inputData):
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
        #print(outputData, ' sssssss')
        keep.append(outputData)
        #print(keep[-1])
        #received.put(outputData)


def putMessage(msg):
    sendData(msg)
    simulator.put(msg, timeout=0.005)


def chechFourthFirstQuad(angle_1, angle_2):
    if(angle_1 > 260 and angle_2 < 100):
        return True
    elif(angle_2 > 260 and angle_1 < 100):
        return True
    return False

""" Create objects for each component """

depth = pid()
angular = pid()
pitch = pid()
yaw = pid()
row = pid()

""" initialize the different PID components """

def depth_PID_init():
    depth.kP = 0.295 ## don't go any higher than 0.9 otherwise, oscillation increases by about 10%
    depth.kI = 0.099
    depth.kD = 0.185
    depth.integral = 0.0

def yaw_PID_init():
    yaw.kP = 0.0099 ## 0.0082
    yaw.kI = 0.000043 ## 0.000043
    yaw.kD = 0.005 ## 0.003
    yaw.integral = 0.0

def row_PID_init():
    row.kP = 0.0099 ## 0.0082
    row.kI = 0.000043 ## 0.000043
    row.kD = 0.005 ## 0.003
    row.integral = 0.0

def pitch_PID_init():
    pitch.kP = 0.0099 ## 0.0082
    pitch.kI = 0.000043 ## 0.000043
    pitch.kD = 0.005 ## 0.003
    pitch.integral = 0.0

""" Calculate the different power required for each component
    Note that each of these algorithm have differences based on which component is being used
    errors are Calculated differently
""""

def runDepthPID(cDepth):

    depth_PID_init() ## initialize PID constants
    depth.intError = 0.5 ## increases or decrease based on magnitude of oscillation
    depth.error = depth.target - abs(cDepth) ## Keep current depth at an absolute value

    ## increase integral if the error does not zero out as power decreases
    if(abs(depth.error) < depth.intError):
        depth.integral += 0.5
    else:
        depth.integral = 0

    depth.integral = 0 if depth.error == 0 else depth.integral
    depth.derivative = depth.error - depth.last_error
    depth.last_error = depth.error

    power = (depth.error*depth.kP)+(depth.integral*depth.kI)+(depth.derivative*depth.kD)

    print('Power = ',power, "Error = ",depth.error, "Current D = ",cDepth, "target = ", depth.target)
    return power;



def runYawPID(angle):

    yaw_PID_init();
    yaw.intError = 15

    if(chechFourthFirstQuad(angle, yaw.target)):
        if(angle > 260):
            yaw.error = (angle-360) - yaw.target
        else:
            yaw.error = angle + (360 - yaw.target)
    else:
        yaw.error = yaw.target - abs(angle) ## Keep current depth at an absolute value

    ## increase integral if the error does not zero out as power decreases
    if(abs(yaw.error) < yaw.intError):
        yaw.integral += 0.03
    else:
        yaw.integral = 0

    yaw.integral = 0 if yaw.error == 0 else yaw.integral
    yaw.derivative = yaw.error - yaw.last_error
    yaw.last_error = yaw.error

    power = (yaw.error*yaw.kP) + (yaw.integral*yaw.kI) + (yaw.derivative*yaw.kD)
    if(angle > 180):
        power*=-1
    print('Power = ',power, "Error = ",yaw.error, "Current yaw = ",angle, "target = ", yaw.target)
    return power


def runRowPID(angle):

    row_PID_init();
    row.intError = 15

    if(chechFourthFirstQuad(angle, row.target)):
        if(angle > 260):
            row.error = (angle-360) - row.target
        else:
            row.error = angle + (360 - row.target)
    else:
        row.error = row.target - abs(angle)

    if(abs(row.error) < row.intError):
        row.integral += 0.03
    else:
        row.integral = 0

    row.integral = 0 if row.error == 0 else row.integral
    row.derivative = row.error - row.last_error
    row.last_error = row.error

    power = (row.error*row.kP) + (row.integral*row.kI) + (row.derivative*row.kD)
    if(angle > 180):
        power*=-1
    print('Power = ',power, "Error = ",row.error, "Current Row = ",angle, "target = ", row.target)
    return power





def runPitchPID(angle):

    pitch_PID_init();
    pitch.intError = 15

    pitch.error = pitch.target - angle

    if(abs(pitch.error) < pitch.intError):
        pitch.integral += 0.05
    else:
        pitch.integral = 0

    pitch.integral = 0 if pitch.error == 0 else pitch.integral
    pitch.derivative = pitch.error - pitch.last_error
    pitch.last_error = pitch.error

    power = (pitch.error*pitch.kP) + (pitch.integral*pitch.kI) + (pitch.derivative*pitch.kD)
    if(angle > 180):
        power*=-1
    print('Power = ',power, "Error = ",pitch.error, "Current D = ",angle, "target = ", pitch.target)
    return power;



# Setup threading for receiving data
t = threading.Thread(target=receiveData)
t.start()


""" Select the different thruster vectors for each component """"

def selectThrusters(choice, power):
    if choice == 1:
        return {
           "fore-port-vert": -power,
           "fore-star-vert": -power,
           "aft-port-vert": power,
           "aft-star-vert": power
           }
    elif choice == 2:
        return {
           "fore-port-horz": power,
           "fore-star-horz": power,
           "aft-port-horz": power,
           "aft-star-horz": -power
           }

    elif choice == 3:
        return {
            "fore-port-vert": power,
            "fore-star-vert": -power,
            "aft-port-vert": -power,
            "aft-star-vert": power
        }

    elif choice == 4:
        return {
            "fore-port-vert": power,
            "fore-star-vert": power,
            "aft-port-vert": power,
            "aft-star-vert": power
        }


if __name__ == "__main__":

    run = False
    choice = int(input("Which input which PID: \n Depth : 1 \n Yaw : 2 \n Row : 3 \n Pitch : 4"))
    thrusterData = {}

    if choice == 1:
        depth.target = float(input("Input Target Depth: "))
    elif choice == 2:
        yaw.target = float(input("Input Target Yaw angle: "))
    elif choice == 3:
        row.target = float(input("Input Target Row angle: "))
    elif choice == 4:
        pitch.target = float(input("Input Target Pitch angle: "))

    if (choice >= 1) && (choice <= 4):
        run = True
        
    while run:
        sendDataB('readSerialArd.py')
        try:

            power = 0.0

            if choice == 1:
                power = runDepthPID(float(keep[-1]))
            elif choice == 2:
                power = runYawPID(float(keep[-1]))
            elif choice == 3:
                power = runRowPID(float(keep[-1]))
            elif choice == 4:
                power = -runPitchPID(float(keep[-1]))

            if(power > 1.0):
                power = 0.3
            elif(power < -1.0):
                power = -0.3

            thrusterData = selectThrusters(choice, power)

            for control in thrusterData:
                val = thrusterData[control]
                putMessage("fControl.py " + str(GLOBALS["thrusterPorts"][control]) + " " + str(val))
            print("good")

        except(Exception):
            print(Exception)
            continue;
