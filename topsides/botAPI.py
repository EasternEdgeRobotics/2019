"""Bot API."""
from flask import Blueprint, render_template, request
from flask_socketio import SocketIO, emit
from adminAPI import protected
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
    "pressure": None,
    "temperaturesensor": None,
    "gyroscopex": None,
    "gyroscopey": None,
    "gyroscopez": None,
    "accelerometerx": None,
    "accelerometery": None,
    "accelerometerz": None,
    "temperatureimu": None,
    "temperatureext": None,
    "metaldetector": None,
    "ph": None
}


def socketSetup(socket):
    global socketio
    socketio = socket


def updateTelemetryData(d):
    """Set the bot data and emit to clients."""
    global data
    data = d
    emitTelemetryData()


def deepGet(obj, array):
    """Safe method for getting nested object fields."""
    if(obj is None):
        return None
    if(len(array) > 0):
        field = array.pop(0)
        return deepGet(obj.get(field, None), array)

    return obj


def emitTelemetryData():
    """Broadcasts the telemetry data to all clients."""
    socketio.emit('data', data, namespace='/bot/telemetry', broadcast=True)


@bot_api.route("/bot/test")
@protected
def test():
    """Test sensor reading."""
    updateTelemetryData({"raspi1": {"ping": random.randint(20, 40), "temp": random.randint(15, 20)}})
    print(data)
    return ""


@bot_api.route("/bot/sensorui")
def sensorui():
    """Test UI for sensor data."""
    return render_template("sensorui.html")


@bot_api.route("/bot/sensordata")
def sensordata():
    """
    Test code for random data.

    Use the sensors.py file for proper testing with everything
    here commented out except for the return template
    """
    data["pressure"] = random.randint(1, 100)
    data["temperaturesensor"] = random.randint(1, 100)
    data["gyroscopex"] = random.randint(1, 100)
    data["gyroscopey"] = random.randint(1, 100)
    data["gyroscopez"] = random.randint(1, 100)
    data["accelerometerx"] = random.randint(1, 100)
    data["accelerometery"] = random.randint(1, 100)
    data["accelerometerz"] = random.randint(1, 100)
    data["temperatureimu"] = random.randint(1, 100)
    data["temperatureext"] = random.randint(1, 100)
    data["metaldetector"] = random.randint(1, 100)
    data["ph"] = random.randint(1, 100)
    emitTelemetryData()
    return render_template("sensordata.html", result=data)
