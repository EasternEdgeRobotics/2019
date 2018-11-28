from flask import Blueprint, Flask, render_template, jsonify, request

notification_api = Blueprint("notification_api", __name__)

@notification_api.route("/testNotificationsPage")
def loadNotificationTestPage():
    return render_template("notificationsTest.html")