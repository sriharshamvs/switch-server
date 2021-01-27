from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import paho.mqtt.client as mqtt
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, get_jwt_identity
)
import sqlite3
import os
import datetime

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_location = BASE_DIR + '/smartHome_2.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + BASE_DIR + '/smartHome_2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'harshamvs'  # Change this!

expires = datetime.timedelta(days=7)

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = expires

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

mqttc = mqtt.Client()
mqttc.connect("localhost", 1883, 60)
mqttc.loop_start()


# Blueprints
from smartHome.controllers.mqttClient import mqtt_route
from smartHome.controllers.users import user_route
from smartHome.models import Topics, TopicsSchema

app.register_blueprint(user_route)
app.register_blueprint(mqtt_route)


def action_on_reboot():
    devices = Topics.find_all()
    for device in devices:
        if device.status == "ON":
            action = "0"
        elif device.status == "OFF":
            action = "1"
        mqttc.publish(device.topic, action)
        print('Published: room: {} topic: {} status: {}'.format(device.room, device.topic, device.status))


action_on_reboot()


@app.route("/")
def main():
    return jsonify({
        "messages": "Sever Running on Port 5000"
    }), 200


@app.route("/api/ping")
def ping():
    return jsonify({
        "messages": "Sever Up"
    }), 200

@app.route('/api/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    token = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify({
        "token": token
    }), 200


@app.route("/robots.txt")
def robots_dot_txt():
    return "User-agent: *\nDisallow: /"
