"""Development testing."""
from flask import Blueprint, render_template, jsonify, request

dev_api = Blueprint("dev_api", __name__)


@dev_api.route("/dev")
def returnDevPage():
    """
    Return page for the development input.

    :return: rendered dev.html web page
    """
    return render_template("dev.html")


@dev_api.route('/devinput', methods=['POST'])
def getDevInput():
    """
    Gets the values from the dev input.

    Input: string

    POST method
    """
    # devData is the variable the stores the data submitted from the webpage.
    # it is printed out to console for testing purposes.
    devData = request.json
    print(devData)
    return jsonify("")
