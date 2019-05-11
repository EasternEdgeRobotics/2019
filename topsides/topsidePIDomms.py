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
def receiveData(flag):
    global s
    while True:
        outputData, addr = s.recvfrom(1024)
        outputData = outputData.decode("utf-8")
        if (outputData == "exit"):
            break
        received.put(outputData)
        if flag.is_set():
            break


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
pitch = pid()
yaw = pid()
roll = pid()

""" initialize the different PID components """

def depth_PID_init():
    depth.kP = 1.25 ## don't go any higher than 0.9 otherwise, oscillation increases by about 10%
    depth.kI = 0.099
    depth.kD = 0.285
    depth.integral = 0.0

def yaw_PID_init():
    yaw.kP = 0.0099
    yaw.kI = 0.000043
    yaw.kD = 0.005
    yaw.integral = 0.0

def roll_PID_init():
    roll.kP = 0.013
    roll.kI = 0.09
    roll.kD = 0.0057
    roll.integral = 0.0

def pitch_PID_init():
    pitch.kP = 0.011
    pitch.kI = 0.075
    pitch.kD = 0.0399
    pitch.integral = 0.0

""" Calculate the different power required for each component
    Note that each of these algorithm have differences based on which component is being used
    errors are Calculated differently
"""

def runDepthPID(cDepth):

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

    if(power > 0.6):
        power = 0.3
    elif(power < -0.6):
        power = -0.3

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
        yaw.error = yaw.target - abs(angle)

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


def runRollPID(angle):

    if(angle < -75):
        angle = -75
    elif(angle > 75):
        angle = 75

    roll_PID_init();
    roll.intError = 15


    roll.error = roll.target - angle

    if(abs(roll.error) < roll.intError):
        roll.integral += 0.05
    else:
        roll.integral = 0

    roll.integral = 0 if roll.error == 0 else roll.integral
    roll.derivative = roll.error - roll.last_error
    roll.last_error = roll.error

    power = (roll.error*roll.kP) + (roll.integral*roll.kI) + (roll.derivative*roll.kD)
    if(angle > 180):
        power*=-1

    if(power > 0.6):
        power = 0.3
    elif(power < -0.6):
        power = -0.3

    print('Power = ', power, " Error = ", roll.error, " Current Roll = ", angle, " Target Roll= ", roll.target)
    return power




def runPitchPID(angle):

    if(angle < -75):
        angle = -75
    elif(angle > 75):
        angle = 75

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

    if(power > 0.6):
        power = 0.3
    elif(power < -0.6):
        power = -0.3

    print('Power = ',power, "Error = ",pitch.error, "Current Pitch = ",angle, "target = ", pitch.target)
    return power;

def getRollAngle():
    decoded_bytes = received.get()
    data = decoded_bytes.split(",")
    return data[3]

def getYawAngle():
    decoded_bytes = received.get()
    data = decoded_bytes.split(",")
    return data[2]

def getPitchAngle():
    decoded_bytes = received.get()
    data = decoded_bytes.split(",")
    return data[4]

def getDepth():
    decoded_bytes = received.get()
    data = decoded_bytes.split(",")
    return data[0]

