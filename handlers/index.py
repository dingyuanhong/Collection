import os
from handlers.register import *
from bson import ObjectId

import json
import tornado.web
from tornado import web
import datetime
from db.table.task import Task
from db.table.job import Job
from db.table.timer import Timer
from db.table.exector import Exector

class BaseHandler(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

class DBHanlder(BaseHandler):
    def DB(self):
        return None;
    def post(self,cmd):
        db = self.DB();
        if db == None:
            self.write({ "success":0});
            return;

        if cmd == "all":
            self.write( json.dumps(  { "success":1,"data": db.all() } ) );
            return;

        if cmd == "get":
            data = json.loads(self.request.body);
            record_ids = [data["id"]];
            self.write( json.dumps( { "success":1,"data":db.find_jobs(record_ids) } ) );

        if cmd == "add":
            data = json.loads(self.request.body);
            record_id = db.insert(data);
            self.write(json.dumps({"success":1,"id": record_id }));

        if cmd == "del":
            data = json.loads(self.request.body);
            record_id = data["id"];
            res = db.remove(record_id);
            self.write(json.dumps({"success":int(res['ok']),"count":res['n']}));

@fm.route(r"/api/task/([a-z-_ .]+)")
class TaskHandler(DBHanlder):
    def DB(self):
        return Task(self.application.db);

@fm.route(r"/api/timer/([a-z-_ .]+)")
class TimerHandler(DBHanlder):
    def DB(self):
        return Timer(self.application.db);

@fm.route(r"/api/job/([a-z-_ .]+)")
class JobHandler(DBHanlder):
    def DB(self):
        return Job(self.application.db);

def adjustmentTiming(timing):
    type_ = timing["type"];
    del timing["type"];
    timer = {"type":type_,"param":timing}
    return timer;

@fm.route(r"/api/exec/([a-z-_ .]+)")
class ExecHandler(BaseHandler):
    def post(self,cmd):
        task = Task(self.application.db);
        job = Job(self.application.db);
        timer = Timer(self.application.db);
        exector = Exector(self.application.db);
        scheduler = self.application.scheduler;

        if cmd == "exec":
            data = json.loads(self.request.body);
            task_id = data["id"];

            res = task.find(task_id);
            if res == None:
                self.write(json.dumps({"success":0,"message":"no task"}));
                return;

            res = scheduler.Exec(res);
            self.write(json.dumps({"success":1,"data":res}));

        if cmd == "fixtime":
            data = json.loads(self.request.body);
            task_id = data["id"];

            res = task.find(task_id);
            if res == None:
                self.write(json.dumps({"success":0,"message":"no task"}));
                return;

            timing = adjustmentTiming(data["timing"]);
            print(timing)
            timing["task_id"] = task_id;
            timer_id = timer.insert(timing);
            timing["id"] = timer_id;

            res = scheduler.ExecByTimer(res,timing);
            if "code" in res:
                if "message" in res:
                    self.write(json.dumps({"success":res["code"],"message":res["message"]}));
                elif "job_id" in res:
                    self.write(json.dumps({"success":res["code"],"id":res["job_id"]}));
                else:
                    self.write(json.dumps({"success":res["code"]}));
            else:
                self.write(json.dumps({"success":-1,"data":res}));
        
        if cmd == "restart":
            data = json.loads(self.request.body);
            job_id = data["id"];
            
            res = scheduler.start_job(job_id);
            self.write(json.dumps({"success":1}));
        
        if cmd == "stop":
            data = json.loads(self.request.body);
            job_id = data["id"];

            scheduler.stop_job(job_id);
            self.write(json.dumps({"success":1}));

        if cmd == "gets":
            data = self.request.body;
            data = json.loads(data);
            options = self.get_options(data);
            data = exector.find_some(options);
            self.write(json.dumps(data));
        
        if cmd == "del":
            data = json.loads(self.request.body);
            record_id = data["id"];
            res = exector.remove(record_id);
            self.write(json.dumps({"success":int(res['ok']),"count":res['n']}));

    def get_options(self,data):
        begin_time = data["begin_time"];
        end_time = data["end_time"];
        status = data["status"];

        options = {};
        if "id" in data and len(data["id"]) > 0:
            options["_id"] = data["id"];

        if "task_id" in data and len(data["task_id"]) > 0:
            options["task_id"] = data["task_id"];

        if "timer_id" in data and len(data["timer_id"]) > 0:
            options["timer_id"] = data["timer_id"];

        if "job_id" in data and len(data["job_id"]) > 0:
            options["job_id"] = data["job_id"];

        if (begin_time != "") and (end_time != ""):
            options["create_time"] = {
                "$gte":datetime.datetime.strptime(begin_time,"%Y-%m-%d %H:%M:%S"),
                "$lte":datetime.datetime.strptime(end_time,"%Y-%m-%d %H:%M:%S"),
            }

        if status != "":
            options["status"] = status;

        return options;
