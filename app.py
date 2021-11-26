from pymongo import MongoClient
from routes.user_route import user_routes
from routes.purchase_route import purchase_routes
from os import environ
import json
from bson import json_util
from flask_socketio import SocketIO, emit


from flask import Flask, g, request

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# app config
app.config.from_pyfile('config.py')
app.config.update(dict(SECRET_KEY=environ.get("SECRET_KEY")))


app.register_blueprint(user_routes, url_prefix="/user")
app.register_blueprint(purchase_routes, url_prefix="/purchase")

socketio = SocketIO(app)
users = {}

@socketio.on('USER_ONLINE_CHANNEL')
def subscribe_user_to_online_channel(data):
    # print(data) # this is just to verify/see the data received from the client
    # users[data] = request.sid # the session id is "saved"
    # print("user connected USER_ONLINE_CHANNEL" + data)
    # print(data)
    # print(request.sid)
    users[data] = request.sid

@socketio.on('JOIN_HOUSEHOLD_REQUEST')
def request_join_household(data):
    # print(data)
    # print(json_util.dumps(data))
    json = json_util.loads(json_util.dumps(data))
    person = json.get("FROM_USER")
    owner = json.get("TO_OWNER")
    # print("JOIN_HOUSEHOLD_REQUEST from " + person + " to " + owner)
    message = "{\"FROM_USER\":\"" + person +"\", \"TO_OWNER\":\"" + owner + "\"}"
    print("JOIN_HOUSEHOLD_REQUEST: " + message)
    if owner in users.keys():
        emit('JOIN_HOUSEHOLD_REQUEST', message, room = users[owner])
    else:
        emit('JOIN_HOUSEHOLD_REQUEST_RESPONSE', "Your requested owner does not exist", room = users[person])

@ app.route("/")
def home():
    print(app.config)
    return "App is running!"



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
