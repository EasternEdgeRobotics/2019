from flask import Blueprint, render_template, request
from flask_socketio import SocketIO, emit
import random

bot_api = Blueprint("bot_api", __name__)
bot_api.threaded = True

socketio = None

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
    "pressure": None
}

def socketSetup(socket):
    global socketio
    socketio = socket

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


@bot_api.route("/bot/test")
def test():
    updateTelemetryData({"raspi1": {"ping": random.randint(20,40), "temp": random.randint(15, 20)}, "pressure": random.randint(80, 120)})
    return ""