"""GUI."""
from flask import Blueprint, render_template, jsonify, request

import math
import time
import sys
sys.path.append('../raspi/libraries')
import maestro
from pidh import pid


gui_api = Blueprint("gui_api", __name__)


@gui_api.route("/gui")
def returnGuiPage():
    """
    Return page for the control gui.

    :return: rendered gui.html web page
    """
    return render_template("gui.html")


@gui_api.route('/guislider', methods=['POST'])
def getSliderValues():
    """
    Gets the values from the 6 degrees of power gui sliders.

    Input: {slider: string, value: int}

    POST method
    """
    # ['value'] = value of slider (0-10 currently)
    # ['slider'] = which slider (Yaw, Pitch, etc.)
    data = request.json
    print(data['slider'])
    print(data['value'])
    return jsonify("")



depth = pid(); ## make a depth object of the pid class
## initialize depth pid constants


"""  PID constants must be tuned to prevent oscillation"""
def depth_PID_init():
    depth.kP = 0.00845 ## don't go any higher than 0.009 otherwise, oscillation increases by about 10%
    depth.kI = 0.000554
    depth.kD = 0.00015



def depth_PID():

    depth_PID_init() ## initialize PID constants
    intError = 20 ## increases or decrease based on magnitude of oscillation
    depth.error = depth.target - abs(cDepth) ## Keep current depth at an absolute value

    ## increase integral if the error does not zero out as power decreases
    if(abs(depth.error) < intError):
        depth.integral += 10
    else:
        depth.integral = 0

    depth.integral = 0 if depth.error == 0 else depth.integral
    depth.derivative = depth.error - depth.last_error
    depth.last_error = depth.error

    power = (depth.error*depth.kP)+(depth.integral*depth.kI)+(depth.derivative*depth.kD)

    print('Power = ',power, "Error = ",depth.error, "Current D = ",cDepth, "target = ", depth.target)
    return power;


@gui_api.route('/autoDepth', methods=['POST'])
def getAndSendVals():
    power = 0.0
    depth.error = 0#int(sys.argv[1]); ## Get current depth
    depth.target = 0#int(sys.argv[2]); ## Get the target depth value

    power = depth_PID()
    setThruster = [0.0,0.0,0.0,0.0,power,power,power,power]
    print(power)
    ## send to thrusters now
    for x in range(len(setThruster)):
        topsidesComms.send.put("fControl.py " + str(x) + " " + str(setThruster[x]))
    return jsonify("lol");
