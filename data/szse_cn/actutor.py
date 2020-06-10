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

@fm.route("szse.com","stock_run")
@this.route("stock_run")
def stock_run(context,task):
    function = task["function"]
    host = this.handlers[function]
    host(context,task);

@fm.route("szse.com","stocks_all")
@this.route("stocks_all")
def stocks_all(context,task):
    db = database.getDB({"NAME":"stock","PREFIX":"szse"});
    codes = db.get_szse_stock_ids()

    param = task["param"]
    task["function"] = param["subfunction"]
    del param["subfunction"];
    if not task["function"]:
        raise Exception("未知的方法")
    if len(task["function"]) == 0 :
        raise Exception("未定义的方法")
    
    for code in codes :
        param["code"] = code;
        task["param"] = param;
        stock_run(context,copy.deepcopy(task))

@fm.route("szse.com","stock_list")
@this.route("stock_list")
def stock_list(context,task):
    param = {"SHOWTYPE":"JSON","CATALOGID":"1110x","TABKEY":"tab1"};
    param = task["param"];

    task = get_stock_list.s(None,param,{"NAME":"stock","PREFIX":"szse" ,"INDEX":["zqdm"] })
    task.apply_async();

@fm.route("szse.com","stock_data")
@this.route("stock_data")
def stock_data(context,task):
    param = {"cycleType":32,"marketId":1,"code":"000659"};
    param = task["param"];
    name = ""
    if param["cycleType"] == 32:
        name = "day"
    elif  param["cycleType"] == 33:
        name="week"
    elif  param["cycleType"] == 34:
        name="month"
    else:
        return None;
    
    task = chain( 
        get_stock_data.s(None, param ) , 
        stock_data_parse.s({"NAME":name,"PREFIX":"szse" ,"INDEX":["code","date"] }) 
    )
    task.apply_async()

@fm.route("szse.com","minuts_data")
@this.route("minuts_data")
def minuts_data(context,task):
    param = {"marketId":1,"code":"000659"};
    param = task["param"];
    task = chain( 
        get_stock_minuts_data.s(None, param ) , 
        stock_minuts_parse.s({"NAME":"minute","PREFIX":"szse" ,"INDEX":["code","date","time"] }) 
    )
    task.apply_async()

@fm.route("szse.com","company_data")
@this.route("company_data")
def company_data(context,task):
    param = {"secCode":"000659"};
    param = task["param"];
    if "code" in param:
        param["secCode"] = param["code"]

    task = chain( 
        get_company.s(None, param ) ,
        output_data.s({"NAME":"company","PREFIX":"szse" ,"INDEX":["agdm"] })
    )
    task.apply_async()