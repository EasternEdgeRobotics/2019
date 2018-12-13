import json
from flask import Blueprint, Flask, render_template, jsonify, request
from TopsidesGlobals import GLOBALS

admin_api = Blueprint("admin_api", __name__)

topsidesComms = None

def adminAPI(comms):
    global topsidesComms
    topsidesComms = comms
    return admin_api



@admin_api.route("/adminlogin")
def loadAdminLoginPage():
    return render_template("adminLogin.html")

@admin_api.route("/authAdminLogin", methods=["POST", "GET"])
def attemptLogin():
    password = request.args.get("pass")
    if(password == GLOBALS["admin_password"]):
        return "y"
    else:
        return "n"
