from flask import Blueprint, jsonify, make_response
from flask.globals import request
from .database import get_db
user_routes = Blueprint("user", __name__)


@user_routes.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    print(data)
    username = data.get("username")
    password = data.get("password")
    user = get_db().users.find_one(
        {"username": username, "password": password})
    if (user):
        return jsonify(data)
    else:
        return make_response(jsonify({"message": "Unsuccessully login"}), 403)


@user_routes.route("/logout", methods=['POST'])
def logout():
    return True


@user_routes.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    db = get_db()
    username = data.get("username")
    password = data.get("password")
    if (db.users.find_one({"username": username}) is not None):
        return make_response(jsonify({"message": "User already exists!"}), 403)

    first_name = data.get("first_name")
    last_name = data.get("last_name")
    is_owner = data.get("is_owner")
    members = data.get("members")
    user = {
        "username": username,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
        "is_owner": is_owner,
        "members": members
    }
    user_id = db.users.insert_one(user).inserted_id
    return jsonify({"id": str(user_id)})
