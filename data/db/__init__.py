from .table import *
import db.mongo as db
import logging

client = db.mongoClient()

def getDB(arg):
    global client

    db = client["data"];
    if arg["NAME"] == "company":
        collection = Company(db,arg["PREFIX"])
        return collection
    if arg["NAME"] == "quotation":
        collection = Quotation(db,arg["PREFIX"])
        return collection
    if arg["NAME"] == "stock":
        collection = Stock(db,arg["PREFIX"])
        return collection
    
    if arg["NAME"] == "minute":
        collection = Minute(db,arg["PREFIX"])
        return collection
    if arg["NAME"] == "day":
        collection = Day(db,arg["PREFIX"])
        return collection
    if arg["NAME"] == "month":
        collection = Month(db,arg["PREFIX"])
        return collection
    if arg["NAME"] == "week":
        collection = Week(db,arg["PREFIX"])
        return collection
    
    logging.error(arg);
    return None;