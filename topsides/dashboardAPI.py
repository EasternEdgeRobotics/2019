"""Dashboard API."""
from flask import Blueprint, render_template, jsonify, request
import json
import profileAPI

dashboard_api = Blueprint("dashboard_api", __name__)

topsidesComms = None


def dashboardAPI(comms):
    global topsidesComms
    topsidesComms = comms
    return dashboard_api


@dashboard_api.route("/dashboard")
def dashboard():
    return render_template("dashboard/dashboard.html")


@dashboard_api.route("/dashboard/page")
def loadPage():
    return render_template(request.args.get("name"))


@dashboard_api.route("/dashboard/getmenujson")
def getMenuJSON():
    try:
        with open("json/dashboard.json") as file:
            return jsonify(json.load(file))
    except Exception as e:
        return "Error loading JSON", 500


@dashboard_api.route("/dashboard/editProfile")
def editProfileMenu():
    profile = profileAPI.getProfileByID(request.args.get("id"))
    return render_template("dashboard/dashboard-profiles-edit.html", profile=profile)

@dashboard_api.route("/dashboard/ext")
def loadExternalPgae():
    return render_template("dashboard/dashboard-external.html") + render_template(request.args.get("name"))