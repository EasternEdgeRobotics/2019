"""Notification API."""
from flask import Blueprint, render_template, Response, Flask, copy_current_request_context
from flask_socketio import SocketIO, emit
import threading
import time
import json
import queue


"""
pip install flask-socketio
"""

notification_api = Blueprint("notification_api", __name__)
notification_api.threaded = True

notificationQueue = queue.Queue()

socketio = None

def notificationAPI():
    """Returns the test page for notifications."""
    t = threading.Thread(target=emitNotifications)
    t.start()
    return notification_api


def emitNotifications():
    global notificationQueue
    while(True):
        if(notificationQueue.qsize() > 0):
            socketio.emit('notification', notificationQueue.get(timeout=1), namespace='/notification/stream', broadcast=True )
        time.sleep(0.5)


def putNotification(msg, msg_type):
    global notificationQueue
    types = ["info", "success", "warning", "danger"]
    if(msg_type not in types):
        msg_type = types[0]
    
    notificationQueue.put({"msg": msg, "type": msg_type})



def socketSetup(socket):
    global socketio
    socketio = socket

    """
    @socketio.on("connect", namespace="/notification/stream")
    def connection():
        print("New Connection")
    """



@notification_api.route("/testNotificationsPage")
def loadNotificationTestPage():
    return render_template("notificationsTest.html")



@notification_api.route("/put", methods=["GET"])
def temp():
    putNotification("test", "info")
    return "done"