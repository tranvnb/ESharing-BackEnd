from flask import Blueprint, jsonify, make_response, request
import json
from bson import json_util
from .database import get_db
user_routes = Blueprint("user", __name__)


@user_routes.route("/all", methods=["GET"])
def find_all_user():
    db = get_db()
    users = db.users.find({})
    return jsonify(json.loads(json_util.dumps(users)))

@user_routes.route("/<string:username>/members", methods=["GET"])
def getMembers(username):
    db = get_db()
    # member must be alone and not have any member
    user = db.users.find_one(
        {"username": username}, {"members": True})
    if (user is None):
        return make_response(jsonify({"message": "user not exist"}), 403)
    members = user.get("members")
    return jsonify(json.loads(json_util.dumps(members)))

@user_routes.route("/<string:username>/purchases", methods=["GET"])
def getPurchases(username):
    db = get_db()
    # member must be alone and not have any member
    user = db.users.find_one(
        {"username": username}, {"purchases": True})
    if (user is None):
        return make_response(jsonify({"message": "user not exist"}), 403)
    purchases = user.get("purchases")
    return jsonify(json.loads(json_util.dumps(purchases)))

@user_routes.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    print(data)
    username = data.get("username")
    password = data.get("password")
    user = get_db().users.find_one(
        {"username": username, "password": password})
    if (user):
        return jsonify({"message": "Successful login"})
    else:
        return make_response(jsonify({"message": "Unsuccessful login"}), 401)


@user_routes.route("/logout", methods=['POST'])
def logout():
    return True


@user_routes.route("/signup", methods=["POST"])
def signup():
    
    data = request.get_json()
    print("User signuppppp", data)
    db = get_db()
    username = data.get("username")
    password = data.get("password")
    if (db.users.find_one({"username": username}) is not None):
        return make_response(jsonify({"message": "User already exists!"}), 403)

    id = data.get("id")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    is_owner = data.get("is_owner")
    # members = data.get("members")
    members = []
    user = {
        "id": id,
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
            {"username": member}, {"members": True})

        if (added_member is None):
            return make_response(jsonify({"message": "Added member not exists"}), 403)
        
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
            {"username": member},
            {"$set": {"is_owner": True}}
        )

        return jsonify({"message": "member was removed from household"})
    else:
        return make_response(jsonify({"message": "Invalid request"}), 403)
