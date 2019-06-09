"""Communicate from server to raspberry pi"""
import queue
import time
import math
import threading
from pidh import pid
from TopsidesGlobals import GLOBALS

keep = [0]
rovInMotion = False
topsidesComms = None

""" Create objects for each component """
depth = pid()
pitch = pid()
yaw = pid()
r = pid()


def setTopsidesComms(comms):
    global topsidesComms
    topsidesComms = comms

def pidInit(comms):
    global topsidesComms
    topsidesComms = comms

def updateTargets(pitchT, rollT, yawT):
    r.target = rollT
    yaw.target = yawT
    pitch.target = pitchT

def chechFourthFirstQuad(angle_1, angle_2):
    if(angle_1 > 260 and angle_2 < 100):
        return True
    elif(angle_2 > 260 and angle_1 < 100):
        return True
    return False


def runThruster(tData):
    for control in tData:
        val = tData[control]
        topsidesComms.putMessage("runThruster.py " + str(GLOBALS["thrusterPorts"][control]) + " " + str(val))
        print("runThruster.py " + str(GLOBALS["thrusterPorts"][control]) + " " + str(val))

""" initialize the different PID components """

def depth_PID_init():
    depth.kP = 1.25 ## don't go any higher than 0.9 otherwise, oscillation increases by about 10%
    depth.kI = 0.099
    depth.kD = 0.285
    depth.integral = 0.0

def yaw_PID_init():
    yaw.kP = 0.011
    yaw.kI = 0.03
    yaw.kD = 0.011
    yaw.integral = 0.0

def roll_PID_init():
    r.kP = 0.0065
    r.kI = 0.0054
    r.kD = 0.0021
    r.integral = 0.0

def pitch_PID_init():
    pitch.kP = 0.0057
    pitch.kI = 0.0109
    pitch.kD = 0.017
    pitch.integral = 0.0

""" Calculate the different power required for each component
    Note that each of these algorithm have differences based on which component is being used
    errors are Calculated differently

    if you want to return the power calculated, set get to TRUE,
    if you want to run only that component, set get to false.
"""

def runDepthPID(cDepth, get):

    depth_PID_init() ## initialize PID constants
    depth.intError = 0.2 ## increases or decrease based on magnitude of oscillation
    depth.error = depth.target - abs(cDepth) ## Keep current depth at an absolute value

    ## increase integral if the error does not zero out as power decreases
    if(abs(depth.error) < depth.intError):
        depth.integral += 0.1
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

    if get: return power

    thrusterData = {
        "fore-port-vert": power,
        "fore-star-vert": power,
        "aft-port-vert": -power,
        "aft-star-vert": -power,
    }

    runThruster(thrusterData)


"""
    @Params:
        angle = (float) current yaw angle
        get = (boolean) true if you want to get calculated power, false if you want to runRoll without returning power
"""
def runYawPID(angle, get):

    yaw_PID_init();
    yaw.intError = 5

    #if(chechFourthFirstQuad(angle, yaw.target)):
    diff = yaw.target - angle
    if diff > 180:
        diff = -(360 - diff)
    elif diff < -180:
        diff = 360 + diff
    yaw.error = diff
        # """if(angle > 260):
        #     yaw.error = (angle-360) - yaw.target
        # else:
        #     yaw.error = angle + (360 - yaw.target)"""
    #else:
    #    yaw.error = yaw.target - abs(angle)

    if(abs(yaw.error) < yaw.intError):
        yaw.integral += 0.05
    else:
        yaw.integral = 0

    yaw.integral = 0 if yaw.error == 0 else yaw.integral
    yaw.derivative = yaw.error - yaw.last_error
    yaw.last_error = yaw.error

    power = (yaw.error*yaw.kP) + (yaw.integral*yaw.kI) + (yaw.derivative*yaw.kD)

    # if power > 0.6: power = 0.3
    # elif power < -0.6: power = -0.3

    print('Power = ',power, "Error = ",yaw.error, "Current yaw = ",angle, "target = ", yaw.target)

    if get: return power

    thrusterData = {
        "fore-port-horz": power,
        "fore-star-horz": power,
        "aft-port-horz": power,
        "aft-star-horz": -power,
    }
    runThruster(thrusterData)


