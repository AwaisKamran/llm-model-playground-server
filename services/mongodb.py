from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

mongoClient = None

def connect_to_mongodb():
    uri = "mongodb+srv://awaiskamran:_CrrfQZTZ$6$Y-P@llm-playground.ccnjzzh.mongodb.net/?retryWrites=true&w=majority&appName=llm-playground"
    mongoClient = MongoClient(uri, server_api=ServerApi('1'))
    try:
        mongoClient.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    return mongoClient

def get_mongodb_client():
    return mongoClient