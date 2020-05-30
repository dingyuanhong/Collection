import json

def stock_screen_parse(content,res):
    values = json.loads(res.text);
    stocks = [];
    for item in values["list"]:
        stocks.append({"symbol":item["symbol"],"name":item["name"]});
    return stocks;

def stock_screen_count_parse(content,res):
    values = json.loads(res.text);
    count = int(values["count"]);
    return count;



#exchange
#CN 沪深一览
#type
#kcb 科创板
#股票列表数量
stock_screen_count_rule = {
    "param":{
        "category":"SH", #类别
        "exchange":"",   #市场
        "areacode":"",   #地域
        "indcode":"",    #板块代码
        "orderby":"symbol", #排序字段
        "order":"desc",     #排序方式
        "page":"1",
    },
    "url":"https://xueqiu.com/stock/screener/screen.json",
    "parse":stock_screen_count_parse,
};

#股票列表
stock_screen_rule = {
    "param":{
        "category":"SH", #类别
        "exchange":"",   #市场
        "areacode":"",   #地域
        "indcode":"",    #板块代码
        "orderby":"symbol", #排序字段
        "order":"desc",     #排序方式
        "page":"1",
    },
    "url":"https://xueqiu.com/stock/screener/screen.json",
    "parse":stock_screen_parse,
};


#沪深一览
#https://xueqiu.com/service/v5/stock/screener/quote/list?page=1&size=90&order=desc&orderby=percent&order_by=percent&market=CN&type=sh_sz&_=1582548769209
#泸A
#https://xueqiu.com/service/v5/stock/screener/quote/list?type=sha&order_by=percent&order=desc&size=10&page=1&_=1582687522770
#泸B
#https://xueqiu.com/service/v5/stock/screener/quote/list?type=shb&order_by=percent&order=desc&size=10&page=1&_=1582687401721
#深A
#https://xueqiu.com/service/v5/stock/screener/quote/list?type=sza&order_by=percent&order=desc&size=10&page=1&_=1582687544665
#深B
#https://xueqiu.com/service/v5/stock/screener/quote/list?type=szb&order_by=percent&order=desc&size=10&page=1&_=1582687564228
#创业板
#https://xueqiu.com/service/v5/stock/screener/quote/list?type=cyb&order_by=percent&order=desc&size=10&page=1&_=1582687583601
#中小板
#https://xueqiu.com/service/v5/stock/screener/quote/list?type=zxb&order_by=percent&order=desc&size=10&page=1&_=1582687605058


#可转债
#https://xueqiu.com/service/v5/stock/screener/quote/list?page=1&size=90&order=desc&orderby=percent&order_by=percent&exchange=CN&market=CN&industry=%E5%8F%AF%E8%BD%AC%E5%80%BA&type=convert&_=1582549648517
#国债
#https://xueqiu.com/service/v5/stock/screener/quote/list?page=1&size=90&order=desc&orderby=percent&order_by=percent&exchange=CN&market=CN&industry=%E5%9B%BD%E5%80%BA&type=national&_=1582549901964
#企业债
#https://xueqiu.com/service/v5/stock/screener/quote/list?page=1&size=90&order=desc&orderby=percent&order_by=percent&exchange=CN&market=CN&industry=%E4%BC%81%E5%80%BA&type=corp&_=1582549982655


#港股一览
#https://xueqiu.com/service/v5/stock/screener/quote/list?page=1&size=90&order=desc&orderby=percent&order_by=percent&market=HK&type=hk&is_delay=true&_=1582548721702
#美股一览
#https://xueqiu.com/service/v5/stock/screener/quote/list?page=1&size=90&order=desc&orderby=percent&order_by=percent&market=US&type=us&_=1582548971877
#美股明星股
#https://xueqiu.com/service/v5/stock/screener/quote/list?page=1&size=90&order=desc&orderby=percent&order_by=percent&market=US&type=us_star&_=1582549256747
#美股中概股
#https://xueqiu.com/service/v5/stock/screener/quote/list?page=1&size=90&order=desc&orderby=percent&order_by=percent&market=US&type=us_china&_=1582549362835   

def stock_quote_parse(content,res):
    data = json.loads(res.text)["data"];
    count = 0;
    if "count" in data:
        count = int(data["count"]);
    if count > 0:
        return data["list"];
    return [];

def stock_quote_count_parse(content,res):
    data = json.loads(res.text)["data"];
    count = 0;
    if "count" in data:
        count = int(data["count"]);
    return count;

