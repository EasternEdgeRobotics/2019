"""GUI."""
from flask import Blueprint, render_template, jsonify, request
from adminAPI import protected

gui_api = Blueprint("gui_api", __name__)


@gui_api.route("/gui")
@protected
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
