"""Control Software for MATE 2019."""
from flask import Flask, render_template, jsonify, request
import json
import random
import profileHandle
import topsidesComms
import threading

app = Flask(__name__)

t = threading.Thread(target=topsidesComms.startComms)


@app.route("/")
def returnGui():
    """
    Base url and table of contents.

    :return: rendered index.html web page
    """
    return render_template("index.html")


@app.route("/editprofile")
def editProfilePage():
    """
    Return page for control profile edit.

    :return: rendered controlProfileEdit.html web page
    """
    profiles = profileHandle.loadProfiles()
    return render_template("controlProfileEdit.html", profiles=profiles)


def setThrusterValues(tDirect, tPos):
    """Set the thruster values."""
    F = 0.5
    B = -0.5
    C = 0.0

    setThruster = [C, C, C, C, C, C]

    if(tDirect == "Surge" and tPos == 1):
        setThruster = [F, B, B, F, C, C]
    elif(tDirect == "Surge" and tPos == -1):
        setThruster = [B, F, F, B, C, C]
    elif(tDirect == "Sway" and tPos == 1):
        setThruster = [F, F, B, B, C, C]
    elif(tDirect == "Sway" and tPos == -1):
        setThruster = [B, B, F, F, C, C]
    elif(tDirect == "Heave" and tPos == 1):
        setThruster = [C, C, C, C, F, F]
    elif(tDirect == "Heave" and tPos == -1):
        setThruster = [C, C, C, C, B, B]
    elif(tDirect == "Pitch" and tPos == 1):
        setThruster = [C, C, C, C, F, B]
    elif(tDirect == "Pitch" and tPos == -1):
        setThruster = [C, C, C, C, B, F]
    elif(tDirect == "Yaw" and tPos == 1):
        setThruster = [F, B, F, B, C, C]
    elif(tDirect == "Yaw" and tPos == -1):
        setThruster = [B, F, B, F, C, C]
    elif(tDirect == "All" and tPos == 0):
        setThruster = [C, C, C, C, C, C]
    else:
        # This should never run. Error should be sent to the dev page when it has an error log
        setThruster = [C, C, C, C, C, C]
    return setThruster


@app.route("/joystickValue", methods=["POST"])
def getJoytickValuesFromJavascript():
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


@app.route("/runscript", methods=["POST"])
def getScriptValuesFromJavascript():
    """
    Simple script name reciever to run on raspberry pi.

    Input: Json Body Format: scriptname

    POST method
    """
    data = request.json

    print(data)

    topsidesComms.send.put("scripts.py " + data)

    return jsonify("")  # returns json as filler (server crashes if nothing is returned)


@app.route("/getProfiles", methods=["GET"])
def getProfiles():
    """
    Returns the control profiles from memory as json.

    GET method

    :return: Json containing all profiles
    """
    return json.dumps(profileHandle.loadProfiles())  # responds json containing all profiles


@app.route("/deleteProfile", methods=["POST"])
def deleteProfile():
    """
    Deletes the requested profile from memory.

    Input: Json Body Format: {id: int}

    POST method

    :return: string "Failed, profileID not read correct or is not a number" or "success"
    """
    profileID = request.args.get('profileID')
    if(profileID is None):
        return "Failed, profileID not read correct or is not a number"
    else:
        profileHandle.deleteProfile(int(profileID))
        return "success"


@app.route("/testGetPressure")
def testGetPressure():
    """
    Returns a random value simulating a pressure sensor.

    GET method

    :return: random int value simulating a pressure sensor
    """
    value = random.randint(99, 105)
    return json.dumps(value)


@app.route("/gui")
def returnGuiPage():
    """
    Return page for the control gui.

    :return: rendered gui.html web page
    """
    return render_template("gui.html")


@app.route('/guislider', methods=['POST'])
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


@app.route("/dev")
def returnDevPage():
    """
    Return page for the development input.

    :return: rendered dev.html web page
    """
    return render_template("dev.html")


@app.route('/devinput', methods=['POST'])
def getDevInput():
    """
    Gets the values from the dev input.

    Input: string

    POST method
    """
    # devData is the variable the stores the data submitted from the webpage.
    # it is printed out to console for testing purposes.
    devData = request.json
    print(devData)
    return jsonify("")


"""
Server start.
This is a standard python function that is True when this file is called from the command line (python3 main.py)
(This statement is false for calls to the server)
"""
if __name__ == "__main__":
    t.start()
    if topsidesComms.received.get() == "bound":
        app.run(debug=True, host='0.0.0.0', use_reloader=True, port=80)
