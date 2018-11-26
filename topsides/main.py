"""Control Software for MATE 2019."""
from flask import Flask, render_template, jsonify, request
import json
import random
from profileAPI import profile_api
import topsidesComms
import threading
from TopsidesGlobals import GLOBALS

app = Flask(__name__)

app.register_blueprint(profile_api)

t = threading.Thread(target=topsidesComms.startComms)


@app.route("/")
def returnGui():
    """
    Base url and table of contents.

    :return: rendered index.html web page
    """
    return render_template("index.html")




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



"""
getControlOptions
GET

returns the control possibilities for mapping gamepads. This function loads the JSON file controls.json
"""
@app.route("/getControlOptions", methods=["GET"])
def getControlOptions():
    try:
        with open("json/controls.json") as file:
            data = json.load(file)
            return json.dumps(data)
    except Exception as e:
        return json.dumps("Problem loading json: " + str(e))




"""
/testGetPressure
GET
returns a random value simulating a pressure sensor
"""
@app.route("/testGetPressure")
def testGetPressure():
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
        app.run(debug=True, host='0.0.0.0', use_reloader=True, port=GLOBALS['flaskPort'])
