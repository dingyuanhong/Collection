from .base import NowDateTime,Base
from bson import ObjectId

class Month(Base):
    def __init__(self,db,prefix):
        super(Month, self).__init__(db,prefix + "_month")