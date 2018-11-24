import json

GLOBALS = {}

try:
    with open("json/Topsides.json") as file:
        data = json.load(file)
        GLOBALS = data
except Exception as ex:
    print("Error loading Global JSON" + str(ex))
