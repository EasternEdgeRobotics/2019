from flask import Blueprint, render_template, request
from flask_socketio import SocketIO, emit
from adminAPI import protected
import json
import random

topsidePID = None

bot_api = Blueprint("bot_api", __name__)
bot_api.threaded = True

socketio = None

rotationLock = False
targetRotation = {
    "x": None,
    "y": None,
    "z": None
}

depthLock = True
targetDepth = None

topsidesComms = None

data = {
    "raspi1": {
        "ping": None,
        "temp": None
    },
    "raspi2": {
        "ping": None,
        "temp": None
    },
    "accelerometer": {
        "x": None,
        "y": None,
        "z": None
    },
    "gyroscope": {
        "x": None,
        "y": None,
        "z": None
    },
    "pressure": None,
    "temperature": None,
    "ph": None
}

def botAPI(topPID, topsideC):
    global topsidePID, topsidesComms
    topsidePID = topPID
    topsidesComms = topsideC

    return bot_api


def socketSetup(socket):
    global socketio
    socketio = socket
    
    
    # Server side
    @socketio.on('connect')
    def on_connect():
        print("connect")

"""
set the bot data and emit to clients
"""
def updateTelemetryData(d):
    global data
    data = d
    emitTelemetryData()


"""
safe method for getting nested object feilds
"""
def deepGet(obj, array):
    if(obj == None):
        return None
    if(len(array) > 0):
        feild = array.pop(0)
        return deepGet(obj.get(feild, None), array)

    return obj


"""
broadcasts the telemetry data to all clients
"""
def emitTelemetryData():
    socketio.emit('data', data, namespace='/bot/telemetry', broadcast=True )


@bot_api.route("/bot/target/rotation", methods=["POST"])
def lockRotation():
    global targetRotation
    """
    targetRotation = {
        "x": data["gyroscope"]["x"]
        "y": data["gyroscope"]["y"]
        "z": data["gyroscope"]["z"]
    }
    """
    topsidePID.pitch.target = data["gyroscope"]["x"] # x on gyro
    topsidePID.r.target = data["gyroscope"]["y"]
    topsidePID.yaw.target = data["gyroscope"]["z"]
    return "good"

@bot_api.route("/bot/target/depth", methods=["POST"])
def lockDepth():
    global targetDepth
    topsidePID.depth.target = data[""]
    targetDepth = data.get("depth", None)
    return "good"

@bot_api.route("/bot/trigger/rotation", methods=["POST"])
def triggerRotation():
    data = request.json
    global rotationLock

    rotationLock = bool(data.get("enabled", False))
    return "good"

@bot_api.route("/bot/trigger/gyro", methods=["POST"])
def triggerGyro():
    topsidesComms.sendData("sensors 0", "raspi-4")
    return "good"

@bot_api.route("/bot/giveme", methods=["GET"])
def giveme():
    return json.dumps(data)
    

@bot_api.route("/bot/trigger/sensors", methods=["POST"])
def triggerSensors():
    topsidesComms.sendData("sensors 1", "raspi-4")
    return "good"

@bot_api.route("/bot/test")
def test():
    updateTelemetryData({"raspi1": {"ping": random.randint(20,40), "temp": random.randint(15, 20)}, "pressure": random.randint(80, 120), "accelerometer": {"x": random.randint(0, 360),"y": random.randint(0, 360),"z": random.randint(0, 360)},"gyroscope": {"x": random.randint(0, 360),"y": random.randint(0, 360),"z": random.randint(0, 360)}})
    return ""
