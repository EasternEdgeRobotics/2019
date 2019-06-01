"""Admin API."""
from flask import Blueprint, render_template, request, make_response, redirect
import random
import string
import json
import datetime
from functools import update_wrapper
import sys

admin_api = Blueprint("admin_api", __name__)

topsidesComms = None

#{"key": {expire, permissions}}
activeKeys = {}
accounts = {}



def adminAPI(comms):
    global topsidesComms, accounts
    topsidesComms = comms

    try:
        with open("json/accounts.json") as file:
            accounts = json.load(file)
    except Exception as ex:
        print("Error loading Accounts JSON:  " + str(ex))

    return admin_api

def protected(permissions=["ADMIN"], redirectB=False):
    def decorator(func):
        global activeKeys
        def wrap(*args, **kwargs):

            if(len(sys.argv) > 1 and (sys.argv[1] == "--dev")):
                return func()

            name = func.__name__
            if("eer_auth_key" in request.cookies):
                key = request.cookies.get("eer_auth_key")
                if(key in activeKeys):
                    if(datetime.datetime.now() <= activeKeys[key]['expire']):
                        for perm in permissions:
                            if(perm not in activeKeys[key]['permissions']):
                                return loadNotAuthorized()
                        return func()
                    del activeKeys[key]
            if(redirectB == True):
                return redirect("/?page=login", code=302)
            return loadAdminLoginPage()
        wrap.__name__ = func.__name__
        return wrap
    return decorator

def loadNotAuthorized():
    return "<p>Not Authorized! Log in to access!</p>", 401
    #return loadAdminLoginPage()

"""
loads the page for logining into admin
"""
def loadAdminLoginPage():
    return render_template("dashboard/login.html")


@admin_api.route("/auth/login", methods=["POST", "GET"])
def attemptLogin():
    global activeKeys, accounts
    password = request.args.get("pass")
    username = request.args.get("user")
    if(username in accounts):
        if(password == accounts[username]["password"]):
            key = "".join(random.choice(string.ascii_lowercase+string.digits) for i in range(0,50))
            activeKeyExpiry = datetime.datetime.now() + datetime.timedelta(hours=5)
            activeKeys[key] = {"expire": activeKeyExpiry, "permissions": accounts[username]["permissions"], "username": username}

            res = make_response("authorized")
            res.set_cookie("eer_auth_key", key)
            return res
    return "Invalid Username or Password!", 401

@admin_api.route("/auth/check", methods=["GET"])
def isAuth():
    global activeKeys
    key = request.cookies.get("eer_auth_key")
    if(key in activeKeys):
        if(datetime.datetime.now() <= activeKeys[key]['expire']):
            return activeKeys[key]["username"]
        else:
            del activeKeys[key]
    return "No Auth", 401

@admin_api.route("/auth/logout", methods=["POST", "GET"])
def logout():
    global activeKeys
    key = request.cookies.get("eer_auth_key")
    if(key in activeKeys):
        del activeKeys[key]

    res = make_response("logged out")
    res.set_cookie("eer_auth_key", "")
    return res


"""
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
"""
"""
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

"""