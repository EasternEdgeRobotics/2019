from flask import Flask, render_template, redirect, jsonify
import json
import random

app = Flask(__name__)

"""
Base url for opening the GUI. This route will return the index.html
"""
@app.route("/")
def returnGui():
    return render_template("index.html")


"""
/testGetPressure
GET
returns a random value simulating a pressure sensor
"""
@app.route("/testGetPressure")
def testGetPressure():
    value = random.randint(99, 105)
    return json.dumps(value)


"""
Server start.
This is a standard python function that is True when this file is called from the command line (python3 main.py)
(This statement is false for calls to the server)
"""
if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0')
