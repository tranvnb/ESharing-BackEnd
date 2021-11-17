from flask import Blueprint
purchase_routes = Blueprint("purchase", __name__)


@purchase_routes.route("/add", methods=['POST'])
def add(purchase):
    return "/purchase/add"


@purchase_routes.route("/remove", methods=['DELETE'])
def remove(id):
    return "/purchase/remoive"


@purchase_routes.route("/update", methods=['PUT'])
def update(purchase):
    return "/purchase/update"


@purchase_routes.route("/<int:id>", methods=['GET'])
def findById(id):
    return "find by Id: {}".format(id)
