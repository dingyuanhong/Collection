from actuator.register import fm; 
from .task import *
import data.db as database
import copy

class self_handlers:
    handlers = {};
    def route(self,func):
        def registe(cls):
            self.handlers[func] = cls;
            return cls;
        return registe;

this = self_handlers()

@fm.route("sina.com.cn","stock_run")
@this.route("stock_run")
def stock_run(context,task):
    function = task["function"]
    host = this.handlers[function]
    host(context,task);

@fm.route("sina.com.cn","stocks_all")
@this.route("stocks_all")
def stocks_all(context,task):
    db = database.getDB({"NAME":"stock","PREFIX":"sina_a"});
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

@fm.route("sina.com.cn","real_data")
@this.route("real_data")
def real_data(context,task):
    param = {"symbol": "sh688298"};
    param = task["param"];

    task = chain( 
        get_real_data.s(None,param),
        output_data.s({ "NAME":"minute","PREFIX":"sina_real" ,"INDEX":["symbol","date","time"] }) 
    )
    task.apply_async();

@fm.route("sina.com.cn","kline_data")
@this.route("kline_data")
def kline_data(context,task):
    param = {"symbol": "sh688298"};
    param = task["param"];

    task = chain( 
        get_kline_data.s(None,param),
        output_datas.s({ "NAME":"day","PREFIX":"sina_a" ,"INDEX":["symbol","date"] }) 
    )
    task.apply_async();

@fm.route("sina.com.cn","minuts_data")
@this.route("minuts_data")
def minuts_data(context,task):
    param = {"symbol" : "sh688298" , "scale" : 5 , "ma"  : "no" , "datalen" : 1023};
    param = task["param"];

    task = chain( 
        get_minuts_data.s(None,param),
        output_datas.s({ "NAME":"minute","PREFIX":"sina_a_" + str(param["scale"]) ,"INDEX":["symbol","day"] }) 
    )
    task.apply_async();

@fm.route("sina.com.cn","stock_list_data")
@this.route("stock_list_data")
def stock_list_data(context,task):
    param = { "sort":"symbol","asc":1,"node":"sh_a","symbol":"","_s_r_a":"page", "num":40 };
    param = task["param"];

    task = get_stock_list.s(None,param,{ "NAME":"stock","PREFIX":"sina_a" ,"INDEX":["symbol"] })
    # task = chain( 
    #     get_stock_list_data.s(None,param),
    #     output_datas.s({ "NAME":"stock","PREFIX":"sina_a" ,"INDEX":["symbol"] }) 
    # )
    task.apply_async();

@fm.route("sina.com.cn","us_stock_list_data")
@this.route("us_stock_list_data")
def us_stock_list_data(context,task):
    param = { "sort":"symbol","asc":1,"id":"","market":"", "num":20 };
    param = task["param"];

    task = get_us_stock_list.s(None,param,{"NAME":"stock","PREFIX":"sina_us" ,"INDEX":["symbol"] })
    task.apply_async();

@fm.route("sina.com.cn","futures_global_list_data")
@this.route("futures_global_list_data")
def futures_global_list_data(context,task):
    param = { "sort":"symbol","asc":1,"node":"global_qh","_s_r_a":"init" };
    param = task["param"];

    task = get_futures_global_list.s(None,param,{"NAME":"stock","PREFIX":"sina_global_future" ,"INDEX":["symbol"] })
    task.apply_async();

@fm.route("sina.com.cn","financial_future_list")
@this.route("financial_future_list")
def financial_future_list(context,task):
    param = { "sort":"symbol","asc":1,"node":"zzgz_qh","_s_r_a":"init" };
    param = task["param"];

    task = get_financial_future_list.s(None,param,{"NAME":"stock","PREFIX":"sina_financial_future" ,"INDEX":["symbol"] })
    task.apply_async();

@fm.route("sina.com.cn","commodity_future_list")
@this.route("commodity_future_list")
def commodity_future_list(context,task):
    param = { "sort":"symbol","asc":1,"node":"yy_qh","_s_r_a":"init" };
    param = task["param"];

    task = get_commodity_future_list.s(None,param,{"NAME":"stock","PREFIX":"sina_commodity_future" ,"INDEX":["symbol"] })
    task.apply_async();

@fm.route("sina.com.cn","future_kline_data")
@this.route("future_kline_data")
def future_kline_data(context,task):
    param = { "symbol":"MA2006","_":"2020_5_30" };
    param = task["param"];

    task = chain( 
        get_future_kline_data.s(None,param),
        output_datas.s({"NAME":"day","PREFIX":"sina_future" ,"INDEX":["symbol","date"] }) 
    )
    task.apply_async()

@fm.route("sina.com.cn","future_minuts_data")
@this.route("future_minuts_data")
def future_minuts_data(context,task):
    param = { "symbol":"MA2006","type": 5 };
    param = task["param"];

    task = chain( 
        get_future_minuts_data.s(None,param),
        output_datas.s({"NAME":"minute","PREFIX":"sina_future_"+ str(param["type"]) ,"INDEX":["symbol","date"] }) 
    )
    task.apply_async()

@fm.route("sina.com.cn","future_real_data")
@this.route("future_real_data")
def future_real_data(context,task):
    param = { "symbol":"MA2006" };
    param = task["param"];

    task = chain( 
        get_future_real_data.s(None,param),
        output_datas.s({"NAME":"minute","PREFIX":"sina_future_real" ,"INDEX":["symbol","date","time"] }) 
    )
    task.apply_async()

@fm.route("sina.com.cn","future_day_data")
@this.route("future_day_data")
def future_day_data(context,task):
    param = { "symbol":"MA2006" };
    param = task["param"];

    task = chain(
        get_future_day_data.s(None,param),
        output_datas.s({"NAME":"day","PREFIX":"sina_future_four" ,"INDEX":["symbol","date","time"] }) 
    )
    task.apply_async()