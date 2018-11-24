"""Loads and deletes control profiles."""
import json


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
        print(data)
        for i in range(0, len(data)):
            element = data[i]
            if(int(element["id"]) == int(id)):
                del data[i]

        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

"""
saveProfile

saves or adds a new profile to the JSON

@params:
    - profile: profile JSON to save to the file
"""
def saveProfile(profile):
    print(profile["id"])
    added = False
    with open("json/controlProfiles.json", "r+") as file:
        data = json.load(file)
        for i in range(0,len(data)):
            if(str(data[i]["id"]) == str(profile["id"])):
                data[i] = profile
                added = True

        if not added:
            data.append(profile)

        print(data)


        file.seek(0)        
        json.dump(data, file, indent=4)
        file.truncate()
        

    
