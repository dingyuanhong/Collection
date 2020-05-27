from .base import NowDateTime,Base
from bson import ObjectId

class Week(Base):
    def __init__(self,db,prefix):
        super(Week, self).__init__(db,prefix + "_week")