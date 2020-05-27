from task import app
import json
import logging
from celery import chord,chain,group

import data.db as database

from .request import *

#arg : NAME 表名
#      PREFIX 表前缀
#      INDEX 主键,用于去重

@app.task(bind=True)
def output_data(self,data,arg):
    if data == None:
        logging.error("output_data: empty")
        logging.error(arg)
        logging.error(data)
        return;

    db = database.getDB(arg);
    if db == None:
        logging.error("db is empty")
        logging.error(arg)
        logging.error(data)
        return;
    index = None;
    if "INDEX" in arg:
        index = arg["INDEX"]
    db.append(data,index);

#数组结果解析
@app.task(bind=True)
def output_datas(self,data,arg):
    if data == None:
        logging.error("output_data: empty")
        logging.error(arg)
        logging.error(data)
        return;
    
    db = database.getDB(arg);
    if db == None:
        logging.error("db is empty")
        logging.error(arg)
        logging.error(data)
        return;

    index = None;
    if "INDEX" in arg:
        index = arg["INDEX"]
    for it in data:
        db.append(it,index);

#分时数据结果解析
@app.task(bind=True)
def stock_data_parse(self,data,arg):
    code = data["code"];
    picupdata = data["picupdata"];
    picdowndata = data["picdowndata"];

    item = ["date","open","close","high","low","delta","deltaPercent","volume","amount"]
    # 时间  开盘价 收盘价 最低价 最高价  涨跌   涨幅  成交量  成交额
    # ["2016-04-01","3.87","3.81","3.54","3.94","-0.09","-2.31",2185768,814907000.00]
    # ["2019-08-30", "2.85", "2.82", "2.55", "2.93", "-0.10", "-3.42", 1345154, 371411711]
    def make(it,item):
        ret = {}
        for i in range(len(item)):
            ret[item[i]] = it[i];
        ret["code"] = code;
        return ret;
    data = [make(it,item) for it in picupdata]
    output_datas.s(data,{**arg, **{"PREFIX":arg["PREFIX"] + "_stock"}}).apply_async();

    # 成交量
    item = ["date","volume","plusminus"]
    # 时间  成交量  涨 plus/跌 minus
    # ["2018-08-31", 7466581, "plus"]
    # ["2016-04-01",2185768,"minus"]
    data = [make(it,item) for it in picdowndata];
    output_datas.s(data,{**arg, **{"PREFIX":arg["PREFIX"] + "_volume"}}).apply_async();

@app.task(bind=True)
def stock_minuts_parse(self,data,arg):
    # code: "000659"
    # now: "1.88"
    # open: "1.93"
    # close: "1.91"
    # high: "1.93"
    # low: "1.88"
    # lastVolume: 1649
    # delta: "-0.03"   #涨跌
    # deltaPercent: "-1.57"  #涨幅
    # amount: 11195549       #成交额
    # marketTime: "2020-05-22 15:00:00"
    # name: "珠海中富"

    code = data["code"];
    marketTime = data["marketTime"];
    date = marketTime[:10]

    # ["09:30", 1.93]
    picavgprice = data["picavgprice"]; #最新价
    sellbuy5 = data["sellbuy5"]; #买卖五档

    picupdata = data["picupdata"]; 
    # ["09:30", 202, "plus"]
    picdowndata = data["picdowndata"]; 

    item = ["time","new","average","delta","deltaPercent","volume","amount"]
    # 时间  最新 均价  涨跌   涨幅  成交量  成交额
    # ["09:30", "1.93", "1.93", "0.02", "1.05", 202, 38986]
    def make(it,item):
        ret = {}
        for i in range(len(item)):
            ret[item[i]] = it[i];
        ret["code"] = code;
        ret["date"] = date;
        return ret;
    my_data = [make(it,item) for it in picupdata]
    output_datas.s(my_data,{**arg, **{"PREFIX":arg["PREFIX"] + "_stock"}}).apply_async();

    # 成交量
    item = ["time","volume","plusminus"]
    # 时间  成交量  涨 plus/跌 minus
    # ["2018-08-31", 7466581, "plus"]
    # ["2016-04-01",2185768,"minus"]
    my_data = [make(it,item) for it in picdowndata];
    output_datas.s(my_data,{**arg, **{"PREFIX":arg["PREFIX"] + "_volume"}}).apply_async();

    #保存数据
    # del data["sellbuy5"]
    del data["picavgprice"]
    del data["picupdata"]
    del data["picdowndata"]
    data["date"] = date;
    data["time"] = marketTime[11:];
    output_data.s(data, arg ).apply_async();

#获取公司数据
@app.task(bind=True)
def get_stock_list(self,context,param,arg):
    try:
        pagecount = request_stock_list_page_count(param)
        
        for i in range(1,pagecount+1):
            pageno = i;
            chain(
                get_stock_list_page_data.s(context,{**param,**{"PAGENO":pageno}}),
                output_datas.s(arg)
            ).apply_async();
        
        return None;
    except Exception as exc:
        raise self.retry(exc=exc,coutdown=10,max_retries=3)

#获取公司分页数据
@app.task(bind=True,rate_limit=10)
def get_stock_list_page_data(self,context,param):
    try:
        return request_stock_list(param)
    except Exception as exc:
        raise self.retry(exc=exc,coutdown=10,max_retries=3)

#获取公司信息
@app.task(bind=True,rate_limit=100)
def get_company(self,context,param):
    try:
        return request_company(param)
    except Exception as exc:
        raise self.retry(exc=exc,coutdown=10,max_retries=3)

#获取个股数据
@app.task(bind=True,rate_limit=10)
def get_stock_data(self,context,param):
    try:
        return request_stock_data(param)
    except Exception as exc:
        raise self.retry(exc=exc,coutdown=10,max_retries=3)

#获取分时数据
@app.task(bind=True,rate_limit=10)
def get_stock_minuts_data(self,context,param):
    try:
        return request_stock_minuts_data(param)
    except Exception as exc:
        raise self.retry(exc=exc,coutdown=10,max_retries=3)