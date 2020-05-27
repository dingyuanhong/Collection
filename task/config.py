
from kombu import Exchange,Queue
 

# BROKER_URL = "redis://:your_password@127.0.0.1:6379/1" 
# CELERY_RESULT_BACKEND = "redis://:your_password@127.0.0.1:6379/1"

# BROKER_URL='redis://10.30.40.12:6379/1'
# CELERY_RESULT_BACKEND='redis://10.30.40.12:6379/2'

CELERY_RESULT_BACKEND="amqp://admin:admin@10.0.0.116:5672/my_vhost"
BROKER_URL="amqp://admin:admin@10.0.0.116:5672/my_vhost"

# CELERY_QUEUES = (
# Queue("default",Exchange("default"),routing_key="default"),
# Queue("for_task_A",Exchange("for_task_A"),routing_key="for_task_A"),
# Queue("for_task_B",Exchange("for_task_B"),routing_key="for_task_B") 
# )
# # 路由
# CELERY_ROUTES = {
# 'tasks.taskA':{"queue":"for_task_A","routing_key":"for_task_A"},
# 'tasks.taskB':{"queue":"for_task_B","routing_key":"for_task_B"}
# }
# CELERY_DEFAULT_QUEUE = 'default'   # 设置默认的路由
# CELERY_DEFAULT_EXCHANGE = 'default'
# CELERY_DEFAULT_ROUTING_KEY = 'default'
 
# CELERY_TASK_RESULT_EXPIRES = 10  # 设置存储的过期时间　防止占用内存过多

#并发的worker数量
CELERYD_CONCURRENCY = 4
# r每次去取任务的数量 默认值就是4
# CELERYD_PREFETCH_MULTIPLIER = 4

# 每个worker执行了多少任务就会死掉，默认是无限的
CELERYD_MAX_TASKS_PER_CHILD = 40