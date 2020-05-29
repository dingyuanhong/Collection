import datetime
import time
import traceback
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.events import EVENT_JOB_MAX_INSTANCES,EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, EVENT_JOB_MISSED
import apscheduler.events
import copy

def props(obj):
    pr = {}
    for name in dir(obj):
        value = getattr(obj, name)
        if not name.startswith('__') and not callable(value) and not name.startswith('_'):
            pr[name] = value
    return pr

import logging
logging.debug(props(apscheduler.events))

def SchedulerStatusListener(context):
    def listener(event):
        context.onStatusChange(event);
    return listener;

def CreateScheduler(context,client):
    jobstores = {
        'mongo': MongoDBJobStore(collection='job', database='scheduler', client=client),
        'default': MemoryJobStore(),
    }
    executors = {
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(5),
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 3,
        'misfire_grace_time':10,
    }
    scheduler = BackgroundScheduler(
        jobstores=jobstores,
        executors=executors,
        job_defaults=job_defaults,
    )
    scheduler.add_listener(SchedulerStatusListener(context), EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    return scheduler;

from db.table.task import Task
from db.table.job import Job
from db.table.timer import Timer
from db.table.exector import Exector

import actuator.exector as Actuator

#https://www.cnblogs.com/ohyb/p/9084011.html
#https://www.cnblogs.com/ohyb/p/9084011.html

def SchedulerExector(context):
    def Exec():
        try:
            res = Actuator.Exec(context,context['task']);
            context["scheduler"].onExectorResult(context,"complete",str(res));
        except Exception as ex:
            logging.error(traceback.format_exc());
            context["scheduler"].onExectorResult(context,"failed","exec.exception."+str(ex));
    return Exec;

def SchedulerJobExector(context):    
    def Exec():
        exector = Exector(context["db"])
        job_id = exector.insert({
            "task_id":context["task"]["id"],
            "task":context["task"],
            "timer_id":context["timer_id"],
            "timer":context["timer"],
            "job_id":context["job_id"],
        });
        if job_id == None:
            context["scheduler"].onJobResult(context,"failed","db insert error");
            return;
        
        context["scheduler"].onJobResult(context,"success","");

        newCxt = copy.copy(context);
        newCxt["exector_id"] = job_id;
        SchedulerExector(newCxt)();
        pass
    return Exec;

class TaskScheduler:
    def __init__(self,**kwargs):
        print("Scheduler 参数:",kwargs);

        self.db = kwargs["db"];
        self.scheduler = CreateScheduler(self,self.db.Client());

    def start(self):
        self.scheduler.start();

    def activate(self):
        job = Job(self.db);
        job_ids = job.find_by_status("active");
        for i in range(len(job_ids)):
            self.start_job(job_ids[i]);

    def Exec(self,task):
        exector = Exector(self.db);
        job_id = exector.insert({
            "task_id":task["id"],
            "task":task
        })
        if job_id == None:
            return {"code":0,"message":"任务执行失败"};

        self.scheduler.add_job(func=SchedulerExector({
            "scheduler":self,
            "task":task,
            "exector_id":job_id,
        }),id="exector."+job_id);
        
        return {"code":1,"job_id":job_id};

    def ExecByTimer(self,task,timer):
        if timer["type"] == "once":
            return self.Exec(task);

        job = Job(self.db);
        job_id = job.insert({
            "task_id":task["id"],
            "task":task,
            "timer_id":timer["id"],
            "timer":timer,
        });

        if job_id == None:
            return {"code":0,"message":"任务存储失败"};

        ret = self.scheduler.add_job(func=SchedulerJobExector({
            "scheduler":self,
            "task":task,
            "timer":timer,
            "job_id":job_id,
        }),trigger=timer["type"],
        id="job."+job_id,**timer["param"],
        misfire_grace_time=3600,coalesce=True);

        return {"code":1,"job_id":job_id};

    def start_job(self,job_id):
        job = Job(self.db);

        job_class = job.find(job_id);
        if(job_class == None):
            return None;
        
        task_class = job_class["task"];
        if(task_class == None):
            return None;

        timer_class = job_class["timer"];
        if(timer_class == None):
            return None;

        job_id = job_class["id"];
        job.update_status(job_id,"active");

        self.scheduler.add_job(func=SchedulerJobExector({
            "scheduler":self,
            "task":task_class,
            "timer":timer_class,
            "job_id":job_id,
        }),trigger=timer_class["type"],
        id="job."+job_id,**timer_class["param"],
        misfire_grace_time=3600,coalesce=True);

        return True;

    def stop_job(self,job_id):
        job = Job(self.db);
        job.update_status(job_id,"stop");
        try:
            self.scheduler.remove_job("job."+job_id);
        except:
            pass;

    def onStatusChange(self,event):
        job_id = event.job_id;
        if(job_id.find("job.") >= 0):
            job = Job(self.db);
            job_id = job_id[4:];
            if event.exception:
                logging.error(str(event)+str(event.exception))
                self.onJobResult({"job_id":job_id},"exception",str(event.exception));
            elif EVENT_JOB_EXECUTED == event.code:
                self.onJobResult({"job_id":job_id},"success","");
            else:
                logging.debug(event)
                self.onJobResult({"job_id":job_id},"complete","event.code." + str(event.code));
        else:
            exector = Exector(self.db);
            job_id = job_id[8:];
            if event.exception:
                logging.error(str(event)+str(event.exception))
                self.onExectorResult({"exector_id":job_id},"exception",str(event.exception));
            elif EVENT_JOB_EXECUTED == event.code:
                self.onExectorResult({"exector_id":job_id},"success","");
            else:
                logging.debug(event)
                self.onExectorResult({"exector_id":job_id},"complete","event.code." + str(event.code));

    def onJobResult(self,content,status,message):
        job = Job(self.db);
        job_id = content["job_id"];
        if status == "success":
            result = {
                "status":status,
            };
        else:
            result = {
                "status":status,
                "message":message,
            };
        job.set_result(job_id,result);
        loop = False;
        if("timer" in content):
            loop = True
        if not loop:
            job.update_status(job_id,"complete");

    def onExectorResult(self,content,status,message):
        exector = Exector(self.db);
        job_id = content["exector_id"];
        if status == "success":
            result = {
                "status":status,
            };
        else:
            result = {
                "status":status,
                "message":message,
            };
        exector.set_result(job_id,result);
        exector.update_status(job_id,"complete");