"""Topsides Globals."""
import json

GLOBALS = {}
RASPI_GLOBALS = {}

try:
    with open("json/Topsides.json") as file:
        data = json.load(file)
        GLOBALS = data
except Exception as ex:
    print("Error loading Global JSON" + str(ex))

def updateTopsidesGlobals(newData):
    with open("json/Topsides.json", "r+") as file:
        data = json.load(file)
        for i in newData:
            try:
                data[i] = int(newData[i])
            except:
                data[i] = newData[i]

        GLOBALS = data

        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()


def updateRaspiGlobals(newData):
    with open("../raspi/json/Raspi.json", "r+") as file:
        data = json.load(file)
        for i in newData:
            if(int(newData[i])):
                data[i] = int(newData[i])
            else:
                data[i] = newData[i]

        RASPI_GLOBALS = data

        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
