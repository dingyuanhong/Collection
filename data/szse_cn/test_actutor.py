from .actutor import *

def stock_list_test():
    stock_list(None,{"param":{ "SHOWTYPE":"JSON","CATALOGID":"1110x","TABKEY":"tab1" } } )

def company_data_test():
    company_data(None,{"param": {"secCode":"000659"} })

def stocks_all_test():
    stocks_all(None,{"param": {"subfunction":"stock_data","marketId":"1","cycleType":32} })

def main():
    # stock_list_test()
    # company_data_test()
    stocks_all_test()

if __name__ == "__main__":
    main()