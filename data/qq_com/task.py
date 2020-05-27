from task import app

@app.task(bind=True)
def ExceterTask(self,context,task):
    pass

