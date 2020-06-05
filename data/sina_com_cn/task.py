from task import app
import json
import logging
from celery import chord,chain,group

from data.task import *
from .request import *

#A股日K线
@app.task(bind=True,rate_limit=10)
def get_real_data(self,context,param):
    try:
        return request_list_data(param)
    except Exception as exc:
        raise self.retry(exc=exc,coutdown=10,max_retries=3)

#A股日K线
@app.task(bind=True,rate_limit=10)
def get_kline_data(self,context,param):
    try:
        return request_kline_data(param)
    except Exception as exc:
        raise self.retry(exc=exc,coutdown=10,max_retries=3)

#A股分钟数据
@app.task(bind=True,rate_limit=10)
def get_minuts_data(self,context,param):
    try:
        return request_minuts_data(param)
    except Exception as exc:
        raise self.retry(exc=exc,coutdown=10,max_retries=3)

#获取股票列表
@app.task(bind=True,rate_limit=10)
def get_stock_list(self,context,param,arg):
    try:
        count = request_stock_count_data(param)
        count = int(count)

        num = 40
        if "num" in param:
            num = int(param["num"]) if (int(param["num"]) > 0) else 40;
        param["num"] = num;
        pagecount = int(count / num ) + (1 if count%num > 0 else 0)

        for i in range(1,pagecount+1):
            pageno = i;
            chain(
                get_stock_list_data.s(context,{**param,**{"page":pageno}}),
                output_datas.s(arg)
            ).apply_async();
        
        return None;
    except Exception as exc:
        raise self.retry(exc=exc,coutdown=10,max_retries=3)

#获取A股单页
@app.task(bind=True,rate_limit=10)
def get_stock_list_data(self,context,param):
    try:
        return request_stock_list_data(param)
    except Exception as exc:
        raise self.retry(exc=exc,coutdown=10,max_retries=3)

#获取美股票列表
@app.task(bind=True,rate_limit=10)
def get_us_stock_list(self,context,param,arg):
    try:
        count = request_us_stock_list_data_count(param)
        count = int(count);

        num = 20
        if "num" in param:
            num = int(param["num"]) if (int(param["num"]) > 0) else 20;
        param["num"] = num;
        pagecount = int(count / num ) + (1 if count%num > 0 else 0)

        for i in range(1,pagecount+1):
            pageno = i;
            chain(
                get_us_stock_list_data.s(context,{**param,**{"page":pageno}}),
                output_datas.s(arg)
            ).apply_async();
        
        return None;
    except Exception as exc:
        raise self.retry(exc=exc,coutdown=10,max_retries=3)

@app.task(bind=True,rate_limit=10)
def get_us_stock_list_data(self,context,param):
    try:
        return request_us_stock_list_data(param)
    except Exception as exc:
        raise self.retry(exc=exc,coutdown=10,max_retries=3)

#获取美全球期货列表
@app.task(bind=True,rate_limit=10)
def get_futures_global_list(self,context,param,arg):
    try:
        count = request_futures_global_list_data_count(param)
        count = int(count);

        num = 40
        if "num" in param:
            num = int(param["num"]) if (int(param["num"]) > 0) else 40;
        param["num"] = num;
        pagecount = int(count / num ) + (1 if count%num > 0 else 0)

        for i in range(1,pagecount+1):
            pageno = i;
            chain(
                get_futures_global_list_data.s(context,{**param,**{"page":pageno}}),
                output_datas.s(arg)
            ).apply_async();
        
        return None;
    except Exception as exc:
        raise self.retry(exc=exc,coutdown=10,max_retries=3)

@app.task(bind=True,rate_limit=10)
def get_futures_global_list_data(self,context,param):
    try:
        return request_futures_global_list_data(param)
    except Exception as exc:
        raise self.retry(exc=exc,coutdown=10,max_retries=3)

# 上证期货
@app.task(bind=True,rate_limit=10)
def get_financial_future_list(self,context,param,arg):
    try:
        count = request_financial_future_list_data_count(param)
        count = int(count);

        num = 40
        if "num" in param:
            num = int(param["num"]) if (int(param["num"]) > 0) else 40;
        param["num"] = num;
        pagecount = int(count / num ) + (1 if count%num > 0 else 0)

        for i in range(1,pagecount+1):
            pageno = i;
            chain(
                get_financial_future_list_data.s(context,{**param,**{"page":pageno}}),
                output_datas.s(arg)
            ).apply_async();
        
        return None;
    except Exception as exc:
        raise self.retry(exc=exc,coutdown=10,max_retries=3)

@app.task(bind=True,rate_limit=10)
def get_financial_future_list_data(self,context,param):
    try:
        return request_financial_future_list_data(param)
    except Exception as exc:
        raise self.retry(exc=exc,coutdown=10,max_retries=3)

# 上海期货,大连期货,郑州期货
@app.task(bind=True,rate_limit=10)
def get_commodity_future_list(self,context,param,arg):
    try:
        count = request_commodity_future_list_data_count(param)
        count = int(count);

        num = 40
        if "num" in param:
            num = int(param["num"]) if (int(param["num"]) > 0) else 40;
        param["num"] = num;
        pagecount = int(count / num ) + (1 if count%num > 0 else 0)

        for i in range(1,pagecount+1):
            pageno = i;
            chain(
                get_commodity_future_list_data.s(context,{**param,**{"page":pageno}}),
                output_datas.s(arg)
            ).apply_async();
        
        return None;
    except Exception as exc:
        raise self.retry(exc=exc,coutdown=10,max_retries=3)

@app.task(bind=True,rate_limit=10)
def get_commodity_future_list_data(self,context,param):
    try:
        return request_commodity_future_list_data(param)
    except Exception as exc:
        raise self.retry(exc=exc,coutdown=10,max_retries=3)

# 期货K线
@app.task(bind=True,rate_limit=10)
def get_future_kline_data(self,context,param):
    try:
        return request_future_kline_data(param)
    except Exception as exc:
        raise self.retry(exc=exc,coutdown=10,max_retries=3)

# 期货分钟线
@app.task(bind=True,rate_limit=10)
def get_future_minuts_data(self,context,param):
    try:
        return request_future_minuts_data(param)
    except Exception as exc:
        raise self.retry(exc=exc,coutdown=10,max_retries=3)

# 期货实时分时线
@app.task(bind=True,rate_limit=10)
def get_future_real_data(self,context,param):
    try:
        return request_future_real_data(param)
    except Exception as exc:
        raise self.retry(exc=exc,coutdown=10,max_retries=3)

# 期货日线
@app.task(bind=True,rate_limit=10)
def get_future_day_data(self,context,param):
    try:
        return request_future_day_data(param)
    except Exception as exc:
        raise self.retry(exc=exc,coutdown=10,max_retries=3)