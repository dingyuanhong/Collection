
from .base import NowDateTime,Base
from bson import ObjectId

class Job(Base):
    def __init__(self,db):
        super(Job, self).__init__(db,"job")
    
    def insert(self,job):
        job_id = self.collection().insert({**job,**{"status":"active","create_time":NowDateTime() }});
        return str(job_id)

    def update_status(self,job_id,status):
        self.collection().update_one({"_id":ObjectId(job_id)},{'$set':{"status":status}});

    def find_by_status(self,status):
        data = self.collection().find({"status":status});
        lst = []
        for it in data:
            lst.append(str(it["_id"]));
        return lst;

    def set_result(self,job_id,result):
        self.DB().job_result.insert({
            "job_id":job_id,
            "result":result,
            "create_time":NowDateTime(),
        });