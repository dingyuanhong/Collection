from .task import *

#股票列表
def get_stock_list_test():
    task = get_stock_list.s(None,{"SHOWTYPE":"JSON","CATALOGID":"1110x","TABKEY":"tab1"},{"NAME":"stock","PREFIX":"szse","INDEX":["zqdm"]})
    print(task.apply_async().get())

    # task = get_stock_list_page_data.s(None,{"SHOWTYPE":"JSON","CATALOGID":"1110x","TABKEY":"tab1","PAGENO":1});
    # print(task.apply_async().get())

    # task = chain( 
    #     get_stock_list_page_data.s(None,{"SHOWTYPE":"JSON","CATALOGID":"1110x","TABKEY":"tab1","PAGENO":1}) , 
    #     output_datas.s({"NAME":"stock","PREFIX":"szse"}) 
    # )
    # print(task.apply_async().get())

# 日 周 月
def get_stock_data_test():
    # task = get_stock_data.s(None, {"cycleType":33,"marketId":1,"code":"000659"} );
    # print(task.apply_async().get())
    
    task = chain( 
        get_stock_data.s(None, {"cycleType":32,"marketId":1,"code":"000659"} ) , 
        stock_data_parse.s({"NAME":"day","PREFIX":"szse","INDEX":["code","date"]}) 
    )
    print(task.apply_async().get())

    task = chain( 
        get_stock_data.s(None, {"cycleType":33,"marketId":1,"code":"000659"} ) , 
        stock_data_parse.s({"NAME":"week","PREFIX":"szse","INDEX":["code","date"]}) 
    )
    print(task.apply_async().get())

    task = chain( 
        get_stock_data.s(None, {"cycleType":34,"marketId":1,"code":"000659"} ) , 
        stock_data_parse.s({"NAME":"month","PREFIX":"szse","INDEX":["code","date"]}) 
    )
    print(task.apply_async().get())

# 分
def get_stock_minuts_data_test():
    # task = get_stock_minuts_data.s(None, {"marketId":1,"code":"000659"} );
    # print(task.apply_async().get())

    task = chain( 
        get_stock_minuts_data.s(None, {"marketId":1,"code":"000659"} ) , 
        stock_minuts_parse.s({"NAME":"minute","PREFIX":"szse" ,"INDEX":["code","date","time"] }) 
    )
    print(task.apply_async().get())

def get_company_test():
    # task = get_company.s(None, {"secCode":"000659"} );
    # print(task.apply_async().get())

    task = chain( 
        get_company.s(None, {"secCode":"000659"} ) ,
        output_data.s({"NAME":"company","PREFIX":"szse" ,"INDEX":["agdm"] })
    )
    print(task.apply_async().get())

def main():
    pass
    # get_stock_list_test();
    # get_stock_data_test();
    # get_company_test();
    # get_stock_minuts_data_test();

if __name__ == "__main__":
    main();