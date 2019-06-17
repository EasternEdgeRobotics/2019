from flask import Blueprint, Flask, render_template, jsonify, make_response, request, Response
import time
import json
import os
from TopsidesGlobals import GLOBALS

theme_api = Blueprint("theme_api", __name__)

def themeAPI():
    return theme_api

""" loadThemes
    
    @description - finalizes and minimizes css for themes in themes directory and copies to /themes/loaded 

"""
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

""" getThemes()
    GET

    @description - returns the html tags to link themes to page. Returns a bunch of <link> tags

"""
@theme_api.route("/themes", methods=["GET"])
def getThemes():
    returnHTML = ""
    for filename in os.listdir("./static/css/themes/loaded"):
        returnHTML += "<link rel='stylesheet' type='text/css' href='/static/css/themes/loaded/" + filename + "'>"
    return returnHTML


""" getThemeNames
    GET

    @description - returns a list of all loaded themes

"""
@theme_api.route("/themes/getnames", methods=["GET"])
def getThemeNames():
    themes = []
    for theme in os.listdir("./static/css/themes/loaded"):
        themes.append(theme.replace(".css", ""))
    return jsonify(themes)

""" setCurrentTheme
    POST

    @description - Uses cookies to set theme for the client.

    @data - JSON object with theme field for theme name

"""
@theme_api.route("/themes/set", methods=["POST"])
def setCurrentTheme():
    res = make_response("set theme")
    res.set_cookie("theme", request.json["theme"])
    return res


""" getCurrentTheme
    GET

    @description - returns the value of the clients theme cookie
"""
@theme_api.route("/themes/get", methods=["GET"])
def getCurrentTheme():
    res = None
    if("theme" in request.cookies):
        res = make_response(jsonify({"theme": request.cookies.get('theme')}))
    else:
        res = make_response(jsonify({"theme": GLOBALS["defaultTheme"]}))
        res.set_cookie("theme", GLOBALS["defaultTheme"])
    return res

@theme_api.route("/themes/reload", methods=["GET"])
def reloadThemes():
    loadThemes()
    return "themes loaded", 200


@theme_api.route("/themes/preview")
def previewTheme():
    theme = request.args.get("theme", GLOBALS["defaultTheme"])
    return render_template("themePreview.html", theme = theme)