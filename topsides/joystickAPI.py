"""Joystick controls."""
from flask import Blueprint, jsonify, request

joystick_api = Blueprint("joystick_api", __name__)
topsidesComms = None

def joystickAPI(comms):
    global topsidesComms
    topsidesComms = comms
    return joystick_api


def setThrusterValues(tDirect, tPos):
    """Set the thruster values."""
    F = 0.5
    B = -0.5
    C = 0.0

    setThruster = [C, C, C, C, C, C]

    if(tDirect == "Surge" and tPos == 1):
        setThruster = [B, F, B, F, C, C]
    elif(tDirect == "Surge" and tPos == -1):
        setThruster = [F, B, F, B, C, C]
    elif(tDirect == "Sway" and tPos == 1):
        setThruster = [B, B, B, B, C, C]
    elif(tDirect == "Sway" and tPos == -1):
        setThruster = [F, F, F, F, C, C]
    elif(tDirect == "Heave" and tPos == 1):
        setThruster = [C, C, C, C, B, F]
    elif(tDirect == "Heave" and tPos == -1):
        setThruster = [C, C, C, C, F, B]
    elif(tDirect == "Pitch" and tPos == 1):
        setThruster = [C, C, C, C, F, F]
    elif(tDirect == "Pitch" and tPos == -1):
        setThruster = [C, C, C, C, B, B]
    elif(tDirect == "Yaw" and tPos == 1):
        setThruster = [F, B, B, F, C, C]
    elif(tDirect == "Yaw" and tPos == -1):
        setThruster = [B, B, F, B, C, C]
    elif(tDirect == "All" and tPos == 0):
        setThruster = [C, C, C, C, C, C]
    else:
        # This should never run. Error should be sent to the dev page when it has an error log
        setThruster = [C, C, C, C, C, C]
    return setThruster


@joystick_api.route("/joystickValue", methods=["POST"])
def getJoytickValuesFromJavascript():
    global topsidesComms
    """
    Simple joystick input reciever.

    Input: Json Body Format: {slider: string, direction: int}

    POST method
    """
    data = request.json
    # store the thruster values in a list
    setThruster = setThrusterValues(data['slider'], int(data['direction']))
    print(setThruster)
    # call the fControl rov file and pass it [port, value]
    for x in range(len(setThruster)):
        # This will most likely produce a file path error
        topsidesComms.send.put("fControl.py " + str(x) + " " + str(setThruster[x]))

    return jsonify("lol")  # returns lol in json as filler (server crashes if nothing is returned)
