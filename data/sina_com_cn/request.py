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

# 地址:
# https://quotes.sina.cn/cn/api/jsonp.php/var%20_sh6882982020_5_29=/KC_MarketDataService.getKLineData?symbol=sh688298
# 数据格式:
# [{"d":"2020-02-05","o":"91.000","h":"152.000","l":"88.010","c":"145.980","v":"18847907","pv":"11350","pa":"1656873"}]
def request_kline_data(param):
    content = request_uri("https://quotes.sina.cn/cn/api/jsonp.php/a=/KC_MarketDataService.getKLineData",param)
    content = content[len("/*<script>location.href=\'//sina.com\';</script>*/\na=("):-2];
    return content;