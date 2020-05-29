import datetime
from bson import ObjectId
import logging

def NowDateTime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class Base:
    def __init__(self,db,name):
        self.db = db;
        self.name = name;
    
    def DB(self):
        return self.db;

    def collection(self):
        return self.DB()[self.name];

    def insert(self,data):
        id_ = self.collection().insert({**data,**{"create_time":NowDateTime() }});
        return str(id_)

    def remove(self,id_):
        res = self.collection().remove({
            "_id":ObjectId(id_)
        })
        return res;

    def find(self,id_):
        data = self.collection().find_one({"_id":ObjectId(id_)});
        if(data == None):
            return None;
        data["id"] = str(data["_id"]);
        del data["_id"];
        return data;
    
    def all(self):
        data = self.collection().find();
        lst = [];
        for it in data:
            it["id"] = str(it["_id"])
            del it["_id"];
            lst.append(it);
        return lst;
    
    def append(self,data,index):
        # logging.error("DB append:")
        # logging.error(self.collection());
        # logging.error(index);
        # logging.error(data)
        
        #主键
        if index:
            keys = {};
            for it in index:
                if it in data:
                    keys[it] = data[it]
                else:
                    logging.warn(str(data)+"\n"+str(it)+":未找到")
            return self.collection().update(keys,{"$setOnInsert": { **data, **{"create_time":NowDateTime()} }}, True );
        else:
            return self.insert(data);