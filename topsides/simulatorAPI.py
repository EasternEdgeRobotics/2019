from flask import Blueprint, Flask, render_template, jsonify, request, Response
import time
import json


simulator_api = Blueprint("simulator_api", __name__)
topsidesComms = None

isEnabled = False

BotStatus = {"pressure": 0, "thrusters": [0,0,0,0,0,0], "orientation": {"x": 0, "y": 0, "z": 0}}


@simulator_api.route("/simulator")
def simulatorPage():
    return render_template("simulator.html")


@simulator_api.route("/getSimulatorValues")
def getBotValues():

    def generator():
        yield "data:" + BotStatus + "\n\n"

        
    return Response(generator(), mimetype='text/event-stream')


@simulator_api.route("/simulator/updateValuesFromClient", methods=["POST"])
def updateValues():
    global BotStatus
    data = request.json
    BotStatus.pressure = data.get("pressure", BotStatus.pressure)
    BotStatus.thrusters = data.get("thrusters", BotStatus.thrusters)
    


"""
    ____                   _    _____           _       __      
   / __ \____ __________  (_)  / ___/__________(_)___  / /______
  / /_/ / __ `/ ___/ __ \/ /   \__ \/ ___/ ___/ / __ \/ __/ ___/
 / _, _/ /_/ (__  ) /_/ / /   ___/ / /__/ /  / / /_/ / /_(__  ) 
/_/ |_|\__,_/____/ .___/_/   /____/\___/_/  /_/ .___/\__/____/  
                /_/                          /_/                
"""


def fControl(tChan, tSpeed):
    global BotStatus
    #PORTS = [2, 1, 15, 17, 0, 16]
    BotStatus.thrusters[tChan] = tSpeed