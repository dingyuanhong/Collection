REM celery worker -A  task.celery_app -l debug -E -P eventlet
celery worker -A  task.celery_app -l error -E -P eventlet