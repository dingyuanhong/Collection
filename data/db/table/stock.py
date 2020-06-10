from .base import NowDateTime,Base
from bson import ObjectId

class Stock(Base):
    def __init__(self,db,prefix):
        super(Stock, self).__init__(db,prefix + "_stock")

    def get_szse_stock_ids(self):
        data = self.collection().find({},{"zqdm":1,"_id":0});
        lst = []
        for it in data:
            lst.append(it["zqdm"]);
        return lst;

    def get_sina_stock_ids(self):
        data = self.collection().find({},{"symbol":1,"_id":0});
        lst = []
        for it in data:
            lst.append(it["symbol"]);
        return lst;