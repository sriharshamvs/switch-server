from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import paho.mqtt.client as mqtt
import sqlite3
import os

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# db_location = BASE_DIR + '/smartHome.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + BASE_DIR + '/smartHome_2.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)


# mqttc = mqtt.Client()
# mqttc.connect("localhost", 1883, 60)
# mqttc.loop_start()


# Blueprints
# from smartHome.controllers.mqttClient import mqtt_route
from smartHome.controllers.users import user_route

app.register_blueprint(user_route)
# app.register_blueprint(mqtt_route)


# def find_all_topics():
#     connection = sqlite3.connect(db_location)
#     cursor = connection.cursor()
#     query = "SELECT * FROM topics"
#     row = cursor.execute(query)
#     if row:
#         keys = ['room', 'device', 'topic', 'status', 'icon']
#         devices = [dict(zip(keys, row)) for row in cursor.fetchall()]
#         connection.close()
#         return devices


# def action_on_reboot():
#     devices = find_all_topics()
#     for device in devices:
#         if device['status'] == "ON":
#             action = "0"
#         elif device['status'] == "OFF":
#             action = "1"
#         mqttc.publish(device['topic'], action)
#         print('Published {}'.format(device))


# action_on_reboot()


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


@app.route("/robots.txt")
def robots_dot_txt():
    return "User-agent: *\nDisallow: /"
