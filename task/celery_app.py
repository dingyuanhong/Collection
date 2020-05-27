import celery
import time

from importlib import import_module, reload

#https://segmentfault.com/a/1190000010112848
def import_string(import_name):
    import_name = str(import_name).replace(':', '.')
    modules = import_name.split('.')
    mod = import_module(modules[0])
    for comp in modules[1:]:
        if not hasattr(mod, comp):
            reload(mod)
        mod = getattr(mod, comp)
    return mod


app = celery.Celery('tasks',broker='amqp://admin:admin@10.0.0.116:5672/my_vhost',backend='amqp://admin:admin@10.0.0.116:5672/my_vhost')
# app=celery.Celery('test')
app.config_from_object("config")
app.conf.CELERY_IMPORTS = ['task.task', 'task.task.all_task']

#执行方法
@app.task
def execute(func, *args, **kwargs):
    func = import_string(func)
    return func(*args, **kwargs)

#定时重复调用
@app.task
def interval(func, seconds, args=(), task_id=None):
    next_run_time = current_time() + timedelta(seconds=seconds)
    kwargs = dict(args=(func, seconds, args), eta=next_run_time)
    if task_id is not None:
        kwargs.update(task_id=task_id)
    interval.apply_async(**kwargs)
    func = import_string(func)
    return func(*args)


def main():
    app.start()

if __name__ == '__main__':
    main();