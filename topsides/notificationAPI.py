from flask import Blueprint, Flask, render_template, jsonify, request, Response
import time


notification_api = Blueprint("notification_api", __name__)
notification_api.threaded = True

lol = 0
testNotifications = []


@notification_api.route("/testNotificationsPage")
def loadNotificationTestPage():
    return render_template("notificationsTest.html")

@notification_api.route("/notificationTest")
def notificationTest():

    def generator():
        global testNotifications
        while len(testNotifications) <= 0:
            None

        temp = testNotifications[0]
        del testNotifications[0]
        print(testNotifications[0])
        yield "data:" + temp + "\n\n"

        
    return Response(generator(), mimetype='text/event-stream')
        

@notification_api.route("/postNotification", methods=["POST"])
def postTestNotification():
    global lol
    global testNotifications
    testNotifications.append("This is test Notification #" + str(lol))

    lol+=1
    return ""