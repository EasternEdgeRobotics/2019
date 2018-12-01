from flask import Blueprint, Flask, render_template, jsonify, request, Response
import time
import json


notification_api = Blueprint("notification_api", __name__)
notification_api.threaded = True

topsidesComms = None

def notificationAPI(comms):
    global topsidesComms
    topsidesComms = comms
    return notification_api

@notification_api.route("/testNotificationsPage")
def loadNotificationTestPage():
    return render_template("notificationsTest.html")

@notification_api.route("/notificationTest")
def notificationTest():

    def generator():
        yield "data:" + str(json.dumps({'message':topsidesComms.received.get(), 'type': 'info'})) + "\n\n"

        
    return Response(generator(), mimetype='text/event-stream')
        

@notification_api.route("/postNotification", methods=["POST"])
def postTestNotification():
    global lol
    global testNotifications
    testNotifications.append("This is test Notification #" + str(lol))

    lol+=1
    return ""