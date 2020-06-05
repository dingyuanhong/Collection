from .actutor import *

def real_data_test():
    real_data(None, {"param":{ "symbol" : "sh600000"  } } )

def stock_list_data_test():
    stock_list_data(None,{"param":{ "sort":"symbol","asc":1,"node":"hs_a","symbol":"","_s_r_a":"page"  } } )

def kline_data_test():
    kline_data(None,{"param": {"symbol":"sh600000"} })
    pass

def minuts_data_test():
    minuts_data(None,{"param": { "symbol" : "sh600000" , "scale" : 5 , "ma"  : "no" , "datalen" : 1023 } } )

def us_stock_list_data_test():
    us_stock_list_data(None,{ "param":{ "sort":"symbol","asc":1,"id":"","market":""  } } )

def futures_global_list_data_test():
    futures_global_list_data(None,{ "param":{ "sort":"symbol","asc":1,"node":"global_qh","_s_r_a":"init"  } } )

def financial_future_list_test():
    financial_future_list(None,{ "param":{ "sort":"symbol","asc":1,"node":"zzgz_qh","_s_r_a":"init"  } } )

def commodity_future_list_test():
    commodity_future_list(None,{ "param":{ "sort":"symbol","asc":1,"node":"yy_qh","_s_r_a":"init"  } } )

def future_kline_data_test():
    future_kline_data(None,{ "param":{ "symbol":"MA2007","_":"2020_5_30" } } )

def future_minuts_data_test():
    future_minuts_data(None,{ "param":{ "symbol":"MA2007","type": 5 } } )

def future_real_data_test():
    future_real_data(None,{ "param":{ "symbol":"MA2007" } } )

def future_day_data_test():
    future_day_data(None,{ "param":{ "symbol":"MA2007" } } )

def main():
    real_data_test()
    # stock_list_data_test()
    # kline_data_test()
    # minuts_data_test()
    # us_stock_list_data_test()
    # futures_global_list_data_test()
    # financial_future_list_test()
    # commodity_future_list_test()
    # future_kline_data_test()
    # future_minuts_data_test()
    # future_real_data_test()
    # future_day_data_test()

if __name__ == "__main__":
    main()