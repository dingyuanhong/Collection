
from .base import NowDateTime,Base

class Task(Base):
    def __init__(self,db):
        super(Task, self).__init__(db,"task")