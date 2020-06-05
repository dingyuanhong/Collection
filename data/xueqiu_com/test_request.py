from .Xueqiu_Excetor import Xueqiu_Excetor

def request_list_data_test():
    data = Xueqiu_Excetor.Do("stocks_list",**{ "type":"sh_sz", "market":"CN","page":1 } )
    print(type(data))
    print(data)

def request_kline_data_test():
    data = Xueqiu_Excetor.Do("kline",**{ "symbol":"SZ300832" } )
    print(type(data))
    print(data)

def main():
    # request_list_data_test()
    request_kline_data_test()

if __name__ == "__name__":
    main()