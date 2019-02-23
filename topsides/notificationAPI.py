"""Notification API."""
from flask import Blueprint, render_template, Response
import json


notification_api = Blueprint("notification_api", __name__)
notification_api.threaded = True

topsidesComms = None


def notificationAPI(comms):
    """Returns the test page for notifications."""
    global topsidesComms
    topsidesComms = comms
    return notification_api


@notification_api.route("/testNotificationsPage")
def loadNotificationTestPage():
    return render_template("notificationsTest.html")


@notification_api.route("/notificationTest")
def notificationTest():
    """Returns the next notification in the test array."""
    def generator():
        yield "data:" + str(json.dumps({'message': topsidesComms.received.get(), 'type': 'info'})) + "\n\n"
 
    return Response(generator(), mimetype='text/event-stream')


@notification_api.route("/postNotification", methods=["POST"])
def postTestNotification():
    """Adds a test notification to the test notification array."""
    global lol
    global testNotifications
    testNotifications.append("This is test Notification #" + str(lol))

    lol += 1
    return ""
