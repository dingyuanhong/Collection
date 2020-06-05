import requests
import json
import logging
from data.util import *

def getHeaders():
    headers = {
        # "Referer": "https://finance.sina.com.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        # "Host": "www.szse.cn",
    }
    return headers

def request_uri(uri,param):
    url = make_get_url(uri,param);
    headers = getHeaders();

    logging.info("request:"+url)
    res = requests.get(url,headers=headers);
    if res.status_code != 200:
        logging.error("request failed:"+str(res.status_code));
        raise Exception("请求失败:" + str(res.status_code));
    
    logging.info("request ok:" + str(res.status_code));
    return res.content.decode("GB18030");

# https://www.jianshu.com/p/fabe3811a01d

# 获取编码
# http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodes
def request_nodes():
    content = request_uri("http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodes",{})
    data = json.loads(content);
    return data

# 日线
# https://quotes.sina.cn/cn/api/jsonp.php/var%20_sh6882982020_5_29=/KC_MarketDataService.getKLineData?symbol=sh688298
# 数据格式:
# [{"d":"2020-02-05","o":"91.000","h":"152.000","l":"88.010","c":"145.980","v":"18847907","pv":"11350","pa":"1656873"}]
def request_kline_data(param):
    content = request_uri("https://quotes.sina.cn/cn/api/jsonp.php/a=/KC_MarketDataService.getKLineData",param)
    content = content[len("/*<script>location.href=\'//sina.com\';</script>*/\na=("):-2];
    data = json.loads(content);
    for it in data:
        it["symbol"] = param["symbol"]
        it["date"] = it["d"]
        it["open"] = it["o"]
        it["close"] = it["c"]
        it["high"] = it["h"]
        it["low"] = it["l"]
        it["volume"] = it["v"]

        # it["pa"] #盘后量
        # it["pv"] #盘后额
        del it["d"]
        del it["o"]
        del it["c"]
        del it["h"]
        del it["l"]
        del it["v"]
    return data

# 5分钟
# https://quotes.sina.cn/cn/api/jsonp_v2.php/var%20_sh688298_5_1590769539734=/CN_MarketDataService.getKLineData?symbol=sh688298&scale=5&ma=no&datalen=1023
# 数据格式
# [{"day":"2020-05-07 14:55:00","open":"87.400","high":"87.400","low":"87.080","close":"87.100","volume":"106334"}]
def request_minuts_data(param):
    content = request_uri("https://quotes.sina.cn/cn/api/jsonp_v2.php/a=/CN_MarketDataService.getKLineData",param)
    content = content[len("/*<script>location.href=\'//sina.com\';</script>*/\na=("):-2];
    data = json.loads(content);
    for it in data:
        it["symbol"] = param["symbol"]
    return data;

# 实时价
# https://hq.sinajs.cn/list=sh688298
def request_list_data(param):
    id_ = param["symbol"];
    content = request_uri("https://hq.sinajs.cn/list="+id_,{})
    content = content[len("var hq_str_"+id_+"=\""):-3];
    data = content.split(",")
    result = {};
    result["symbol"] = id_;
    result["name"] = data[0];
    result["open"] = data[1];   #今日开盘价
    result["close"] = data[2]; #昨日收盘价
    result["price"] = data[3];  #当前价格
    result["high"] = data[4];   #今日最高价
    result["low"] = data[5];    #今日最低价
    result["buy1"] = data[6];   # 买一 报价
    result["sell1"] = data[7];  # 卖一 报价
    result["volume"] = data[8]; #成交的股票数
    result["amount"] = data[9]; #成交金额
    result["buy"] = [
        [data[11],data[10]],   #“买一”报价 , #买一”申请4695股，即47手
        [data[13],data[12]],
        [data[15],data[14]],
        [data[17],data[16]],
        [data[19],data[18]],
    ]
    result["sell"] = [
        [data[21],data[20]],   #“卖一”报价 , #卖一”申请4695股，即47手
        [data[23],data[22]],
        [data[25],data[24]],
        [data[27],data[26]],
        [data[29],data[28]],
    ]
    result["date"] = data[30];
    result["time"] = data[31];

    return result;

