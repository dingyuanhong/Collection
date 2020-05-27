from .base import NowDateTime,Base
from bson import ObjectId

class Day(Base):
    def __init__(self,db,prefix):
        super(Day, self).__init__(db,prefix + "_day")