from actuator.register import fm; 
from .task import *

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
    task = get_stock_data.s("kline",param)
    print(task.apply_async().get())

    # task = chain( 
    #     get_stock_data.s("kline",param),
    #     output_datas.s({"NAME":"day","PREFIX":"xueqiu" ,"INDEX":["symbol","date"] }) 
    # )
    # task.apply_async()

@fm.route("xueqiu.com","minute_data")
def minute_data(context,task):
    param = task["param"]
    task = get_stock_data.s("minute",param)
    print(task.apply_async().get())

    # task = chain( 
    #     get_stock_data.s("kline",param),
    #     output_datas.s({"NAME":"day","PREFIX":"xueqiu" ,"INDEX":["symbol","date"] }) 
    # )
    # task.apply_async()

@fm.route("xueqiu.com","compinfo_data")
def compinfo_data(context,task):
    param = task["param"]
    task = get_stock_data.s("compinfo",param)
    print(task.apply_async().get())

    # task = chain( 
    #     get_stock_data.s("kline",param), 
    #     output_datas.s({"NAME":"day","PREFIX":"xueqiu" ,"INDEX":["symbol","date"] }) 
    # ) 
    # task.apply_async() 

@fm.route("xueqiu.com","cash_flow_data")
def cash_flow_data(context,task):
    param = task["param"]
    task = get_stock_data.s("cash_flow",param)
    print(task.apply_async().get())

    # task = chain( 
    #     get_stock_data.s("kline",param),
    #     output_datas.s({"NAME":"day","PREFIX":"xueqiu" ,"INDEX":["symbol","date"] }) 
    # )
    # task.apply_async()

@fm.route("xueqiu.com","balance_data")
def balance_data(context,task):
    param = task["param"]
    task = get_stock_data.s("balance",param)
    print(task.apply_async().get())

    # task = chain( 
    #     get_stock_data.s("kline",param),
    #     output_datas.s({"NAME":"day","PREFIX":"xueqiu" ,"INDEX":["symbol","date"] }) 
    # )
    # task.apply_async()

@fm.route("xueqiu.com","income_data")
def income_data(context,task):
    param = task["param"]
    task = get_stock_data.s("income",param)
    print(task.apply_async().get())

    # task = chain( 
    #     get_stock_data.s("kline",param),
    #     output_datas.s({"NAME":"day","PREFIX":"xueqiu" ,"INDEX":["symbol","date"] }) 
    # )
    # task.apply_async()