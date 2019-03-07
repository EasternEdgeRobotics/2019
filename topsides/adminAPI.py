"""Admin API."""
from flask import Blueprint, render_template, request, make_response
import random
import string
import datetime
from TopsidesGlobals import GLOBALS, RASPI_GLOBALS
import TopsidesGlobals

admin_api = Blueprint("admin_api", __name__)

topsidesComms = None

activeKey = None
activeKeyExpiry = None


def protected(func):
    global activeKey, activeKeyExpiry

    def wrap(*args, **kwargs):
        if("eer_auth_key" in request.cookies):
            if(request.cookies.get("eer_auth_key") == activeKey):
                if(datetime.datetime.now() <= activeKeyExpiry):
                    return func()
        return loadNotAuthorized()
    wrap.__name__ = func.__name__
    return wrap

def loadNotAuthorized():
    return "<p>Not Authorized! Log in to access!</p>", 401
        


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
        res = make_response("authorized")
        res.set_cookie("eer_auth_key", key)
        activeKeyExpiry = datetime.datetime.now() + datetime.timedelta(minutes=10)
        return res
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

