from pymongo import MongoClient
from app.config import settings

def get_database():
    client = MongoClient(settings.MONGODB_URI)
    return client[settings.DATABASE_NAME]

def get_collection():
    db = get_database()
    return db[settings.COLLECTION_NAME]