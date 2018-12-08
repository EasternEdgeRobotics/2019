import json
from flask import Blueprint, Flask, render_template, jsonify, request
from TopsidesGlobals import GLOBALS

control_api = Blueprint("control_api", __name__)

topsidesComms = None

def controlAPI(comms):
    global topsidesComms
    topsidesComms = comms
    return control_api

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

@inputs:
    {JSON} Parsed data - example: {sway:0.563, surge:0.231, yaw: 0, etc....}
                       - all types of controls are in the controls.json
"""
@control_api.route("/sendControlValues", methods=["POST"])
def sendControlValues():
    try:
        data = request.json
        v = data["heave"]
        port = GLOBALS["thrusterPorts"]["fore-port-vert"]
        print(port)
        topsidesComms.send.put("fControl.py " + str(port) + " " + str(v))
        print(v)
        return "good"
    except(Exception):
        return "error"



