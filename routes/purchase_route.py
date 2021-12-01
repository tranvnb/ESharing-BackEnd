from flask import Blueprint, request
from flask.helpers import make_response
from flask.json import jsonify
import json
from bson import json_util
from .database import get_db
purchase_routes = Blueprint("purchase", __name__)


@purchase_routes.route("/add", methods=['POST'])
def add():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    purchase = data["purchase"]
    db = get_db()
    db.users.find_one_and_update(
        {"username": username, "password": password}, {"$push": {"purchases": purchase}}, upsert=True)
    return jsonify({"message": "Purchase added."})


@purchase_routes.route("/<string:id>", methods=['DELETE'])
def remove(id):
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    # should prevent access database if invalid data
    db = get_db()
    db.users.update_one(
        {"username": username, "password": password}, {"$pull": {"purchases": {"id": id}}})
    return jsonify({"message": "Purchase removed."})


@ purchase_routes.route("/<string:id>", methods=['PUT'])
def update(id):
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    purchase = data["purchase"]
    # make sure it always has id for further query
    purchase["id"] = id
    # NOTE: make sure all the properties of purchase are submitted.
    db = get_db()
    db.users.find_one_and_update(
        {"username": username, "password": password, "purchases.id": id}, {"$set": {"purchases.$[]": purchase}}, upsert=True)
    return jsonify({"message": "Purchase updated."})


@ purchase_routes.route("/<string:member>/<string:id>", methods=['POST'])
def findMemberPurchaseById(member, id):
    # TODO: should allow only in household, otherwise return false
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    db = get_db()

    user = db.users.find_one(
        {"username": username, "password": password, "members": {"$in":[member]}})

    if (user is None):
        return make_response(jsonify({"message": "you dont have permission to view this purchases"}), 403)

    purchase = db.users.find_one(
        {"username": member, "purchases.id": id})
    return json.dumps(purchase, sort_keys=True, indent=2, default=json_util.default)


@ purchase_routes.route("/all", methods=['DELETE'])
def deleteAll():
    # TODO: should allow only in household, otherwise return false
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    db = get_db()
    purchase = db.users.update_one(
        {"username": username, "password": password}, {"$set": {"purchases": []}})
    return jsonify({"message": "All purchases removed."})