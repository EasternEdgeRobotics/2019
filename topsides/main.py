"""Control Software Server for MATE 2019."""
from flask import Flask, render_template
from flask_cors import CORS
import json
import random
from profileAPI import profile_api
from controlAPI import controlAPI
import notificationAPI
import botAPI
from devAPI import devAPI
from guiAPI import gui_api
import dashboardAPI
import themeAPI
from adminAPI import adminAPI
from simulatorAPI import simulatorAPI
from TopsidesGlobals import GLOBALS
import gevent.pywsgi
import gevent.monkey
import werkzeug.serving
import topsidesComms
from flask_socketio import SocketIO

#gevent.monkey.patch_all()
app = Flask(__name__)
socketio = SocketIO(app)
CORS(app)

# Registering APIs
app.register_blueprint(profile_api)
app.register_blueprint(controlAPI(topsidesComms))
app.register_blueprint(notificationAPI.notificationAPI())
app.register_blueprint(devAPI(topsidesComms))
app.register_blueprint(adminAPI(topsidesComms))
app.register_blueprint(gui_api)
app.register_blueprint(simulatorAPI(topsidesComms))
app.register_blueprint(dashboardAPI.dashboardAPI(topsidesComms))
app.register_blueprint(themeAPI.themeAPI())
app.register_blueprint(botAPI.bot_api)


#Register socket events
notificationAPI.socketSetup(socketio)
botAPI.socketSetup(socketio)


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



#@werkzeug.serving.run_with_reloader
def run_server():
    """Run the gevent production server with reloading enabled."""
    #ws = gevent.pywsgi.WSGIServer(listener=('0.0.0.0', GLOBALS['flaskPort']), application=app)
    #ws.serve_forever()

    #This is new, running server with socketio. This is required if we want the new notification system
    socketio.run(app, debug=True, use_reloader=False, host='0.0.0.0', port=GLOBALS['flaskPort'])


"""
Server start.

This is a standard python function that is True when this
file is called from the command line (python3 main.py)
(This statement is false for calls to the server)
"""
if __name__ == "__main__":
    themeAPI.loadThemes()
    run_server()
