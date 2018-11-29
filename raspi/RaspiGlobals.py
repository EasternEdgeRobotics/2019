import json

GLOBALS = {}

try:
    with open("json/Raspi.json") as file:
        data = json.load(file)
        GLOBALS = data
except Exception as ex:
    print("Error loading Global JSON" + str(ex))