# 逐笔行情
# https://vip.stock.finance.sina.com.cn/quotes_service/view/CN_TransListV2.php?num=11&symbol=sh688298&rn=26512833
# trade_item_list 逐笔详情
# trade_INVOL_OUTVOL 外盘 内盘
def request_translist_data(param):
    content = request_uri("https://vip.stock.finance.sina.com.cn/quotes_service/view/CN_TransListV2.php",param)
    # content = content[len("var hq_str_"+id_+"=\""):-2];
    return content;

# 股票列表
# 股票数
# http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeStockCount?node=sh_b
# 列表
# http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=2&num=40&sort=symbol&asc=1&node=sh_a&symbol=&_s_r_a=page
def request_stock_count_data(param):
    content = request_uri("http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeStockCount",param)
    return int(content[1:-1]);
def request_stock_list_data(param):
    content = request_uri("http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData",param)
    return json.loads(content);

# 英股
# http://quotes.sina.cn/hq/api/jsonp.php/IO.XSRV2.CallbackList['M2Q8x79da4XTQI3u']/LseService.lsePcHq?page=1&num=40&sort=-&asc=0&type=lse_all&_s_r_a=init
def request_lse_stock_list_data(param):
    content = request_uri("http://quotes.sina.cn/hq/api/jsonp.php/a/LseService.lsePcHq",param)
    return content;

# 美股列表
# http://stock.finance.sina.com.cn/usstock/api/jsonp.php/var%20category=/US_CategoryService.getCategory

# 美股
# http://stock.finance.sina.com.cn/usstock/api/jsonp.php/IO.XSRV2.CallbackList['wbtic6wRmcUjMInd']/US_CategoryService.getList?page=1&num=20&sort=&asc=0&market=&id=
def request_us_stock_list_data_count(param):
    content = request_uri("http://stock.finance.sina.com.cn/usstock/api/jsonp.php/a/US_CategoryService.getList",param)    
    lines = content.splitlines()
    content = lines[1][2:-2];
    data = json.loads(content);
    return int(data["count"]);

# 名称	代码	最新价	涨跌额	涨跌幅	振幅	昨收/今开盘	最高/最低价	成交量	市值(亿)	市盈率	行业板块	上市地
# 微软公司	MSFT	184.42	-0.49	-0.26%	0.83%	184.91/184.81	185.14/183.61	7,714,784	14,022.15	30.43	软件
# 'cname': '微软公司', 'preclose': '184.91', 'price': '184.42', 'market': 'NASDAQ', 'mktcap': '1402215087071', 
# 'pe': '30.43234322', 'chg': '-0.26', 'high': '185.14', 'diff': '-0.49', 'category': '软件', 
# 'amplitude': '0.83%', 'open': '184.81', 'symbol': 'MSFT', 'low': '183.61', 
# 'volume': '7714784', 'name': 'Microsoft Corp.', 'category_id': '14'
def request_us_stock_list_data(param):
    content = request_uri("http://stock.finance.sina.com.cn/usstock/api/jsonp.php/a/US_CategoryService.getList",param)    
    lines = content.splitlines()
    content = lines[1][2:-2];
    data = json.loads(content);
    return data["data"];

# 全球期货
# 数量
# http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getFuturesGlobalCount?node=global_qh
# 列表
# http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getFuturesGlobalData?page=1&num=40&sort=symbol&asc=1&node=global_qh&_s_r_a=init
def request_futures_global_list_data_count(param):
    content = request_uri("http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getFuturesGlobalCount",param)
    data = json.loads(content);
    return int(data);
def request_futures_global_list_data(param):
    content = request_uri("http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getFuturesGlobalData",param)
    data = json.loads(content);
    return data;

# 上证50期货
# 数量
# http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getNameCount?node=zzgz_qh
# 列表
# http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getNameList?page=1&num=40&sort=symbol&asc=1&node=zzgz_qh&_s_r_a=init
def request_financial_future_list_data_count(param):
    content = request_uri("http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getNameCount",param)
    data = json.loads(content);
    return int(data);

def request_financial_future_list_data(param):
    content = request_uri("http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getNameList",param)
    data = json.loads(content);
    for it in data:
        it["node"] = param["node"]
    return data;

