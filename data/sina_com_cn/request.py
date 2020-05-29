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
    return res.content.decode("utf-8");

# https://www.jianshu.com/p/fabe3811a01d

# 获取编码
# http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodes
def request_nodes():
    content = request_uri("http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodes",{})
    return content;

# 日线
# https://quotes.sina.cn/cn/api/jsonp.php/var%20_sh6882982020_5_29=/KC_MarketDataService.getKLineData?symbol=sh688298
# 数据格式:
# [{"d":"2020-02-05","o":"91.000","h":"152.000","l":"88.010","c":"145.980","v":"18847907","pv":"11350","pa":"1656873"}]
def request_kline_data(param):
    content = request_uri("https://quotes.sina.cn/cn/api/jsonp.php/a=/KC_MarketDataService.getKLineData",param)
    content = content[len("/*<script>location.href=\'//sina.com\';</script>*/\na=("):-2];
    return content;

# 5分钟
# https://quotes.sina.cn/cn/api/jsonp_v2.php/var%20_sh688298_5_1590769539734=/CN_MarketDataService.getKLineData?symbol=sh688298&scale=5&ma=no&datalen=1023
# 数据格式
# [{"day":"2020-05-07 14:55:00","open":"87.400","high":"87.400","low":"87.080","close":"87.100","volume":"106334"}]
def request_minuts_data(param):
    content = request_uri("https://quotes.sina.cn/cn/api/jsonp_v2.php/a=/CN_MarketDataService.getKLineData",param)
    content = content[len("/*<script>location.href=\'//sina.com\';</script>*/\na=("):-2];
    return content;

# 实时价
# https://hq.sinajs.cn/list=sh688298
def request_list_data(param):
    id_ = param["id"];
    content = request_uri("https://hq.sinajs.cn/list="+id,{})
    content = content[len("var hq_str_"+id_+"=\""):-2];
    return content;

# 逐笔行情
# https://vip.stock.finance.sina.com.cn/quotes_service/view/CN_TransListV2.php?num=11&symbol=sh688298&rn=26512833
# trade_item_list 逐笔详情
# trade_INVOL_OUTVOL 外盘 内盘
def request_translist_data(param):
    content = request_uri("https://vip.stock.finance.sina.com.cn/quotes_service/view/CN_TransListV2.php",param)
    # content = content[len("var hq_str_"+id_+"=\""):-2];
    return content;

# 股票数
# http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeStockCount?node=sh_b
def request_stock_count_data(param):
    content = request_uri("http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeStockCount",param)
    return content;

# 股票列表
# http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=2&num=40&sort=symbol&asc=1&node=sh_a&symbol=&_s_r_a=page
def request_stock_list_data(param):
    content = request_uri("http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData",param)
    return content;


# 英股
# http://quotes.sina.cn/hq/api/jsonp.php/IO.XSRV2.CallbackList['M2Q8x79da4XTQI3u']/LseService.lsePcHq?page=1&num=40&sort=-&asc=0&type=lse_all&_s_r_a=init
def request_lse_stock_list_data(param):
    content = request_uri("http://quotes.sina.cn/hq/api/jsonp.php/a/LseService.lsePcHq",param)
    return content;

# 美股
# http://stock.finance.sina.com.cn/usstock/api/jsonp.php/IO.XSRV2.CallbackList['wbtic6wRmcUjMInd']/US_CategoryService.getList?page=1&num=20&sort=&asc=0&market=&id=
def request_us_stock_list_data(param):
    content = request_uri("http://stock.finance.sina.com.cn/usstock/api/jsonp.php/a/US_CategoryService.getList",param)
    return content;

# 全球期货
# http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getFuturesGlobalData?page=1&num=40&sort=symbol&asc=1&node=global_qh&_s_r_a=init
def request_futures_list_data(param):
    content = request_uri("http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getFuturesGlobalData",param)
    return content;

# 上证50期货交易所
# http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getNameList?page=1&num=40&sort=symbol&asc=1&node=zzgz_qh&_s_r_a=init
def request_future_list_data(param):
    content = request_uri("http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getNameList",param)
    return content;

# 上海期货
# http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQFuturesData?page=1&num=40&sort=symbol&asc=1&node=yy_qh&_s_r_a=init
def request_future2_list_data(param):
    content = request_uri("http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQFuturesData",param)
    return content;

# 期货K线
# https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_MA20062020_5_30=/InnerFuturesNewService.getDailyKLine?symbol=MA2006&_=2020_5_30
def request_future_kline_data(param):
    content = request_uri("https://stock2.finance.sina.com.cn/futures/api/jsonp.php/a/InnerFuturesNewService.getDailyKLine",param)
    return content;

# 期货分钟线
# https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_MA2006_5_1590776402780=/InnerFuturesNewService.getFewMinLine?symbol=MA2006&type=5
def request_future_minuts_data(param):
    content = request_uri("https://stock2.finance.sina.com.cn/futures/api/jsonp.php/a/InnerFuturesNewService.getFewMinLine",param)
    return content;

# 期货5日线
# https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20t1nf_MA2006=/InnerFuturesNewService.getMinLine?symbol=MA2006
def request_future_day_data(param):
    content = request_uri("https://stock2.finance.sina.com.cn/futures/api/jsonp.php/a/InnerFuturesNewService.getMinLine",param)
    return content;