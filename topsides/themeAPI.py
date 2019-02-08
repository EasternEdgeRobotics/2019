from flask import Blueprint, Flask, render_template, jsonify, make_response, request, Response
import time
import json
import os
from TopsidesGlobals import GLOBALS

theme_api = Blueprint("theme_api", __name__)

def themeAPI():
    return theme_api


def loadThemes():
    print("loading themes...")
    for filename in os.listdir("./static/css/themes"):
       
        if ".css" not in filename or filename == "template.css":
            continue

        themename = filename.replace(".css", "")

        with open("./static/css/themes/" + filename, "r") as oldfile:
            css = oldfile.read().replace("\n", "").replace("@theme", themename)
            with open("./static/css/themes/loaded/" + filename, "w") as newfile:
                newfile.write(css)
                newfile.close()
                print("loaded theme: " + themename)
            oldfile.close()

@theme_api.route("/themes", methods=["GET"])
def getThemes():
    returnHTML = ""
    for filename in os.listdir("./static/css/themes/loaded"):
        returnHTML += "<link rel='stylesheet' type='text/css' href='/static/css/themes/loaded/" + filename + "'>"
    return returnHTML

@theme_api.route("/themes/getnames", methods=["GET"])
def getThemeNames():
    themes = []
    for theme in os.listdir("./static/css/themes/loaded"):
        themes.append(theme.replace(".css", ""))
    return jsonify(themes)

@theme_api.route("/themes/set", methods=["POST"])
def setCurrentTheme():
    res = make_response("set theme")
    res.set_cookie("theme", request.json["theme"])
    return res

@theme_api.route("/themes/get", methods=["GET"])
def getCurrentTheme():
    res = None
    if("theme" in request.cookies):
        res = make_response(jsonify({"theme": request.cookies.get('theme')}))
    else:
        res = make_response(jsonify({"theme": GLOBALS["defaultTheme"]}))
        res.set_cookie("theme", GLOBALS["defaultTheme"])
    return res

@theme_api.route("/themes/preview")
def previewTheme():
    theme = request.args.get("theme", GLOBALS["defaultTheme"])
    return render_template("themePreview.html", theme = theme)