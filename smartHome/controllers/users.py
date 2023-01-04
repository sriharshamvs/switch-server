from smartHome import db_location
from flask import Blueprint, jsonify, request
import sqlite3


user_route = Blueprint('user', __name__)


def find_user_by_username(username):
    connection = sqlite3.connect(db_location)
    cursor = connection.cursor()
    query = "SELECT * FROM users WHERE username=?"
    result = cursor.execute(query, (username,))
    row = result.fetchone()
    connection.close()
    if row:
        return row

def find_all_users():
    connection = sqlite3.connect(db_location)
    cursor = connection.cursor()
    query = "SELECT username, room FROM users WHERE username != 'admin'"
    rows = cursor.execute(query, ())
    if rows:
        keys = ['user', 'room']
        users = [dict(zip(keys, rows)) for rows in cursor.fetchall()]
        connection.close()
        return users

def find_topics_by_room(room):
    connection = sqlite3.connect(db_location)
    cursor = connection.cursor()
    query = "SELECT room, device, status, icon, location FROM topics WHERE room=?"
    row = cursor.execute(query, (room,))
    if row:
        keys = ['room', 'device', 'status', 'icon', 'location']
        deviceData = [dict(zip(keys, row)) for row in cursor.fetchall()]
        connection.close()
        return deviceData


def find_all_topics():
    connection = sqlite3.connect(db_location)
    cursor = connection.cursor()
    query = "SELECT room, device, status, icon, location FROM topics"
    rows = cursor.execute(query, ())
    if rows:
        keys = ['room', 'device', 'status', 'icon', 'location']
        deviceData = [dict(zip(keys, rows)) for rows in cursor.fetchall()]
        connection.close()
        return deviceData


@user_route.route('/api/test')
def testRoute():
    return jsonify({
        "status": 200,
        "message": "You are in Test Route"
    })


@user_route.route('/api/auth', methods=["POST"])
def getDevices():
    requestData = request.get_json()
    user = requestData['username']
    password = requestData['password']
    try:
        dbUser = find_user_by_username(user)
        if dbUser[1] == password:
            if dbUser[0] == 'admin':
                deviceData = find_all_topics()
                users = find_all_users()
                print("Users: ", users)
                data = {"room": dbUser[2], "devices": deviceData, "users": users}
                pass
            else:
                deviceData = find_topics_by_room(dbUser[2])
                data = {"room": dbUser[2], "devices": deviceData}
            return jsonify({
                "message": "You are Authenticated",
                "data": data
            }), 200
        else:
            return jsonify({
                "message": "You are Not Authenticated"
            }), 401
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")
        return jsonify({
            "message": "You are Not Authenticated"
        }), 500
