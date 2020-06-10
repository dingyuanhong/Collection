from actuator.register import fm; 
from .task import *
import json

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

@fm.route("xueqiu.com","*")
def stock_info(context,task):
    param = task["param"]
    func = task["function"]
    task = get_stock_info.s(None,func,param)
    task.apply_async();

@fm.route("xueqiu.com","stock_list")
def stock_list(context,task):
    param = task["param"]
    task = get_stock_list.s(None,param)
    task.apply_async()

@fm.route("xueqiu.com","kline_data")
def kline_data(context,task):
    param = task["param"]

    task = chain( 
        get_stock_data.s("kline",param),
        parse_kline.s(param),
        output_datas.s({"NAME":"day","PREFIX":"xueqiu" ,"INDEX":["symbol","date"] }) 
    )
    task.apply_async()

@fm.route("xueqiu.com","minute_data")
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
def cash_flow_data(context,task):
    param = task["param"]

    task = chain( 
        get_stock_data.s("cash_flow",param),
        parse_cash_flow.s(param),
        output_datas.s({"NAME":"company","PREFIX":"xueqiu_cash_flow" ,"INDEX":["symbol","date","report_name"] }) 
    )
    task.apply_async()

@fm.route("xueqiu.com","balance_data")
def balance_data(context,task):
    param = task["param"]

    task = chain( 
        get_stock_data.s("balance",param),
        parse_cash_flow.s(param),
        output_datas.s({"NAME":"company","PREFIX":"xueqiu_balance" ,"INDEX":["symbol","date","report_name"] }) 
    )
    task.apply_async()

@fm.route("xueqiu.com","income_data")
def income_data(context,task):
    param = task["param"]

    task = chain( 
        get_stock_data.s("income",param),
        parse_cash_flow.s(param),
        output_datas.s({"NAME":"company","PREFIX":"xueqiu_income" ,"INDEX":["symbol","date","report_name"] }) 
    )
    task.apply_async()