#
# if __name__ == "__main__":
#
#     run = False
#     choice = int(input("Which input which PID: \n Depth : 1 \n Yaw : 2 \n Roll : 3 \n Pitch : 4 \nPick One: "))
#     thrusterData = {}
#
#     if choice == 1:
#         depth.target = float(input("Input Target Depth: "))
#     elif choice == 2:
#         yaw.target = float(input("Input Target Yaw angle: "))
#     elif choice == 3:
#         roll.target = float(input("Input Target Roll angle: "))
#     elif choice == 4:
#         pitch.target = float(input("Input Target Pitch angle: "))
#
#     if (choice >= 1) and (choice <= 4):
#         run = True
#
#     while run:
#         sendDataB('readSerialArd.py')
#         try:
#
#             power = 0.0
#             sensorVals = parseSensorVals()
#
#             if choice == 1:
#                 print('Running Depth')
#                 power = -runDepthPID(float(sensorVals['depth']))
#             elif choice == 2:
#                 print('Running Yaw')
#                 power = runYawPID(float(sensorVals['gyro_x']))
#             elif choice == 3:
#                 print('Running Roll')
#                 power = runRollPID(float(sensorVals['gyro_y']))
#             elif choice == 4:
#                 print('Running Pitch')
#                 power = -runPitchPID(float(sensorVals['gyro_z']))
#
#             rollPitchControl = {
#                 "fore-port-vert": -runPitchPID(float(sensorVals['gyro_z']))-runRollPID(float(sensorVals['gyro_y'])),
#                 "fore-star-vert": -runPitchPID(float(sensorVals['gyro_z']))+runRollPID(float(sensorVals['gyro_y'])),
#                 "aft-port-vert": runPitchPID(float(sensorVals['gyro_z']))-runRollPID(float(sensorVals['gyro_y'])),
#                 "aft-star-vert": runPitchPID(float(sensorVals['gyro_z']))+runRollPID(float(sensorVals['gyro_y']))
#             }
#
#             if(power > 1.0):
#                 power = 0.3
#             elif(power < -1.0):
#                 power = -0.3
#
#             thrusterData = selectThrusters(choice, power)
#
#             for control in thrusterData:
#                 val = thrusterData[control]
#                 putMessage("fControl.py " + str(GLOBALS["thrusterPorts"][control]) + " " + str(val))
#             print("good")
#
#         except(Exception):
#             print(Exception)
#             continue;

# Setup threading for receiving data
flag = threading.Event()
t = threading.Thread(target=receiveData, args=(flag,))
t.start()


## run pitch and roll together
if __name__ == "__main__":
    sendDataB('readSerialArd.py')
    # roll.target = float(input("Target Roll: "))
    # yaw.target = float(input("Target Yaw: "))
    #pitch.target = float(input("Target Pitch: "))
    try:
        while True:
            try:
                cPitch = getPitchAngle()
                cRoll = getRollAngle()
                cDepth = float(getDepth())/100
            except (IndexError,ValueError):
                continue

            # print(cAngle)

            #power = -runRollPID(float(cRoll))

            # power = runYawPID(float(cAngle))

            # power = -runPitchPID(float(cPitch))

            # if(power > 0.6):
            #     power = 0.3
            # elif(power < -0.6):
            #     power = -0.3

            #roll
            # thrusterData = {
            #     "fore-port-vert": power,
            #     "fore-star-vert": -power,
            #     "aft-port-vert": -power,
            #     "aft-star-vert": power,
            # }

            # yaw

            # thrusterData = {
            #     "fore-port-horz": power,
            #     "fore-star-horz": power,
            #     "aft-port-horz": power,
            #     "aft-star-horz": -power,
            # }

            # pitch
            # thrusterData = {
            #     "fore-port-vert": power,
            #     "fore-star-vert": power,
            #     "aft-port-vert": power,
            #     "aft-star-vert": power,
            # }

            roll.target = -3.5
            pitch.target = 3.2
            # depth.target = 11.10
            #
            # thrusterData = {
            #     "fore-port-vert": (runDepthPID(cDepth)-runPitchPID(float(cPitch))-runRollPID(float(cRoll)))/1.5,
            #     "fore-star-vert": (runDepthPID(cDepth)-runPitchPID(float(cPitch))+runRollPID(float(cRoll)))/1.5,
            #     "aft-port-vert": (-runDepthPID(cDepth)+runPitchPID(float(cPitch))-runRollPID(float(cRoll)))/1.5,
            #     "aft-star-vert": (-runDepthPID(cDepth)+runPitchPID(float(cPitch))+runRollPID(float(cRoll)))/1.5
            # }

            thrusterData = {
                "fore-port-vert": -runPitchPID(float(cPitch))-runRollPID(float(cRoll)),
                "fore-star-vert": -runPitchPID(float(cPitch))+runRollPID(float(cRoll)),
                "aft-port-vert": -runPitchPID(float(cPitch))+runRollPID(float(cRoll)),
                "aft-star-vert": -runPitchPID(float(cPitch))-runRollPID(float(cRoll))
            }


            # power = runDepthPID(cDepth)
            #
            # thrusterData = {
            #     "fore-port-vert": power,
            #     "fore-star-vert": power,
            #     "aft-port-vert": -power,
            #     "aft-star-vert": -power,
            # }

            for control in thrusterData:
                val = thrusterData[control]
                putMessage("fControl.py " + str(GLOBALS["thrusterPorts"][control]) + " " + str(val))
            print("good")
    except KeyboardInterrupt:
        flag.set()
