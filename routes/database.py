from pymongo import MongoClient
from os import environ
from dotenv import load_dotenv


load_dotenv()


def get_db():
    client = MongoClient(environ.get("DATABASE_URL"))
    db = client['esharing-database']
    return db
