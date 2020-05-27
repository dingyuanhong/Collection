from .base import NowDateTime,Base
from bson import ObjectId

class Minute(Base):
    def __init__(self,db,prefix):
        super(Minute, self).__init__(db,prefix + "_minute")