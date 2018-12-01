"""Control Software Server for MATE 2019."""
from flask import Flask, render_template
import json
import random
from profileAPI import profile_api
from controlAPI import controlAPI
from notificationAPI import notificationAPI
from joystickAPI import joystickAPI
from devAPI import devAPI
from guiAPI import gui_api
import topsidesComms
import threading
from TopsidesGlobals import GLOBALS

app = Flask(__name__)

# Registering APIs
app.register_blueprint(profile_api)
#app.register_blueprint(controlAPI(topsidesComms))
app.register_blueprint(notificationAPI(topsidesComms))
app.register_blueprint(joystickAPI(topsidesComms))
app.register_blueprint(devAPI(topsidesComms))
app.register_blueprint(gui_api)

# Setup threading for communications
t = threading.Thread(target=topsidesComms.startComms)


@app.route("/")
def returnGui():
    """
    Base url and table of contents.

    :return: rendered index.html web page
    """
    return render_template("index.html")


@app.route("/controlTest")
def controlTestPage():
    """
    Base url and table of contents.

    :return: rendered controlTest.html web page
    """
    return render_template("controlTest.html")


@app.route("/testGetPressure")
def testGetPressure():
    """
    A test pressure sensor.

    GET

    :return: a random value simulating a pressure sensor
    """
    value = random.randint(99, 105)
    return json.dumps(value)


"""
Server start.
This is a standard python function that is True when this file is called from the command line (python3 main.py)
(This statement is false for calls to the server)
"""
if __name__ == "__main__":
    t.start()
    if topsidesComms.received.get() == "bound":
        app.run(debug=True, host='0.0.0.0', use_reloader=True, port=GLOBALS['flaskPort'], threaded=True)
