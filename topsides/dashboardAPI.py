"""Dashboard API."""
from flask import Blueprint, render_template, jsonify, request
import json
import profileAPI
import adminAPI
import copy

dashboard_api = Blueprint("dashboard_api", __name__)

topsidesComms = None

dashboardJson = []


def dashboardAPI(comms):
    global topsidesComms, dashboardJson
    topsidesComms = comms
    try:
        with open("json/dashboard.json") as file:
            dashboardJson = json.load(file)
    except Exception as e:
        print("Error Loading Dashboard JSON")

    return dashboard_api


@dashboard_api.route("/dashboard")
def dashboard():
    return render_template("dashboard/dashboard.html")

"""
loads a dashboard page
"""
@dashboard_api.route("/dashboard/page/<pagename>")
def loadPage(pagename):
    if(pagename == "login"):
        return loadLoginPage()

    for menu in dashboardJson["menus"]:
        if(menu["name"] == pagename):
            return render_template(menu["file_name"])

    return render_template(dashboardJson["menus"][0]["file_url"])


"""
gets the json for the dahsboard
"""
@dashboard_api.route("/dashboard/getmenujson")
def getMenuJSON():
    sendData = copy.deepcopy(dashboardJson)
    for button in sendData["menus"]:
        del button["file_name"]
    return jsonify(sendData)


"""
Specialized page for profile editor
Needs jinja to load profile
"""
@dashboard_api.route("/dashboard/editProfile")
def editProfileMenu():
    return profileAPI.editProfilePage()


"""
loads pages outside the dashboard
"""
@dashboard_api.route("/dashboard/ext")
@adminAPI.protected(permissions=["CONTROL"], redirectB=True)
def loadExternalPage():
    return render_template("dashboard/dashboard-external.html") + render_template(request.args.get("name"))

"""
special case for login
"""
@dashboard_api.route("/dashboard/login")
def loadLoginPage():
    return render_template("dashboard/login.html")
