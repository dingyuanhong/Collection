from .Xueqiu_Rule import  Xueqiu_Rules
from .RequestHelper import CacheRequestHelper,RequestHelper
from .Xueqiu_Cookie  import XueQiuCookieFactory
from .util import get_url_param

def getContentDict(rules):
    dict_ = {};
    for it in rules:
        dict_[it["type"]] = it;
    return dict_;

Xueqiu_Contents_Dict = getContentDict(Xueqiu_Rules);

def getContent(type_):
    if type_ in Xueqiu_Contents_Dict:
        return Xueqiu_Contents_Dict[type_]
    return None

class RequestError(Exception):
    def __init__(self,code,message):
        self.code = code;
        self.message = message;
        Exception.__init__(self, self.code, self.message)

def Xueqiu_request(content,**args):
    rule = content["rule"];

    defaultHeader = {
        "Host": "xueqiu.com",
        "Origin": "https://xueqiu.com",
        # "Referer": "https://xueqiu.com/",
    };
    if "header" in rule:
        header = {**defaultHeader,**rule["header"]};
    else:
        header = defaultHeader;

    data = get_url_param(rule["param"],**args);
    url = rule["url"]
    data = "&".join(data);

    method = "get"
    if "method" in rule:
        method = rule["method"]

    print("default header:",header)
    if method == "get":
        url = url + "?" + data;
        print("请求地址:",url);
        res = RequestHelper(header=header,cookie=XueQiuCookieFactory()).get(url);
    else:
        print("请求地址:",url," 数据:",data);
        res = RequestHelper(header=header,cookie=XueQiuCookieFactory()).post(url,data);

    if res.status_code != 200:
        raise RequestError(res.status_code, res.text)
        return None;
    if "parse" in rule:
        return rule["parse"](content,res)
    return res.text;

class Xueqiu_Excetor:
    @staticmethod
    def Do(func,**arg):
        content = getContent(func)
        data = Xueqiu_request(content,**arg);
        if data == None:
            return None;
        return data;

if __name__ == "__main__":
    count = Xueqiu_Excetor.Do("stocks_list_count",**{
        "type":"hk",
        "market":"HK",
        "is_delay":"true",
    })
    print(count)

    data = Xueqiu_Excetor.Do("stocks_list",**{
        "type":"hk",
        "market":"HK",
        "is_delay":"true",
        "page":str(2),
    })
    print(data[0]);