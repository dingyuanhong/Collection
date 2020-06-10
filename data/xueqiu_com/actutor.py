from actuator.register import fm; 
from .task import *
import data.db as database
import json
import copy

class self_handlers:
    handlers = {};
    def route(self,func):
        def registe(cls):
            self.handlers[func] = cls;
            return cls;
        return registe;

this = self_handlers()

@fm.route("xueqiu.com","stock_run")
@this.route("stock_run")
def stock_run(context,task):
    function = task["function"]
    host = this.handlers[function]
    host(context,task);

@fm.route("xueqiu.com","stocks_all")
@this.route("stocks_all")
def stocks_all(context,task):
    db = database.getDB({"NAME":"stock","PREFIX":"xueqiu"});
    codes = db.get_stock_symbol()

    param = task["param"]
    task["function"] = param["subfunction"]
    del param["subfunction"];
    if not task["function"]:
        raise Exception("未知的方法")
    if len(task["function"]) == 0 :
        raise Exception("未定义的方法")

    for code in codes :
        param["symbol"] = code;
        stock_run(context,copy.deepcopy(task))

@fm.route("xueqiu.com","stock_list")
@this.route("stock_list")
def stock_list(context,task):
    param = task["param"]
    task = get_stock_list.s(None,param, {"NAME":"stock","PREFIX":"xueqiu" ,"INDEX":["symbol"] })
    task.apply_async()

@fm.route("xueqiu.com","kline_data")
@this.route("kline_data")
def kline_data(context,task):
    param = task["param"]

    task = chain( 
        get_stock_data.s("kline",param),
        parse_kline.s(param),
        output_datas.s({"NAME":"day","PREFIX":"xueqiu" ,"INDEX":["symbol","date"] }) 
    )
    task.apply_async()

@fm.route("xueqiu.com","minute_data")
@this.route("minute_data")
def minute_data(context,task):
    param = task["param"]

    task = chain( 
        get_stock_data.s("minute",param),
        parse_minute.s(param),
        output_datas.s({"NAME":"minus","PREFIX":"xueqiu_" + param["period"] ,"INDEX":["symbol","date"] }) 
    )
    task.apply_async()

@fm.route("xueqiu.com","compinfo_data")
def compinfo_data(context,task):
    param = task["param"]
    task = get_stock_data.s("compinfo",param)
    data = task.apply_async().get()
    print(type(data))
    data = parse_compinfo(data,param)
    print(data)

    # task = chain( 
    #     get_stock_data.s("kline",param), 
    #     output_datas.s({"NAME":"day","PREFIX":"xueqiu" ,"INDEX":["symbol","date"] }) 
    # ) 
    # task.apply_async() 

@fm.route("xueqiu.com","cash_flow_data")
@this.route("cash_flow_data")
def cash_flow_data(context,task):
    param = task["param"]

    task = chain( 
        get_stock_data.s("cash_flow",param),
        parse_cash_flow.s(param),
        output_datas.s({"NAME":"company","PREFIX":"xueqiu_cash_flow" ,"INDEX":["symbol","date","report_name"] }) 
    )
    task.apply_async()

@fm.route("xueqiu.com","balance_data")
@this.route("balance_data")
def balance_data(context,task):
    param = task["param"]

    task = chain( 
        get_stock_data.s("balance",param),
        parse_cash_flow.s(param),
        output_datas.s({"NAME":"company","PREFIX":"xueqiu_balance" ,"INDEX":["symbol","date","report_name"] }) 
    )
    task.apply_async()

@fm.route("xueqiu.com","income_data")
@this.route("income_data")
def income_data(context,task):
    param = task["param"]

    task = chain( 
        get_stock_data.s("income",param),
        parse_cash_flow.s(param),
        output_datas.s({"NAME":"company","PREFIX":"xueqiu_income" ,"INDEX":["symbol","date","report_name"] }) 
    )
    task.apply_async()