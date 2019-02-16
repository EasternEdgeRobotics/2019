"""Loads and deletes control profiles."""
from flask import Blueprint, render_template, request
import json

profile_api = Blueprint('profile_api', __name__)


@profile_api.after_request
def afterRequest(response):
    response.headers.add('Access-Control-Allow-Origin', "*")
    response.headers.add('Access-Control-Allow-Headers', "Content-Type,Authorization")
    response.headers.add('Access-Control-Allow-Methods', "GET,POST,PUT,DELETE,OPTIONS")
    return response


@profile_api.route("/editprofile")
def editProfilePage():
    """
    Return page for control profile edit.

    :return: rendered controlProfileEdit.html web page
    """
    profiles = loadProfiles()
    return render_template("controlProfileEdit.html", profiles=profiles)


@profile_api.route("/getProfiles", methods=["GET"])
def getProfiles():
    """
    Returns the control profiles from memory as json.

    GET method

    :return: Json containing all profiles
    """
    return json.dumps(loadProfiles())  # Responds json containing all profiles


@profile_api.route("/deleteProfile", methods=["POST"])
def deleteProfile():
    """
    Deletes the requested profile from memory.

    POST

    Input: Json Body Format: {id: int}

    :return: string "Failed, profileID not read correct or is not a number" or "success"
    """
    profileID = request.args.get('profileID')
    profileID = request.json["profileId"]
    if(profileID is None):
        return "Failed, profileID not read correct or is not a number"
    else:
        deleteProfile(int(profileID))
        return "success"


@profile_api.route("/saveProfile", methods=["POST"])
def saveProfileRequest():
    """
    saveProfile.

    POST
    """
    print(request.json)
    saveProfile(request.json)
    return json.dumps("Profile Saved!")


# ----- METHODS ----- #
def loadProfiles():
    """
    Loads the profiles json file and returns it as a json object.

    If the file can't be loaded, the function returns a string containing the error.

    :return: profile json object or string containing error
    """
    try:
        with open("json/controlProfiles.json") as file:
            data = json.load(file)
            return data
    except Exception as e:
        return ("Problem loading json: " + str(e))


def deleteProfile(id):
    """
    Deletes a control profile from memory.

    :params id: id of profile to delete from memory
    """
    print(id)
    with open("json/controlProfiles.json", "r+") as file:
        data = json.load(file)
        for i in range(0, len(data)):
            element = data[i]
            if(int(element["id"]) == int(id)):
                del data[i]
                break

        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()


def saveProfile(profile):
    """
    Saves or adds a new profile to the JSON.

    :param profile: profile JSON to save to the file
    """
    print(profile["id"])
    added = False
    with open("json/controlProfiles.json", "r+") as file:
        data = json.load(file)
        for i in range(0, len(data)):
            if(str(data[i]["id"]) == str(profile["id"])):
                data[i] = profile
                added = True

        if not added:
            data.append(profile)

        print(data)

        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()


def getProfileByID(id):
    profiles = loadProfiles()
    for profile in profiles:
        if(str(profile['id']) == str(id)):
            return profile
    return None
