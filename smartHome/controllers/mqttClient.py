from smartHome import mqttc
from smartHome.models import Topics, TopicsSchema
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

topic_schema = TopicsSchema(many=True)

mqtt_route = Blueprint('mqtt_route', __name__)


def publishData(requestData):
      username = requestData['username']
      room = requestData['room']
      device = requestData['device']
      action = requestData['action']

      try:
          dbTopic = Topics.find_by_room_and_device(room, device)
          if dbTopic:
            if action == "ON":
                mqttc.publish(dbTopic[0].topic, "0")
                print('Published : {}'.format(dbTopic[0].topic))
            if action == "OFF":
                mqttc.publish(dbTopic[0].topic, "1")
                print('Published : {}'.format(dbTopic[0].topic))
            Topics.find_device_and_update(action, dbTopic[0].topic)
            if username == "admin":
                room = '0'
                deviceData = topic_schema.dump(Topics.find_all())
            else:
                deviceData = topic_schema.dump(Topics.find_by_room(room))
              
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
      devices = Topics.find_by_room(room)
      for device in devices:
        mqttc.publish(device.topic, action)
      Topics.update_all(status, room)
      deviceData = topic_schema.dump(Topics.find_by_room(room))
      data = {"room": room, "deviceData" : deviceData}
      return {
          "message": "Request Sucessful",
          "data": data 
        }, 200
      print("Room Reset")
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")
        return {"message": "Server Error"}, 500


@mqtt_route.route("/api/dashboard", methods=['POST'])
@jwt_required
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
@jwt_required
def resetAll():
   requestData = request.get_json()
   if requestData:
      message, statusCode = statusRest(requestData)
      return jsonify(message), statusCode
   else:
      return jsonify({
         "message": "Bad Request"
      }), 400
