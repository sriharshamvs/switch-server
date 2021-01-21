from flask import Blueprint, jsonify, request
from smartHome.models import User, Topics, TopicsSchema, UserSchema
from smartHome import utils

user_route = Blueprint('user', __name__)

topics_schema = TopicsSchema(many=True)
user_schema = UserSchema(many=True)

@user_route.route('/api/test')
def testRoute():
    return jsonify({
        "status": 200,
        "message": "You are in Test Route"
    })


@user_route.route('/api/auth', methods=["POST"])
def getDevices():
    requestData = request.get_json()
    try:
        user_details = User.find_by_username(requestData['username'])
        if user_details:
            if utils.check_password(user_details.password_hash, requestData['password']):
                if user_details.username == 'admin':
                    deviceData = topics_schema.dump(Topics.find_all())
                    users = user_schema.dump(User.find_all())
                    data = {"room": user_details.room, "devices": deviceData, "users": users}
                else:
                    deviceData = topics_schema.dump(Topics.find_by_room(user_details.room))
                    data = {"room": user_details.room, "devices": deviceData}
                return jsonify({
                    "message": "You are Authenticated",
                    "data": data
                }), 200
            else:
                return jsonify({
                    "message": "You are Not Authenticated",
                }), 401
        else:
            return jsonify({
                "message": "You are Not Authenticated",
            }), 401
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")
        return jsonify({
            "message": "You are Not Authenticated"
        }), 500