# 期货
# 数量
# http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQFuturesCount?node=rzjb_qh
# 列表
# http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQFuturesData?page=1&num=40&sort=symbol&asc=1&node=rzjb_qh&_s_r_a=init

# 上海期货,大连期货,郑州期货
# http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQFuturesData?page=1&num=40&sort=symbol&asc=1&node=yy_qh&_s_r_a=init
def request_commodity_future_list_data_count(param):
    content = request_uri("http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQFuturesCount",param)
    data = json.loads(content);
    return int(data);
def request_commodity_future_list_data(param):
    content = request_uri("http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQFuturesData",param)
    data = json.loads(content);
    for it in data:
        it["node"] = param["node"]
    return data;

# 期货K线
# https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_MA20062020_5_30=/InnerFuturesNewService.getDailyKLine?symbol=MA2006&_=2020_5_30
# 'h': '1577.000', 'c': '1577.000', 'v': '130', 'l': '1550.000', 'd': '2020-06-03', 'o': '1550.000', 'p': '1030'
def request_future_kline_data(param):
    content = request_uri("https://stock2.finance.sina.com.cn/futures/api/jsonp.php/a/InnerFuturesNewService.getDailyKLine",param)
    lines = content.splitlines()
    content = lines[1][2:-2];
    data = json.loads(content);
    for it in data:
        it["symbol"] = param["symbol"]

        it["date"] = it["d"]
        it["open"] = it["o"]
        it["close"] = it["c"]
        it["high"] = it["h"]
        it["low"] = it["l"]
        it["volume"] = it["v"]

        # it["pa"] #盘后量
        # it["pv"] #盘后额
        del it["d"]
        del it["o"]
        del it["c"]
        del it["h"]
        del it["l"]
        del it["v"]
    return data;

# 期货分钟线
# https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_MA2006_5_1590776402780=/InnerFuturesNewService.getFewMinLine?symbol=MA2006&type=5
def request_future_minuts_data(param):
    content = request_uri("https://stock2.finance.sina.com.cn/futures/api/jsonp.php/a/InnerFuturesNewService.getFewMinLine",param)
    lines = content.splitlines()
    content = lines[1][2:-2];
    data = json.loads(content);
    for it in data:
        it["symbol"] = param["symbol"]

        it["date"] = it["d"]
        it["open"] = it["o"]
        it["close"] = it["c"]
        it["high"] = it["h"]
        it["low"] = it["l"]
        it["volume"] = it["v"]
        # it["p"] = it["p"]

        # it["p"] #持仓量
        del it["d"]
        del it["o"]
        del it["c"]
        del it["h"]
        del it["l"]
        del it["v"]
    return data;

#期货实时分时线
# https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20t1nf_MA2006=/InnerFuturesNewService.getMinLine?symbol=MA2006
def request_future_real_data(param):
    content = request_uri("https://stock2.finance.sina.com.cn/futures/api/jsonp.php/a/InnerFuturesNewService.getMinLine",param)
    lines = content.splitlines()
    content = lines[1][2:-2];
    data = json.loads(content);
    date = None;
    ret = [];
    for it in data:
        if date == None:
            date = it[6]
        item = {}
        item["symbol"] = param["symbol"]

        item["date"] = date
        item["time"] = it[0]
        item["price"] = it[1]
        item["average"] = it[2]
        item["volume"] = it[3]
        item["p"] = it[4]
        # it["p"] #持仓量
        ret.append(item)
    return ret;

# 期货5日线
# https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20t5nf_MA2006=/InnerFuturesNewService.getFourDaysLine?symbol=MA2006
def request_future_day_data(param):
    content = request_uri("https://stock2.finance.sina.com.cn/futures/api/jsonp.php/a/InnerFuturesNewService.getFourDaysLine",param)
    lines = content.splitlines()
    content = lines[1][2:-2];
    content = json.loads(content);

    ret = [];
    for data in content:
        date = None;
        for it in data:
            if date == None:
                date = it[6]
            item = {}
            item["symbol"] = param["symbol"]

            item["date"] = date
            item["time"] = it[0]
            item["price"] = it[1]
            item["average"] = it[2]
            item["volume"] = it[3]
            item["p"] = it[4]
            # it["p"] #持仓量
            ret.append(item)
    
    return ret;