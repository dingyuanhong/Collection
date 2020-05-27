
from Scheduler.Scheduler import TaskScheduler

def start_scheduler(**kwargs):
    scheduler = TaskScheduler(**kwargs);
    scheduler.start();
    scheduler.activate();
    return scheduler;