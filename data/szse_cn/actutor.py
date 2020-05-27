from actuator.register import fm; 
from .task import *
import data.db as database

@fm.route("szse.com","stock_list")
def stock_list(context,task):
    param = {"SHOWTYPE":"JSON","CATALOGID":"1110x","TABKEY":"tab1"};
    param = task["param"];

    task = get_stock_list.s(None,param,{"NAME":"stock","PREFIX":"szse" ,"INDEX":["zqdm"] })
    task.apply_async();

@fm.route("szse.com","stock_data")
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
def minuts_data(context,task):
    param = {"marketId":1,"code":"000659"};
    param = task["param"];
    task = chain( 
        get_stock_minuts_data.s(None, param ) , 
        stock_minuts_parse.s({"NAME":"minute","PREFIX":"szse" ,"INDEX":["code","date","time"] }) 
    )
    task.apply_async()

@fm.route("szse.com","company_data")
def company_data(context,task):
    param = {"secCode":"000659"};
    param = task["param"];
    task = chain( 
        get_company.s(None, param ) ,
        output_data.s({"NAME":"company","PREFIX":"szse" ,"INDEX":["agdm"] })
    )
    task.apply_async()

@fm.route("szse.com","stocks_data")
def stocks_data(context,task):
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
    
    db = database.getDB({"NAME":"stock","PREFIX":"szse"});
    codes = db.get_stock_ids()
    task = group([
        chain( 
            get_stock_data.s(None, {**param,**{"code":code} }) , 
            stock_data_parse.s({"NAME":name,"PREFIX":"szse" ,"INDEX":["code","date"] }) 
        ) for code in codes])
    task.apply_async()

@fm.route("szse.com","stocks_minuts_data")
def stocks_minuts_data(context,task):
    param = {"marketId":1,"code":"000659"};
    param = task["param"];

    db = database.getDB({"NAME":"stock","PREFIX":"szse"});
    codes = db.get_stock_ids()
    task = group([
        chain( 
            get_stock_minuts_data.s(None, {**param,**{"code":code}} ) , 
            stock_minuts_parse.s({"NAME":"minute","PREFIX":"szse" ,"INDEX":["code","date","time"] }) 
        ) for code in codes])
    task.apply_async()

@fm.route("szse.com","stocks_company_data")
def stocks_company_data(context,task):
    param = {"secCode":"000659"};
    param = task["param"];
    db = database.getDB({"NAME":"stock","PREFIX":"szse"});
    codes = db.get_stock_ids()
    task = group([
        chain( 
            get_company.s(None, {**param,**{"secCode":code}} ) ,
            output_data.s({"NAME":"company","PREFIX":"szse" ,"INDEX":["agdm"] })
        ) for code in codes])
    task.apply_async()