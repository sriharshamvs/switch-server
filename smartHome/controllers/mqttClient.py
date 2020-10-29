from smartHome import mqttc, db_location
from flask import Blueprint, jsonify, request
import sqlite3


mqtt_route = Blueprint('mqtt_route', __name__)


def find_topics_by_room(room):
    connection = sqlite3.connect(db_location)
    cursor = connection.cursor()
    query = "SELECT room, device, status, icon FROM topics WHERE room=?"
    row = cursor.execute(query, (room,))
    if row:
        keys = ['room', 'device', 'status', 'icon']
        deviceData = [dict(zip(keys, row)) for row in cursor.fetchall()]
        connection.close()
        return deviceData

def find_all_topics():
    connection = sqlite3.connect(db_location)
    cursor = connection.cursor()
    query = "SELECT room, device, status, icon FROM topics"
    row = cursor.execute(query, ())
    if row:
        keys = ['room', 'device', 'status', 'icon']
        deviceData = [dict(zip(keys, row)) for row in cursor.fetchall()]
        connection.close()
        return deviceData

def find_topic_by_room_and_device(room, device):
    connection = sqlite3.connect(db_location)
    cursor = connection.cursor()
    query = "SELECT * FROM topics WHERE room=? AND device=?"
    result = cursor.execute(query, (room, device))
    row = result.fetchone()
    connection.close()
    if row:
        return row


def find_device_and_update(action, room, device):
    connection = sqlite3.connect(db_location)
    cursor = connection.cursor()
    query = "UPDATE topics SET status=? WHERE room=? AND device=?"
    cursor.execute(query, (action, room, device))
    connection.commit()
    connection.close()


def update_all(action, room):
    connection = sqlite3.connect(db_location)
    cursor = connection.cursor()
    query = "UPDATE topics SET status=? WHERE room=?"
    cursor.execute(query, (action, room))
    connection.commit()
    connection.close()


def publishData(requestData):
      user = requestData['user']
      room = requestData['room']
      device = requestData['device']
      action = requestData['action']

      try:
          dbTopic = find_topic_by_room_and_device(room, device)
          if dbTopic:
            if action == "ON":
                mqttc.publish(dbTopic[2], "0")
                print('Published : {}'.format(dbTopic))
            if action == "OFF":
                mqttc.publish(dbTopic[2], "1")
                print('Published : {}'.format(dbTopic))
            find_device_and_update(action, room, device)
            deviceData = find_all_topics() if user == 'admin' else find_topics_by_room(room)
            if user == 'admin':
              room = '0'
            data = {"room": room, "devices": deviceData}
            return {
                "message": "Request Sucessful",
                "data": data
            }, 200
          else:
            return {"message": "Server Error"}, 500
      except Exception as e:
         print("Oops!", e.__class__, "occurred.")
         return {"message": "Server Error"}, 500


def statusRest(requestData):
    room = requestData['room']
    status = requestData['reset']
    try:
      if status == "ON":
        action = "0"
      elif status == "OFF":
        action = "1"
      devices = find_topics_by_room(room)
      for device in devices:
        mqttc.publish(device['topic'], action)
      update_all(status, room)
      print("Room Reset")
      return { "message": "Request Sucessful" }, 200
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")
        return {"message": "Server Error"}, 500


@mqtt_route.route("/api/dashboard", methods=['POST'])
def dashboard():
   requestData = request.get_json()
   if requestData:
      message, statusCode = publishData(requestData)
      return jsonify(message), statusCode
   else:
      return jsonify({
         "message": "Bad Request"
      }), 400


@mqtt_route.route("/api/dashboard/reset", methods=['POST'])
def resetAll():
   requestData = request.get_json()
   if requestData:
      message, statusCode = statusRest(requestData)
      return jsonify(message), statusCode
   else:
      return jsonify({
         "message": "Bad Request"
      }), 400
