from flask import Blueprint, jsonify, make_response
from flask.globals import request
import json
from bson import json_util
from .database import get_db
user_routes = Blueprint("user", __name__)


@user_routes.route("/")
def find_all_user():
    # for testing only
    db = get_db()
    # member must be alone and not have any member
    # added_members = db.users.find_one(
    #     {"username": "username"}, {"members": True})

    # print(len([]))
    # print(len(added_members.get("members")))

    users = list(db.users.find({}))

    users_dicts = [doc for doc in users]

    # serialize to json string
    users_json_string = json.dumps(users_dicts, default=json_util.default)
    return jsonify({"users": json.loads(users_json_string)})
    # return jsonify({"users": json_util.dumps(users)})


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


@user_routes.route("/add-member", methods=["POST"])
def add_member():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    member = data.get("member")
    if (member is not None and username is not None and password):
        db = get_db()
        user = db.users.find_one({
            "username": username,
            "password": password,
            "is_owner": True})
        if (user is None):
            return make_response(jsonify({"message": "you dont have permission to add member"}), 403)

        # member must be alone and not have any member
        added_member = db.users.find_one(
            {"username": "username"}, {"members": True})
        if (added_member.get("members") is not None and len(added_member.get("members")) > 0):
            return make_response(jsonify({"message": "Can not add member to your household, member must be alone."}), 403)

        # add member to household
        db.users.update_one(
            {"username": username},
            {"$push": {"members": member}},
            upsert=True
        )

        # change member owner to false, they are not on their own anymore
        db.users.update_one(
            {"username": member},
            {"$set": {"is_owner": False}}
        )

        return jsonify({"message": "member was added to household"})
    else:
        return make_response(jsonify({"message": "Invalid request"}), 403)


@ user_routes.route("remove-member", methods=["POST"])
def remove_member():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    member = data.get("member")
    if (member is not None and username is not None and password):
        db = get_db()
        user = db.users.find_one({
            "username": username,
            "password": password,
            "is_owner": True})
        if (user is None):
            return make_response(jsonify({"message": "you dont have permission to remove member"}), 403)

        # remove from household
        db.users.update_one(
            {"username": username},
            {"$pull": {"members": member}}
        )

        # set the removed member to the owner on their own
        db.users.update_one(
            {"username": username},
            {"$set": {"is_owner": True}}
        )

        return jsonify({"message": "member was removed from household"})
    else:
        return make_response(jsonify({"message": "Invalid request"}), 403)
