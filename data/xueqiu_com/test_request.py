from .Xueqiu_Excetor import Xueqiu_Excetor

def request_list_data_test():
    data = Xueqiu_Excetor.Do("stocks_list",**{ "type":"sh_sz", "market":"CN","page":1 } )
    print(type(data))
    print(data)

def request_kline_data_test():
    data = Xueqiu_Excetor.Do("kline",**{ "symbol":"SZ300832" } )
    print(type(data))
    print(data)

def request_minute_data_test():
    data = Xueqiu_Excetor.Do("minute",**{"symbol":"SZ300832","period":"1d" } )
    print(type(data))
    print(data)

def request_compinfo_data_test():
    data = Xueqiu_Excetor.Do("compinfo",**{"symbol":"SZ300832" } )
    print(type(data))
    print(data)

def request_cash_flow_data_test():
    data = Xueqiu_Excetor.Do("cash_flow",**{"symbol":"SZ300832" } )
    print(type(data))
    print(data)

def request_balance_data_test():
    data = Xueqiu_Excetor.Do("balance",**{"symbol":"SZ300832" } )
    print(type(data))
    print(data)

def request_income_data_test():
    data = Xueqiu_Excetor.Do("income",**{"symbol":"SZ300832" } )
    print(type(data))
    print(data)

def main():
    # request_list_data_test()
    # request_kline_data_test()
    # request_minute_data_test()
    # request_compinfo_data_test()
    # request_cash_flow_data_test()
    # request_balance_data_test()
    request_income_data_test()

if __name__ == "__name__":
    main()