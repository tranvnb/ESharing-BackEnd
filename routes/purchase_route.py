from flask import Blueprint, request
from flask.json import jsonify
import json
from bson import json_util
from .database import get_db
purchase_routes = Blueprint("purchase", __name__)


@purchase_routes.route("/add", methods=['POST'])
def add():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    purchase = data.get("purchase")

    db = get_db()
    db.users.find_one_and_update(
        {"username": username, "password": password}, {"$push": {"purchases": purchase}}, upsert=True)
    return jsonify({"message": "Purchase added."})


@purchase_routes.route("/<string:id>", methods=['DELETE'])
def remove(id):
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    # should prevent access database if invalid data
    db = get_db()
    db.purchases.update_one(
        {"username": username, "password": password}, {"$pull": {"purchases": {"id": id}}})
    return jsonify({"message": "Purchase removed."})


@ purchase_routes.route("/<string:id>", methods=['PUT'])
def update(id):
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    purchase = data.get("purchase")
    # make sure it always has id for further query
    purchase["id"] = id
    # NOTE: make sure all the properties of purchase are submitted.
    db = get_db()
    db.users.find_one_and_update(
        {"username": username, "password": password, "purchases.id": id}, {"$set": {"purchases.$[]": purchase}}, upsert=True)
    return jsonify({"message": "Purchase updated."})


@ purchase_routes.route("/<string:id>", methods=['GET'])
def findById(id):
    # TODO: should allow only in household, otherwise return false
    data = request.get_json()
    username = data.get("username")
    db = get_db()
    purchase = db.users.find_one(
        {"username": username, "purchases.id": id})
    return json.dumps(purchase, sort_keys=True, indent=2, default=json_util.default)


@ purchase_routes.route("/all", methods=['DELETE'])
def findById():
    # TODO: should allow only in household, otherwise return false
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    db = get_db()
    purchase = db.users.update_one(
        {"username": username, "password": password}, {"$set": {"purchases": []}})
    return jsonify({"message": "All purchases removed."})