#股票列表
#沪深一览 type:sh_sz market:CN
#沪深科创版 type:kcb market:CN
#可转债 type:convert market:CN industry=%E5%8F%AF%E8%BD%AC%E5%80%BA
#国债 type:national market:CN industry=%E5%8F%AF%E8%BD%AC%E5%80%BA
#企业债 type:corp market:CN industry=%E4%BC%81%E5%80%BA

#港股一览 type:hk market:HK 有is_delay
#美股一览 type:us market:US
#美股明星股 type:us_star market:US
#美股中概股 type:us_china market:US
quote_list_rule = {
    "param":{
        "type":"", #类别
        "market":"",   #市场
        
        "exchange":{
            "use":"market=CN",
            "status":"可选",
        },  #可选,A股需要
        "industry":{
            "use":"market=CN",
            "status":"可选",
        },
        
        "is_delay":{
            "use":"type:hk;market:HK",
            "status":"可选",
        },  #可选,港股需要
        
        "order_by":"symbol",
        "orderby":"symbol", #排序字段
        "order":"desc",     #排序方式
        "page":"1",
        "size":"90",
    },
    "url":"https://xueqiu.com/service/v5/stock/screener/quote/list",
    "parse":stock_quote_parse,
};

quote_list_count_rule = {
    "param":{
        "type":"", #类别
        "market":"",   #市场
        
        "exchange":{
            "use":"market=CN",
            "status":"可选",
        },  #可选,A股需要
        "industry":{
            "use":"market=CN",
            "status":"可选",
        },
        
        "is_delay":{
            "use":"type:hk;market:HK",
            "status":"可选",
        },  #可选,港股需要
        
        "order_by":"symbol",
        "orderby":"symbol", #排序字段
        "order":"desc",     #排序方式
        "page":"1",
        "size":"90",
    },
    "url":"https://xueqiu.com/service/v5/stock/screener/quote/list",
    "parse":stock_quote_count_parse,
};

from bs4 import BeautifulSoup
def ind_code_parse(content,res):
    #index = 0; #沪深板块
    #index = 2; #港股板块
    #index = 3; #美股板块
    index = content["index"];
    soup = BeautifulSoup(res.text);
    divs = soup.find_all("div", class_="third-nav");
    a = divs[index].find_all("a");
    ind_codes = [];
    for it in a:
        ind_codes.append({
            "name":it.attrs["title"],
            "ind_code":it.attrs["data-level2code"],
        });
    return ind_codes;

#沪深板块
ind_code_rule = {
    "url":"https://xueqiu.com/hq",
    "parse":ind_code_parse,
};

#板块
#沪深板块 market:CN exchange:CN
#港股板块 market:HK exchange:HK
#美股板块 market:US exchange:US
ind_code_quote_list_rule = {
    "param":{
        "ind_code":"", #板块
        "market":"",   #市场
        "exchange":"",
        
        "order_by":"symbol",
        "orderby":"symbol", #排序字段
        "order":"desc",     #排序方式
        "page":"1",
        "size":"90",
    },
    "url":"https://xueqiu.com/service/v5/stock/screener/quote/list",
    "parse":stock_screen_parse,
};

#分钟线
#period: 1m 5m 15m 30m 60m 120m day week month quarter year
stock_kline_rule = {
    "param":{
        "symbol":"", #股票编号
        "period":"5m",
        "count":"-142",
        "begin":"1582632396334",
        "type":"before",
        "indicator":"kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance",
    },
    "url":"https://stock.xueqiu.com/v5/stock/chart/kline.json",
};

#当日分时线（实时获取）
#period: 1d 5d （分时 5日）
stock_minute_rule = {
    "param":{
        "symbol":"", #股票编号
        "period":"1d",
    },
    "url":"https://stock.xueqiu.com/v5/stock/chart/minute.json",
};

#活动日个股详情
stock_quote_rule = {
    "param":{
        "symbol":"", #股票编号
        "extend":"detail",
    },
    "url":"https://stock.xueqiu.com/v5/stock/quote.json",
};

#公司简介
stock_compinfo_rule = {
    "param":{
        "symbol":"", #股票编号
    },
    "url":"https://xueqiu.com/stock/f10/compinfo.json",
};

#公司董事
stock_skholder_rule = {
    "param":{
        "symbol":"", #股票编号
    },
    "url":"https://stock.xueqiu.com/v5/stock/f10/cn/skholder.json",
};

#高管增坚持
stock_skholderchg_rule = {
    "param":{
        "symbol":"", #股票编号
        "extend":"true",
        "page":"1",
        "size":"10",
    },
    "url":"https://stock.xueqiu.com/v5/stock/f10/cn/skholderchg.json",
};

