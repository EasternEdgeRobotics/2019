import json
from flask import Blueprint, Flask, render_template, jsonify, request
from TopsidesGlobals import GLOBALS
import random
import string
import datetime

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
            return render_template("admin.html")
    except(Exception):
        None    
    return "Unauthorized", 401
