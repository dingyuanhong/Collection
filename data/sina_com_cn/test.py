
from data.sina_com_cn.request import *


def request_kline_data_test():
    data = request_kline_data({
        "symbol": "sh688298"
    });
    print(data)

def main():
    request_kline_data_test()

if __name__ =="__main__":
    main();