"""
    @Params:
        angle = (float) current roll angle
        get = (boolean) true if you want to get calculated power, false if you want to runRoll without returning power
"""
def runRollPID(angle, get):
    roll_PID_init()

    if(angle < -75):
        angle = -75
    elif(angle > 75):
        angle = 75


    r.intError = 5

    r.error = r.target - angle

    if(abs(r.error) < r.intError):
        r.integral += 0.05
    else:
        r.integral = 0

    r.integral = 0 if r.error == 0 else r.integral
    r.derivative = r.error - r.last_error
    r.last_error = r.error

    power = (r.error*r.kP) + (r.integral*r.kI) + (r.derivative*r.kD)

    power *= -1

    if(power > 0.6):
        power = 0.3
    elif(power < -0.6):
        power = -0.3

    print('Power = ', power, " Error = ", r.error, " Current Roll = ", angle, " Target Roll= ", r.target)
    # print('Power = ', power, " Error = ", r.error, " derivative = ", r.derivative, " integral= ", r.integral)

    if get: return power

    thrusterData = {
        "fore-port-vert": power,
        "fore-star-vert": -power,
        "aft-port-vert": -power,
        "aft-star-vert": power,
    }

    runThruster(thrusterData)


"""
    @Params:
        angle = (float) current pitch angle
        get = (boolean) true if you want to get calculated power, false if you want to runRoll without returning power
"""
def runPitchPID(angle, get):

    if(angle < -75):
        angle = -75
    elif(angle > 75):
        angle = 75

    pitch_PID_init()
    pitch.intError = 10



    pitch.error = pitch.target - angle

    if(abs(pitch.error) < pitch.intError):
        pitch.integral += 0.1
    else:
        pitch.integral = 0

    pitch.integral = 0 if pitch.error == 0 else pitch.integral
    pitch.derivative = pitch.error - pitch.last_error
    pitch.last_error = pitch.error

    power = (pitch.error*pitch.kP) + (pitch.integral*pitch.kI) + (pitch.derivative*pitch.kD)

    power *= -1

    if(power > 0.6):
        power = 0.3
    elif(power < -0.6):
        power = -0.3


    print('Power = ',power, "Error = ",pitch.error, "Current Pitch = ",angle, "target = ", pitch.target, " LE = ", pitch.derivative)

    thrusterData = {
        "fore-port-vert": power,
        "fore-star-vert": power,
        "aft-port-vert": power,
        "aft-star-vert": power,
    }

    if get: return power

    runThruster(thrusterData)

"""
    @Params
        cPitch: pass current pitch angle
        cRoll: pass current roll angle
"""
def runPitchAndRollPID(cPitch, cRoll):
    pch = runPitchPID(float(cPitch), True)
    rl = runRollPID(float(cRoll), True)

    thrusterData = {
        "fore-port-vert": pch+rl,
        "fore-star-vert": pch-rl,
        "aft-port-vert": pch-rl,
        "aft-star-vert": pch+rl
    }

    runThruster(thrusterData)

"""
@Params cPitch, cRoll, cYaw, cDepth
"""
def runAbsoluteLockPID(cPitch, cRoll, cYaw, cDepth):
    pch = runPitchPID(float(cPitch), True)
    rl = runRollPID(float(cRoll), True)
    yw = runYawPID(float(cYaw), True)
    dth = runDepthPID(float(cDepth), True)

    thrusterData = {
        "fore-port-vert": dth+pch+rl,
        "fore-star-vert": dth+pch-rl,
        "aft-port-vert": -dth+pch-rl,
        "aft-star-vert": -dth+pch+rl,
        "fore-port-horz": yw,
        "fore-star-horz": yw,
        "aft-port-horz": yw,
        "aft-star-horz": -yw,

    }

    runThruster(thrusterData)

def getRollAngle():
    decoded_bytes = received.get()
    data = decoded_bytes.split(",")
    return data[4]

def getYawAngle():
    decoded_bytes = received.get()
    data = decoded_bytes.split(",")
    return data[3]

def getPitchAngle():
    decoded_bytes = received.get()
    data = decoded_bytes.split(",")
    return data[5]

def getDepth():
    decoded_bytes = received.get()
    data = decoded_bytes.split(",")
    return data[1]



## run pitch and roll together
if __name__ == "__main__":
    r.target = float(input("Target Roll: "))
    yaw.target = float(input("Target Yaw: "))
    pitch.target = float(input("Target Pitch: "))
    depth.target = float(input("depth: "))  # input format for depth.target must me xx.xx
    while True:
        try:
            cPitch = float(input("Input Pitch: "))
            cRoll = float(input("Input Roll: "))
            cYaw = float(input("Input Yaw: "))
        except (IndexError,ValueError):
            continue

        #runAbsoluteLockPID(float(cPitch), float(cRoll), float(cYaw), cDepth)
        # runDepthPID(cDepth, False)
        runPitchAndRollPID(float(cPitch), float(cRoll))
        # runRollPID(float(cRoll), False)
        #runPitchPID(float(cPitch), False)
