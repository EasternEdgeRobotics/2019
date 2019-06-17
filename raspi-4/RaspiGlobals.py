"""Raspberry Pi Globals."""
import json

GLOBALS = {}

try:
    with open("json/Raspi.json") as file:
        data = json.load(file)
        GLOBALS = data
except Exception as ex:
    print("Error loading Global JSON" + str(ex))

def editJSON(key, value):
    with open('json/Raspi.json', 'r+') as file:
        data = json.load(file)
        data[key] = value
        file.seek(0)        # <--- should reset file position to the beginning.
        json.dump(data, file, indent=4)
        file.truncate()     # remove remaining part
