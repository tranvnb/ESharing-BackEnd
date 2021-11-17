from pymongo import MongoClient
from routes.user_route import user_routes
from routes.purchase_route import purchase_routes
from os import environ

from flask import Flask, g

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# app config
app.config.from_pyfile('config.py')
app.config.update(dict(SECRET_KEY=environ.get("SECRET_KEY")))


app.register_blueprint(user_routes, url_prefix="/user")
app.register_blueprint(purchase_routes, url_prefix="/purchase")


@ app.route("/")
def home():
    print(app.config)
    return "App is running!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
