
from data.sina_com_cn.request import *

def request_list_data_test():
    data = request_list_data({
        "symbol": "sh600000"
    })
    print(data)

# k线
def request_kline_data_test():
    data = request_kline_data({
        "symbol": "sh688298"
    });
    print(data)

# 分钟线
def request_minuts_data_test():
    # 5分钟
    data = request_minuts_data({
        "symbol" : "sh688298" ,
        "scale" : 5 ,
        "ma"  : "no" ,
        "datalen" : 1023 ,
    })
    print(data)
    return

    # 15分钟
    data = request_minuts_data({
        "symbol" : "sh688298" ,
        "scale" : 15 ,
        "ma"  : "no" ,
        "datalen" : 1023 ,
    })
    print(data)

    # 30分钟
    data = request_minuts_data({
        "symbol" : "sh688298" ,
        "scale" : 30 ,
        "ma"  : "no" ,
        "datalen" : 1023 ,
    })
    print(data)

    # 60分钟
    data = request_minuts_data({
        "symbol" : "sh688298" ,
        "scale" : 60 ,
        "ma"  : "no" ,
        "datalen" : 1023 ,
    })
    print(data)

def request_translist_data_test():
    data = request_translist_data( { "num" : "11", "symbol" : "sh688298" , "rn" : "26512833" } )
    print(data)

# node=sh_a&_s_r_a=page
# sh_a 泸A
# sh_b 泸B
# sz_a 深A
# sz_b 深B

# node=sh_z&_s_r_a=init
# init 债券
# sh_z 泸债
# sz_z 深债
# node=hs_z&_s_r_a=init
# 泸深债券
# node=hskzz_z&_s_r_a=init
# 泸深可转债

# node=hs_a&symbol=&_s_r_a=init
# 泸深A股
# node=hs_b&symbol=&_s_r_a=init
# 泸深B股
# node=hs_z&_s_r_a=init
# 泸深债券
# node=hs_s&_s_r_a=init
# 所有指数
# node=zxqy&symbol=&_s_r_a=init
# 中小企业
# node=cyb&symbol=&_s_r_a=init
# 创业板
# node=kcb&symbol=&_s_r_a=init
# 科创板
# node=shfxjs&symbol=&_s_r_a=init
# 上证风险警示板
# node=dpzs&_s_r_a=init
# 大盘指数

# node=qbgg_hk&_s_r_a=init
# 全部港股
# node=lcg_hk&_s_r_a=init
# 港股 蓝筹股
# node=hcg_hk&_s_r_a=init
# 港股 红筹股
# node=gqg_hk&_s_r_a=init
# 港股 国企股
# node=cyb_hk&_s_r_a=init
# 港股 创业板
# node=zs_hk&_s_r_a=init
# 港股 指数
# node=aplush&_s_r_a=init
# 港股 A+H
# node=hgt_sh&symbol=&_s_r_a=init
# 泸股通 --> 香港可买的国内
# node=hgt_hk&_s_r_a=init
# 港股通 --> 国内可买的香港
# node=sgt_sz&symbol=&_s_r_a=init
# 深港通

# node=tect_us&_s_r_a=init
# 美国科技类
# node=china_us&_s_r_a=init
# 中概股
# node=finance_us&_s_r_a=init
# 美国金融类

def request_stock_list_data_test():
    data = request_stock_count_data({
        "node":"sh_a",
    })
    print(data)

    data = request_stock_list_data({
        "page":2,
        "num": 40,
        "sort":"symbol",
        "asc":1,
        "node":"sh_a",
        "symbol":"",
        "_s_r_a":"page",
    })
    print(data)

def request_us_stock_list_data_test():
    data = request_us_stock_list_data_count({
        "page":1,
        "num":20,
        "sort":"",
        "asc":0,
        "market":"",
        "id":"",
    })
    print(data)

    data = request_us_stock_list_data({
        "page":1,
        "num":20,
        "sort":"",
        "asc":0,
        "market":"",
        "id":"",
    })
    print(data)

def request_lse_stock_list_data_test():
    data = request_lse_stock_list_data({
        "page":1,
        "num":20,
        "sort":"",
        "asc":0,
        "type":"lse_all",
        "_s_r_a":"init",
    })
    print(data)

def request_futures_global_list_data_test():
    data = request_futures_global_list_data_count({
        "page":1,
        "num": 40,
        "sort":"symbol",
        "asc":1,
        "node":"global_qh",
        "_s_r_a":"init",
    })
    print(int(data))

    data = request_futures_global_list_data({
        "page":1,
        "num": 40,
        "sort":"symbol",
        "asc":1,
        "node":"global_qh",
        "_s_r_a":"init",
    })
    print(data)

# node=zzgz_qh&_s_r_a=init
# 中证500期货
# node=szgz_qh&_s_r_a=init
# 上证50期货
# node=sngz_qh&_s_r_a=init
# 10年期国债
# node=gz_qh&_s_r_a=init
# 5年期国债
# node=engz_qh&_s_r_a=init
# 2年期国债
# node=qz_qh&_s_r_a=init
# 泸深300期货
def request_financial_future_list_data_test():
    data = request_financial_future_list_data_count({
        "page":1,
        "num": 40,
        "sort":"symbol",
        "asc":1,
        "node":"zzgz_qh",
        "_s_r_a":"init",
    })
    print(data)

    data = request_financial_future_list_data({
        "page":1,
        "num": 40,
        "sort":"symbol",
        "asc":1,
        "node":"zzgz_qh",
        "_s_r_a":"init",
    })
    print(data)

# node=yy_qh&_s_r_a=init
# 上海-原油
# node=rzjb_qh&_s_r_a=init
# 上海-热轧卷板
# node=zly_qh&_s_r_a=init
# 大连-棕榈油
# node=zc_qh&_s_r_a=init
# 郑州-甲醇
def request_commodity_future_list_data_test():
    data = request_commodity_future_list_data_count({
        "page":1,
        "num": 40,
        "sort":"symbol",
        "asc":1,
        "node":"yy_qh",
        "_s_r_a":"init",
    })
    print(data)

    data = request_commodity_future_list_data({
        "page":1,
        "num": 40,
        "sort":"symbol",
        "asc":1,
        "node":"yy_qh",
        "_s_r_a":"init",
    })
    print(data)

def request_future_kline_data_test():
    data = request_future_kline_data({
        "symbol":"MA2006",
        "_":"2020_5_30"
    })
    print(data)

def request_future_minuts_data_test():
    data = request_future_minuts_data({
        "symbol":"MA2006",
        "type":5,
    })
    print(data)

def request_future_real_data_test():
    data = request_future_real_data({
        "symbol":"MA2006",
        "type":5,
    })
    print(data)

def request_future_day_data_test():
    data = request_future_day_data({
        "symbol":"MA2006",
    })
    print(data)

def request_nodes_test():
    data = request_nodes()
    print(data)

def main():
    request_list_data_test()
    # request_stock_list_data_test()
    # request_kline_data_test()
    # request_minuts_data_test()
    # request_translist_data_test()
    # request_us_stock_list_data_test()
    # request_lse_stock_list_data_test()
    # request_futures_global_list_data_test()
    # request_futures_list_data_test()
    # request_future_list_data_test()
    # request_future2_list_data_test()
    # request_future_kline_data_test()
    # request_future_minuts_data_test()
    # request_future_real_data_test()
    # request_future_day_data_test()
    # request_nodes_test()

if __name__ =="__main__":
    main();