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
    return render_template("controlTest.html")


"""

"""
@app.route("/joystickValueTest", methods=["POST"])
def getJoytickValuesFromJavascript():
    #CODE HERE FOR RECIEVING CLIENT SIDE CONTROLS TEST
    #to get json data: <<VAR>> = request.json
    print(request.json)
    return(jsonify("lol"))


@app.route("/getProfiles")
def getProfiles():
    return json.dumps(profileHandle.loadProfiles())

@app.route("/deleteProfile")
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
Server start.
This is a standard python function that is True when this file is called from the command line (python3 main.py)
(This statement is false for calls to the server)
"""
if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0')
