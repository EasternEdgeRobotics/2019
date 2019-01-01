from flask import Blueprint, Flask, render_template, jsonify, request
import json
import math
from TopsidesGlobals import GLOBALS

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
        trusterData = {
            "fore-port-vert": -data.get("heave", 0) - data.get("pitch", 0) + data.get("roll",0),
            "fore-star-vert": -data.get("heave", 0) - data.get("pitch", 0) - data.get("roll",0),
            "aft-port-vert": -data.get("heave", 0) + data.get("pitch", 0) + data.get("roll",0),
            "aft-star-vert": -data.get("heave", 0) + data.get("pitch", 0) - data.get("roll",0),

            "fore-port-horz": -data.get("surge", 0) + data.get("yaw", 0) + data.get("sway", 0),
            "fore-star-horz": -data.get("surge", 0) - data.get("yaw", 0) - data.get("sway", 0),
            "aft-port-horz": +data.get("surge", 0) - data.get("yaw", 0) + data.get("sway", 0),
            "aft-star-horz": -data.get("surge", 0) - data.get("yaw", 0) + data.get("sway", 0),
        }

        for control in trusterData:
            val = trusterData[control]
            topsidesComms.send.put("fControl.py " + str(GLOBALS["thrusterPorts"][control]) + " " + str(val))
        return "good"
    except(Exception):
        return "error"
