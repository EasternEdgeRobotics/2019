"""Control Software Server for MATE 2019."""
from flask import Flask, render_template
from flask_cors import CORS
import json
import random
from profileAPI import profile_api
from controlAPI import controlAPI
from notificationAPI import notificationAPI
from devAPI import devAPI
from guiAPI import gui_api
import dashboardAPI
from adminAPI import adminAPI
from simulatorAPI import simulatorAPI
from TopsidesGlobals import GLOBALS
import gevent.pywsgi
import gevent.monkey
import werkzeug.serving
import topsidesComms

gevent.monkey.patch_all()
app = Flask(__name__)
CORS(app)

# Registering APIs
app.register_blueprint(profile_api)
app.register_blueprint(controlAPI(topsidesComms))
app.register_blueprint(notificationAPI(topsidesComms))
app.register_blueprint(devAPI(topsidesComms))
app.register_blueprint(adminAPI(topsidesComms))
app.register_blueprint(gui_api)
app.register_blueprint(simulatorAPI(topsidesComms))
app.register_blueprint(dashboardAPI.dashboardAPI(topsidesComms))


@app.after_request
def afterRequest(response):
    response.headers.add('Access-Control-Allow-Origin', "*")
    response.headers.add('Access-Control-Allow-Headers', "Content-Type,Authorization")
    response.headers.add('Access-Control-Allow-Methods', "GET,POST,PUT,DELETE,OPTIONS")
    return response


@app.route("/")
def returnGui():
    """
    Base url and table of contents.

    :return: rendered index.html web page
    """
    return dashboardAPI.dashboard()


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


@werkzeug.serving.run_with_reloader
def run_server():
    """Run the gevent production server with reloading enabled."""
    ws = gevent.pywsgi.WSGIServer(listener=('0.0.0.0', GLOBALS['flaskPort']), application=app)
    ws.serve_forever()


"""
Server start.

This is a standard python function that is True when this
file is called from the command line (python3 main.py)
(This statement is false for calls to the server)
"""
if __name__ == "__main__":
    run_server()
