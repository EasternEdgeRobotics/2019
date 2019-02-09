"""Simulator API."""
from flask import Blueprint, render_template, jsonify

topsidesComms = None

simulator_api = Blueprint("simulator_api", __name__)
topsidesComms = None

isEnabled = False


def simulatorAPI(comms):
    global topsidesComms
    topsidesComms = comms
    return simulator_api


@simulator_api.route("/simulator")
def simulatorPage():
    return render_template("simulator.html")


"""
@simulator_api.route("/simulator/getCommand")
def getBotCommand():

    def generator():
        global topsidesComms
        if(not topsidesComms.simulator.empty()):
            msg = topsidesComms.simulator.get(timeout=1)
            topsidesComms.simulator.task_done()
            print("ran")
            print(msg)
            yield "data:" + msg + "\n\n"
            print("here")


    return Response(generator(), mimetype='text/event-stream')
"""


@simulator_api.route("/simulator/getCommand", methods=['GET'])
def getBotCommand():
    returnMsg = []
    while(not topsidesComms.simulator.empty()):
        returnMsg.append(topsidesComms.simulator.get())

    return jsonify(returnMsg)
