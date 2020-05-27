
from .base import NowDateTime,Base

class Timer(Base):
    def __init__(self,db):
        super(Timer, self).__init__(db,"timer")
