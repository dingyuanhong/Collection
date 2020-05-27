import datetime
from bson import ObjectId

def NowDateTime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class Base:
    def __init__(self,db,name):
        self.db = db;
        self.name = name;
    
    def DB(self):
        return self.db.db;

    def collection(self):
        return self.db.db[self.name];

    def insert(self,job):
        job_id = self.collection().insert({**job,**{"create_time":NowDateTime() }});
        return str(job_id)

    def remove(self,job_id):
        res = self.collection().remove({
            "_id":ObjectId(job_id)
        })
        return res;

    def find(self,job_id):
        data = self.collection().find_one({"_id":ObjectId(job_id)});
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

    def find_jobs(self,job_ids):
        for i in range(len(job_ids)):
            job_ids[i] = ObjectId(job_ids[i]);
        
        data = self.collection().find( {"_id":{"$in":job_ids} });
        lst = [];
        for it in data:
            it["id"] = str(it["_id"])
            del it["_id"];
            lst.append(it);
        return lst;
    
    def remove_jobs(self,job_ids):
        for i in range(len(job_ids)):
            job_ids[i] = ObjectId(job_ids[i]);
        
        res = self.collection().remove( {"_id":{"$in":job_ids} });
        return res;

    def find_some(self,options):
        if("_id" in options):
            options["_id"] = ObjectId(options["_id"]);
        
        data = self.collection().find( options );
        lst = [];
        for it in data:
            it["id"] = str(it["_id"]);
            del it["_id"];
            lst.append(it);
        return lst;