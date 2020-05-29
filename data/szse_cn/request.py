import requests
import json
import logging
from data.util import *

def add_random_value(url):
    url += "&random=0.7881663624839406";
    return url

def getHeaders():
    headers = {
        "Referer": "http://www.szse.cn/market/companys/company/index.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        "Host": "www.szse.cn",
    }
    return headers

def request_url(uri,param):
    url = make_get_url(uri,param);
    url = add_random_value(url)
    headers = getHeaders();

    logging.info("request:"+url)
    res = requests.get(url,headers=headers);
    if res.status_code != 200:
        logging.error("request failed:"+str(res.status_code));
        raise Exception("请求失败:" + str(res.status_code));
    
    logging.info("request ok:" + str(res.status_code));

    return res.content.decode("utf-8");

# 公司列表
# http://www.szse.cn/api/report/ShowReport/data?
# SHOWTYPE=JSON&CATALOGID=1110x&TABKEY=tab1&PAGENO=13&random=0.7881663624839406
def request_stock_list_page_count(param):
    content = request_url("http://www.szse.cn/api/report/ShowReport/data",param)
    data = json.loads(content)
    pagecount = data[0]["metadata"]["pagecount"];
    return pagecount;

def request_stock_list(param):
    content = request_url("http://www.szse.cn/api/report/ShowReport/data",param)
    data = json.loads(content)
    data = data[0]["data"]
    return data;

# 结果字段:
# agdm: "A股代码"
# agjc: "A股简称"
# agltgb: "A股流通股本"
# agssrq: "A股上市日期"
# agzgb: "A股总股本"
# bgdm: "B股代码"
# bgjc: "B股简称"
# bgltgb: "B股流通股本"
# bgssrq: "B股上市日期"
# bgzgb: "B股总股本"
# dldq: "地区"
# gsqc: "公司全称"
# http: "公司网址"
# sheng: "省份"
# shi: "城市"
# sshymc: "所属行业"
# ywqc: "英文全称"
# zcdz: "注册地址"

# 公司信息
# http://www.szse.cn/api/report/index/companyGeneralization?random=0.6825774567012031&secCode=000001
def request_company(param):
    content = request_url("http://www.szse.cn/api/report/index/companyGeneralization",param)
    data = json.loads(content)
    if data["code"] == "0":
        data = data["data"]
        return data;
    return None;

#个股数据
# 日线
# http://www.szse.cn/api/market/ssjjhq/getHistoryData?random=0.13528516955205339&cycleType=32&marketId=1&code=000659
# 周
# http://www.szse.cn/api/market/ssjjhq/getHistoryData?random=0.1740269684505269&cycleType=33&marketId=1&code=000659
# 月
# http://www.szse.cn/api/market/ssjjhq/getHistoryData?random=0.9191935433749283&cycleType=34&marketId=1&code=000659
def request_stock_data(param):
    # cycleType=33&marketId=1&code=000659
    content = request_url("http://www.szse.cn/api/market/ssjjhq/getHistoryData",param)
    data = json.loads(content)
    if data["code"] == "0":
        data = data["data"]
        return data;
    return None;

# 分时线
# http://www.szse.cn/api/market/ssjjhq/getTimeData?random=0.5403685466504138&marketId=1&code=000659
def request_stock_minuts_data(param):
    # marketId=1&code=000659
    content = request_url("http://www.szse.cn/api/market/ssjjhq/getTimeData",param)
    data = json.loads(content)
    if data["code"] == "0":
        data = data["data"]
        return data;
    return None;
