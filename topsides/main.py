from flask import Flask, render_template, redirect, jsonify, request
import json
import random
import profileHandle

app = Flask(__name__)

"""
Base url for opening the GUI. This route will return the index.html
"""
@app.route("/")
def returnGui():
    return render_template("index.html")


"""
Return page for control profile edit
"""
@app.route("/editprofile")
def editProfilePage():
    profiles = profileHandle.loadProfiles()
    return render_template("controlProfileEdit.html", profiles=profiles)


"""
Return page for control input testing
"""
@app.route("/testJoystick")
def testJoystickPage():
    return render_template("controlTest.html")  # return html page for testing joystick


"""
joystickValueTest
POST

simple reciever function for testing client to server comms for joystick input. Json containing joystick values is attached

INPUT:
    Json Body Format: {x: double, y: double, z: double, thumbstick}

"""

def setThrusterValues(tDirect, tPos):
    F = 1.0
    B = -1.0
    C = 0.0

    setThruster = [C,C,C,C,C,C];

    if(tDirect == "surge" and tPos == 1):
        setThruster = [F, B, B, F, C, C]
    elif(tDirect == "surge" and tPos == -1):
        setThruster = [B, F, F, B, C, C]
    elif(tDirect == "sway" and tPos == 1):
        setThruster = [F, F, B, B, C, C]
    elif(tDirect == "sway" and tPos == -1):
        setThruster = [B, B, F, F, C, C]
    elif(tDirect == "heave" and tPos == 1):
        setThruster = [C, C, C, C, F, F]
    elif(tDirect == "heave" and tPos == -1):
        setThruster = [C, C, C, C, B, B]
    elif(tDirect == "pitch" and tPos == 1):
        setThruster = [C, C, C, C, F, B]
    elif(tDirect == "pitch" and tPos == -1):
        setThruster = [C, C, C, C, B, F]
    elif(tDirect == "yaw" and tPos == 1):
        setThruster = [F, B, F, B, C, C]
    elif(tDirect == "yaw" and tPos == -1):
        setThruster = [B, F, B, F, C, C]
    else:
        setThruster = [C, C, C, C, C, C]

    return setThruster

@app.route("/joystickValueTest", methods=["POST"])
def getJoytickValuesFromJavascript():
    # CODE HERE FOR RECEIVING CLIENT SIDE CONTROLS TEST @KEIFF
    # to get json data: <<VAR>> = request.json

    # ['direction'] = 1 or -1
    # ['slider'] = which slider (Yaw, Pitch, etc.)
    data = request.json
    print(data['slider'])
    print(data['direction'])

    ## store the thruster values in a list
    setThruster = setThrusterValues(data['slider'], int(data['direction']));
    ## call the fControl rov file and pass it [port, value]
    for x in range(len(setThruster)):
        ## This will most likely produce a file path error
        topsidesComms.send.put("fControl.py " + str(x) + str(setThruster[x]));

    return jsonify("lol")  # returns lol in json as filler (server crashes if nothing is returned)


"""
getProfiles
GET

returns the control profiles from memory as json
"""
@app.route("/getProfiles", methods=["GET"])
def getProfiles():
    return json.dumps(profileHandle.loadProfiles())  # responds json containing all profiles


"""
deleteProfile
POST

deletes the requested profile from memory.

INPUT:
    Json Body Format: {id: int}
"""
@app.route("/deleteProfile", methods=["POST"])
def deleteProfile():
    profileID = request.args.get('profileID')
    if(profileID is None):
        return "Failed, profileID not read correct or is not a number"
    else:
        profileHandle.deleteProfile(int(profileID))
        return "success"


"""
/testGetPressure
GET

returns a random value simulating a pressure sensor
"""
@app.route("/testGetPressure")
def testGetPressure():
    value = random.randint(99, 105)
    return json.dumps(value)


"""
Return page for the control gui
"""
@app.route("/gui")
def returnGuiPage():
    return render_template("gui.html")


"""
/guislider
POST

gets the values from the 6 degrees of power gui sliders
"""
@app.route('/guislider', methods = ['POST'])
def getSliderValues():
    # ['value'] = value of slider (0-10 currently)
    # ['slider'] = which slider (Yaw, Pitch, etc.)
    data = request.json
    print(data['slider'])
    print(data['value'])
    return jsonify("")


"""
Return page for the development input
"""
@app.route("/dev")
def returnDevPage():
    return render_template("dev.html")


"""
/devinput
POST

gets the values from the dev input
"""
@app.route('/devinput', methods = ['POST'])
def getDevInput():
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
    app.run(debug=True, host='0.0.0.0')
