from .base import NowDateTime,Base
from bson import ObjectId

# "code" 代码
# "date" 时间
# "open" 开盘
# "close" 收盘
# "high" 高
# "low" 低
# "delta" 涨跌
# "deltaPercent" 涨跌幅
# "volume" 成交量
# "amount" 成交额

class Day(Base):
    def __init__(self,db,prefix):
        super(Day, self).__init__(db,prefix + "_day")