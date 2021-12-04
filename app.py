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
app.config.from_pyfile("config.py")
app.config.update(dict(SECRET_KEY=environ.get("SECRET_KEY")))


app.register_blueprint(user_routes, url_prefix="/user")
app.register_blueprint(purchase_routes, url_prefix="/purchase")

socketio = SocketIO(app)
users = {}

@socketio.on("USER_ONLINE_CHANNEL")
def subscribe_user_to_online_channel(data):
    users[data] = request.sid
    return True

@socketio.on("JOIN_HOUSEHOLD_REQUEST")
def request_join_household(data):
    # print(data)
    # print(json_util.dumps(data))
    
    # json = json_util.loads(json_util.dumps(data))

    json = data
    person = json["FROM_USER"]
    owner = json["TO_OWNER"]
    # print("JOIN_HOUSEHOLD_REQUEST from " + person + " to " + owner)
    message = {"FROM_USER": person, "TO_OWNER": owner}
    print("JOIN_HOUSEHOLD_REQUEST: " + str(message))
    if owner in users.keys():
        # print("JOIN_HOUSEHOLD_REQUEST from " + person + " to " + owner)
        emit("JOIN_HOUSEHOLD_REQUEST", message, room = users[owner])
    else:
        # print("emit JOIN_HOUSEHOLD_REQUEST_RESPONSE")
        emit("JOIN_HOUSEHOLD_REQUEST_RESPONSE_NOT_EXIST", {"MESSAGE":"Your requested owner does not exist"}, room = users[person])

@socketio.on("JOIN_HOUSEHOLD_REQUEST_RESPONSE")
def resonse_from_house_owner(data):
    
    # json = json_util.loads(json_util.dumps(data))
    print ("==================", data)
    json = data
    user = json["TO_USER"]
    owner = json["FROM_OWNER"]
    message = json["MESSAGE"]
    approved = json["APPROVED"]
    print("emit JOIN_HOUSEHOLD_REQUEST_RESPONSE from owner reply")
    emit("JOIN_HOUSEHOLD_REQUEST_RESPONSE", {"MESSAGE":"Message from the " + owner +": " + message, "APPROVED": approved, "FROM_OWNER": owner} , room = users[user])

@socketio.on("REMOVED_MEMBER_FROM_HOUSEHOLD")
def being_removed_from_household(data):
    json = data
    user = json["TO_USER"]
    owner = json["FROM_OWNER"]
    message = json["MESSAGE"]
    message = {"FROM_OWNER": owner, "TO_USER": user, "MESSAGE": "You were removed from our house"}
    emit("BEING_REMOVED_FROM_HOUSEHOLD", message, room = users[user])

@socketio.on("USER_DISCONNECT")
def user_disconnect(data):
    users.pop(data)

@socketio.on('disconnect')
def test_disconnect():
    # users.pop(data)
    print('Client disconnected', request.sid)

@ app.route("/")
def home():
    print(app.config)
    return "App is running!"



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
