from task import app
import json
import logging
import time
from celery import chord,chain,group

from data.task import *
from .Xueqiu_Excetor import Xueqiu_Excetor

@app.task(bind=True,rate_limit=10)
def get_stock_data(self,func,param):
    try:
        return Xueqiu_Excetor.Do(func,**param)
    except Exception as exc:
        raise self.retry(exc=exc,coutdown=10,max_retries=3)

@app.task(bind=True)
def get_stock_info(self,func,param):
    try:
        arg = {"NAME":"day","PREFIX":"sina_future" ,"INDEX":["symbol"] }

        chain(
            get_stock_data.s(func,param),
            output_datas.s(arg)
        ).apply_async();
    except Exception as exc:
        raise self.retry(exc=exc,coutdown=10,max_retries=3)

@app.task(bind=True)
def get_stock_list(self,context,param):
    try:
        count = get_stock_data.s("stocks_list_count",param)
        count = count.apply_async().get()
        count = int(count)

        num = 90
        if "num" in param:
            num = int(param["num"]) if (int(param["num"]) > 0) else 90;
        param["num"] = num;
        pagecount = int(count / num ) + (1 if count%num > 0 else 0)

        arg = {"NAME":"stock","PREFIX":"xueqiu" ,"INDEX":["symbol"] }

        for i in range(1,pagecount+1):
            pageno = i;
            chain(
                get_stock_data.s("stocks_list",{**param,**{"page":pageno}}),
                output_datas.s(arg)
            ).apply_async();
            break;
        
        return None;
    except Exception as exc:
        raise self.retry(exc=exc,coutdown=10,max_retries=3)

@app.task(bind=True)
def parse_kline(self,data,param):
    data = json.loads(data)

    column = data["data"]["column"];
    items = data["data"]["item"];
    symbol =  data["data"]["symbol"];

    result = [];
    for it in items:
        line = {};
        for i in range(0,len(column)):
            line[column[i]] = it[i];
        line["symbol"] = symbol;
        local = time.localtime(int(line["timestamp"])/1000)
        line["date"] = time.strftime("%Y-%m-%d %H:%M:%S", local)

        result.append(line)
    return result;

@app.task(bind=True)
def parse_minute(self,data,param):
    data = json.loads(data)

    items = data["data"]["items"];
    symbol =  param["symbol"];

    result = [];
    for it in items:
        line = it;
        line["symbol"] = symbol;
        local = time.localtime(int(line["timestamp"])/1000)
        line["date"] = time.strftime("%Y-%m-%d %H:%M:%S", local)

        result.append(line)
    return result;

def parse_compinfo(data,param):
    pass

@app.task
def parse_cash_flow(data,param):
    data = json.loads(data)
    items = data["data"]["list"];
    symbol =  param["symbol"];

    result = [];
    for it in items:
        line = it;
        line["symbol"] = symbol;
        local = time.localtime(int(line["report_date"])/1000)
        line["date"] = time.strftime("%Y-%m-%d %H:%M:%S", local)

        result.append(line)
    return result;