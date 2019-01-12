import json
from flask import Blueprint, Flask, render_template, jsonify, request
from TopsidesGlobals import GLOBALS
import math

control_api = Blueprint("control_api", __name__)

topsidesComms = None

def controlAPI(comms):
    global topsidesComms
    topsidesComms = comms
    return control_api


@control_api.after_request
def afterRequest(response):
    response.headers.add('Access-Control-Allow-Origin', "*")
    response.headers.add('Access-Control-Allow-Headers', "Content-Type,Authorization")
    response.headers.add('Access-Control-Allow-Methods', "GET,POST,PUT,DELETE,OPTIONS")
    return response

"""
getControlOptions
GET

returns the control possibilities for mapping gamepads. This function loads the JSON file controls.json
"""
@control_api.route("/getControlOptions", methods=["GET"])
def getControlOptions():
    try:
        with open("json/controls.json") as file:
            data = json.load(file)
            return json.dumps(data)
    except Exception as e:
        return json.dumps("Problem loading json: " + str(e))


@control_api.route("/testControls")
def loadControlTestPage():
    return(render_template("controlTest.html"))



"""
sendControlValues
POST

parsed control values are sent to the server and eventually to the bot
Thruster Vectoring done here

@inputs:
    {JSON} Parsed data - example: {sway:0.563, surge:0.231, yaw: 0, etc....}
                       - all types of controls are in the controls.json
"""
@control_api.route("/sendControlValues", methods=["POST"])
def sendControlValues():
    try:
        data = request.json
        print("1")
        #TODO: THRUSTER VECTORING, current stuff is placeholder
        #.get(<index>, <default value if key doesn't exist>)

        """
          +heave
            ^
            |
            |
            O - - > +sway
        -surge

        """

        heave = data.get("heave", data.get("heave_up", 0) - data.get("heave_down", 0))
        pitch = data.get("pitch", data.get("pitch_up", 0) - data.get("pitch_down", 0))
        roll = data.get("roll", data.get("roll_cw", 0) - data.get("roll_ccw", 0))
        surge = data.get("surge", data.get("surge_forewards", 0) - data.get("surge_bakcwards", 0))
        yaw = data.get("yaw", data.get("yaw_cw", 0) - data.get("yaw_ccw", 0))
        sway = data.get("sway", data.get("sway_right", 0) - data.get("sway_left", 0))

        """
        Handling Movement Axes Controls
        """
        thrusterData = {
            "fore-port-vert": -heave - pitch + roll,
            "fore-star-vert": -heave - pitch - roll,
            "aft-port-vert": -heave + pitch + roll,
            "aft-star-vert": -heave + pitch - roll,

            "fore-port-horz": -surge + yaw + sway,
            "fore-star-horz": -surge - yaw - sway,
            "aft-port-horz": +surge - yaw + sway,
            "aft-star-horz": -surge - yaw + sway,
        }

        for control in thrusterData:
            val = thrusterData[control]
            topsidesComms.putMessage("fControl.py " + str(GLOBALS["thrusterPorts"][control]) + " " + str(val))
        return "good"



    except(Exception):
        return "error"
