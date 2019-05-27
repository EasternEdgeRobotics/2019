"""Control API."""
from flask import Blueprint, render_template, request
import json
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


@control_api.route("/getControlOptions", methods=["GET"])
def getControlOptions():
    """
    getControlOptions.

    GET

    This function loads the JSON file controls.json
    :return: the control possibilities for mapping gamepads.
    """
    try:
        with open("json/controls.json") as file:
            data = json.load(file)
            return json.dumps(data)
    except Exception as e:
        return json.dumps("Problem loading json: " + str(e))


@control_api.route("/testControls")
def loadControlTestPage():
    return(render_template("controlTest.html"))


@control_api.route("/sendControlValues", methods=["POST"])
def sendControlValues():
    """
    Parsed control values are sent to the server and eventually to the bot.

    Thruster Vectoring done here

    POST

    +heave
        ^
        |
        |
        O - - > +sway
    -surge

    Input:
        {JSON} Parsed data - example: {sway:0.563, surge:0.231, yaw: 0, etc....}
                           - all types of controls are in the controls.json
    """
    try:
        data = request.json
        #print("1")
        # .get(<index>, <default value if key doesn't exist>)

        heave = data.get("heave", data.get("heave_up", data.get("heave_down", 0))) * GLOBALS["thrusterSafety"]
        pitch = data.get("pitch", data.get("pitch_up", data.get("pitch_down", 0))) * GLOBALS["thrusterSafety"]
        roll = data.get("roll", data.get("roll_cw", data.get("roll_ccw", 0))) * GLOBALS["thrusterSafety"]
        surge = data.get("surge", data.get("surge_forewards", data.get("surge_backwards", 0))) * GLOBALS["thrusterSafety"]
        yaw = data.get("yaw", data.get("yaw_cw", data.get("yaw_ccw", 0))) * GLOBALS["thrusterSafety"]
        sway = data.get("sway", data.get("sway_right", data.get("sway_left", 0))) * GLOBALS["thrusterSafety"]
        rotateCam1 = data.get("rotateCam1")
        rotateCam2 = data.get("rotateCam2")
        
        smartPitch = data.get("smart_pitch", 0)
        smartRoll = data.get("smart_roll", 0)

        claws = data.get("claws", 0)
        light = data.get("light", 0)
        trought_fly = data("trout_fly", 0)

        # Handling Movement Axes Controls
        thrusterData = {
            "fore-port-vert": +heave + ((abs(pitch) if pitch < 0 else 0) if smartPitch else -pitch) + ((abs(roll) if roll < 0 else 0) if smartRoll else -roll),
            "fore-star-vert": +heave + ((abs(pitch) if pitch < 0 else 0) if smartPitch else -pitch) + ((abs(roll) if roll < 0 else 0) if smartRoll else roll),
            "aft-port-vert": -heave + ((-abs(pitch) if pitch > 0 else 0) if smartPitch else -pitch) + ((abs(roll) if roll < 0 else 0) if smartRoll else roll),
            "aft-star-vert": -heave + ((-abs(pitch) if pitch > 0 else 0) if smartPitch else -pitch) + ((abs(roll) if roll < 0 else 0) if smartRoll else -roll),

            "fore-port-horz": -surge + yaw + sway,
            "fore-star-horz": +surge + yaw + sway,
            "aft-port-horz": -surge + yaw - sway,
            "aft-star-horz": -surge - yaw + sway,

            "fore-camera": rotateCam1,
            "aft-camera": rotateCam2
        }


        for control in thrusterData:
            print(control + "   " + str(thrusterData))
            val = thrusterData[control]
            topsidesComms.putMessage("runThruster.py " + str(GLOBALS["thrusterPorts"][control]) + " " + str(val))

        topsidesComms.putMessage("claw " + ("close" if claws is 1 else "open"), "raspi-4")
        topsidesComms.putMessage("led.py " + ("100" if light is 1 else "0"))
        topsidesComms.putMessage("pebbles " + ("open" if trought_fly is 1 else "close"), "raspi-4")
            

        
        return "good"

    except(Exception):
        return "error"
