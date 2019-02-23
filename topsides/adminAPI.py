"""Admin API."""
from flask import Blueprint, render_template, request
import random
import string
import datetime
from TopsidesGlobals import GLOBALS, RASPI_GLOBALS
import TopsidesGlobals

admin_api = Blueprint("admin_api", __name__)

topsidesComms = None

activeKey = None
activeKeyExpiry = None


def adminAPI(comms):
    global topsidesComms
    topsidesComms = comms
    return admin_api


@admin_api.route("/adminlogin")
def loadAdminLoginPage():
    return render_template("adminLogin.html")


@admin_api.route("/authAdminLogin", methods=["POST", "GET"])
def attemptLogin():
    global activeKey, activeKeyExpiry
    password = request.args.get("pass")
    if(password == GLOBALS["admin_password"]):
        key = "".join(random.choice(string.ascii_lowercase+string.digits) for i in range(0,50))
        activeKey = key
        activeKeyExpiry = datetime.datetime.now() + datetime.timedelta(minutes=10)
        return key
    else:
        return "Invalid Password!", 401


@admin_api.route("/adminpage", methods=["GET"])
def getAdminPage():
    global activeKey, activeKeyExpiry
    key = request.args.get("key")
    dnow = datetime.datetime.now()
    
    try:
        if(key == activeKey and dnow <= activeKeyExpiry):
            copyT = dict(GLOBALS)
            copyT.pop("admin_password")
            copyT.pop("thrusterPorts")
            copyR = dict(RASPI_GLOBALS)
            return render_template("admin.html", topsides_globals=copyT, raspi_globals=copyR, isinstance=isinstance, int=int)
    except Exception as e:
        print(e)    
    return "Unauthorized", 401


@admin_api.route("/updateTopsidesGlobal", methods=["POST"])
def updateTopsides():
    data = request.json
    try:
        TopsidesGlobals.updateTopsidesGlobals(data)
        return "Saved Topsides.json!"
    except(Exception):
        return "Error Saving Topsides.json!", 500


@admin_api.route("/updateRaspiGlobal", methods=["POST"])
def updateRaspi():
    data = request.json
    try:
        TopsidesGlobals.updateRaspiGlobals(data)
        return "Saved Raspi.json!"
    except(Exception):
        return "Error Saving Raspi.json!", 500