#内部交易
# stock_skholderchg_rule = {
#     "param":{
#         "symbol":"", #股票编号
#         "extend":"true",
#         "page":"1",
#         "size":"10",
#     },
#     "url":"https://stock.xueqiu.com/v5/stock/f10/cn/skholderchg.json",
# };

#股东人数
stock_holders_rule = {
    "param":{
        "symbol":"", #股票编号
        "extend":"true",
        "page":"1",
        "size":"10",
    },
    "url":"https://stock.xueqiu.com/v5/stock/f10/cn/holders.json",
};

#限售解禁
stock_shareschg_rule = {
    "param":{
        "symbol":"", #股票编号
        "extend":"true",
        "type":"restricts",
        "page":"1",
        "size":"10",
    },
    "url":"https://stock.xueqiu.com/v5/stock/f10/cn/shareschg.json",
};

#分红增配
stock_bonus_rule = {
    "param":{
        "symbol":"", #股票编号
        "size":"10",
        "page":"1",
    },
    "url":"https://xueqiu.com/stock/f10/bonus.json",
};

#增发一览
stock_cn_bonus_rule = {
    "param":{
        "symbol":"", #股票编号
        "size":"10",
        "page":"1",
        "extend":"true"
    },
    "url":"https://stock.xueqiu.com/v5/stock/f10/cn/bonus.json",
};

#主要指标
stock_indicator_rule = {
    "param":{
        "symbol":"", #股票编号
        "type":"Q4",
        "is_detail":"true",
        "count":"5",
        "timestamp":"",
    },
    "url":"https://stock.xueqiu.com/v5/stock/f10/cn/shareschg.json",
};

#现金流量表
cash_flow_rule = {
    "param":{
        "symbol":"", #股票编号
        "type":"all",
        "is_detail":"true",
        "count":"5",
    },
    "url":"https://stock.xueqiu.com/v5/stock/finance/cn/cash_flow.json",
};

#资产负债表
balance_rule = {
    "param":{
        "symbol":"", #股票编号
        "type":"all",
        "is_detail":"true",
        "count":"5",
    },
    "url":"https://stock.xueqiu.com/v5/stock/finance/cn/balance.json",
};

#利润表
income_rule = {
    "param":{
        "symbol":"", #股票编号
        "type":"all",
        "is_detail":"true",
        "count":"5",
    },
    "url":"https://stock.xueqiu.com/v5/stock/finance/cn/income.json",
};


#雪球规则
Xueqiu_Rules = [
    {
        "name":"股票列表",
        "type":"stocks_list",
        "rule":quote_list_rule
    },
    {
        "name":"股票数量",
        "type":"stocks_list_count",
        "rule":quote_list_count_rule
    },
    {
        "name":"沪深板块列表",
        "type":"sh_sz_inc_code_list",
        "index":0,
        "rule":ind_code_rule,
    },
    {
        "name":"港股板块列表",
        "type":"hk_inc_code_list",
        "index":1,
        "rule":ind_code_rule,
    },
    {
        "name":"美股板块列表",
        "type":"us_inc_code_list",
        "index":3,
        "rule":ind_code_rule,
    },
    {
        "name":"板块股票列表",
        "type":"ind_code_stock_list",
        "rule":ind_code_quote_list_rule,
    },
    {
        "name":"K线",
        "type":"kline",
        "rule":stock_kline_rule,
    },
    {
        "name":"分时线",
        "type":"minute",
        "rule":stock_minute_rule,
    },
    {
        "name":"当日K线",
        "type":"stock",
        "rule":stock_quote_rule,
    },
    {
        "name":"公司简介",
        "type":"compinfo",
        "rule":stock_compinfo_rule,
    },
    {
        "name":"公司董事",
        "type":"skholder",
        "rule":stock_skholder_rule,
    },
    {
        "name":"高管增坚持",
        "type":"skholderchg",
        "rule":stock_skholderchg_rule,
    },
    {
        "name":"股东人数",
        "type":"holders",
        "rule":stock_holders_rule,
    },
    {
        "name":"限售解禁",
        "type":"shareschg",
        "rule":stock_shareschg_rule,
    },
    {
        "name":"分红增配",
        "type":"bonus",
        "rule":stock_bonus_rule,
    },
    {
        "name":"增发一览",
        "type":"cn_bonus",
        "rule":stock_cn_bonus_rule,
    },
    {
        "name":"主要指标",
        "type":"indicator",
        "rule":stock_indicator_rule,
    },
    {
        "name":"现金流量表",
        "type":"cash_flow",
        "rule":cash_flow_rule,
    },
    {
        "name":"资产负债表",
        "type":"balance",
        "rule":balance_rule,
    },
    {
        "name":"利润表",
        "type":"income",
        "rule":income_rule,
    },
];