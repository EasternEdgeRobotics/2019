from flask import Blueprint, Flask, render_template, jsonify, request, Response
import time
import json


notification_api = Blueprint("notification_api", __name__)
notification_api.threaded = True

topsidesComms = None

lol = 0
testNotifications = []

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
        global testNotifications
        while len(testNotifications) <= 0:
            time.sleep(0.5)

        temp = testNotifications[0]
        del testNotifications[0]
        yield "data:" + str(json.dumps({'message':temp, 'type': 'good'})) + "\n\n"

        
    return Response(generator(), mimetype='text/event-stream')
        

@notification_api.route("/postNotification", methods=["POST"])
def postTestNotification():
    global lol
    global testNotifications
    testNotifications.append("This is test Notification #" + str(lol))

    lol+=1
    return ""