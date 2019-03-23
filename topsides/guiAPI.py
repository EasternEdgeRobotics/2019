"""GUI."""
from flask import Blueprint, render_template, jsonify, request

gui_api = Blueprint("gui_api", __name__)

topsidesComms = None


def guiAPI(comms):
    global topsidesComms
    topsidesComms = comms
    return gui_api


@gui_api.after_request
def afterRequest(response):
    response.headers.add('Access-Control-Allow-Origin', "*")
    response.headers.add('Access-Control-Allow-Headers', "Content-Type,Authorization")
    response.headers.add('Access-Control-Allow-Methods', "GET,POST,PUT,DELETE,OPTIONS")
    return response


@gui_api.route("/gui")
def returnGuiPage():
    """
    Return page for the control gui.

    :return: rendered gui.html web page
    """
    return render_template("gui.html")


@gui_api.route('/guislider', methods=['POST'])
def getSliderValues():
    """
    Gets the values from the 6 degrees of power gui sliders.

    Input: {slider: string, value: int}

    POST method
    """
    # ['value'] = value of slider (0-10 currently)
    # ['slider'] = which slider (Yaw, Pitch, etc.)
    data = request.json
    print(data['slider'])
    print(data['value'])
    return jsonify("")


@gui_api.route('/ledtoggle', methods=['POST'])
def getLedValues():
    """
    Turns the led lights on or off.

    Input: {value: int}

    POST method
    """
    data = request.json
    neededValue = data['value']
    # TODO: Change to a file on the raspberry pi to toggle the lights
    topsidesComms.putMessage("led.py " + " " + str(neededValue))
    return "good"