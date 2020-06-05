from .actutor import *

def stock_list_test():
    stock_list(None, {"param":{"type":"sh_sz", "market":"CN"} })

def kline_data_test():
    kline_data(None,{ "param":{"symbol":"SZ300832" } } )

def minute_data_test():
    minute_data(None,{ "param":{"symbol":"SZ300832","period":"1d" } } )

def compinfo_data_test():
    compinfo_data(None,{ "param":{"symbol":"SZ300832" } } )

def cash_flow_data_test():
    cash_flow_data(None, { "param":{"symbol":"SZ300832" } } )

def balance_data_test():
    balance_data(None, { "param":{"symbol":"SZ300832" } } )

def income_data_test():
    income_data(None, { "param":{"symbol":"SZ300832" } } )

def main():
    # stock_list_test()
    # kline_data_test()
    # minute_data_test()
    # compinfo_data_test()
    cash_flow_data_test()
    # balance_data_test()
    # income_data_test()

if __name__ == "__main__":
    main()