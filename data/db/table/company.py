from .base import NowDateTime,Base
from bson import ObjectId

class Company(Base):
    def __init__(self,db,prefix):
        super(Company, self).__init__(db,prefix + "_company")