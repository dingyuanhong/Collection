import os
from pymongo import MongoClient

def mongoClient():
    MONGODB_DB_URL = os.environ.get('MONGODB_DB_URL') if os.environ.get('MONGODB_DB_URL') else 'mongodb://10.0.0.116:27017/'
    client = MongoClient(MONGODB_DB_URL)
    return client;

class MongoFactory:
    def __init__(self):
        self.client = mongoClient();

        MONGODB_DB_NAME = os.environ.get('APP_NAME') if os.environ.get('APP_NAME') else 'server'
        self.db = self.client[MONGODB_DB_NAME];
    
    def Client(self):
        return self.client;