import os
from pymongo import MongoClient
from dotenv import load_dotenv


load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["laptopdb"]

laptops_collection = db["laptops"]
users_collection = db["users"]
