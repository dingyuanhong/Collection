import os

root_path = os.getcwd() + "/";
cookie_path = "cookie/index.txt";
cookie_cache = {}
class FileLoader:
    @staticmethod
    def cacheSet(key,cookie):
        replaceKey = key if (".com" not in key) else key[7:int(key.index(".com"))];
        p = cookie_path.replace("index",replaceKey)
        path = root_path + p;
        with open(path,"wb") as fp:
            fp.write(cookie.encode("utf-8"))
    
    @staticmethod
    def cacheGet(key):
        replaceKey = key if (".com" not in key) else key[7:int(key.index(".com"))];
        p = cookie_path.replace("index",replaceKey)
        path = root_path + p;
        
        if os.path.exists(path):
            with open(path,"rb") as fp:
                data = fp.read()
                data = data.decode("utf-8")
            return data;
        return ""
    @staticmethod
    def cacheClear(key):
        replaceKey = key if (".com" not in key) else key[7:int(key.index(".com"))];
        p = cookie_path.replace("index",replaceKey)
        path = root_path + p;
        
        if os.path.exists(path):
            os.remove(path);

    @staticmethod
    def updateCookie(cookie,key):
        cookie_cache[key] = cookie;
        
        FileLoader.cacheSet(key,cookie);
    @staticmethod
    def loadCookie(key):
        if key in cookie_cache:
            return cookie_cache[key];
        return ""


class UserAgent:
    @staticmethod
    def Random():
        lst = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36";
        return lst;


class UrlBuilder:
    def __init__(self,target):
        self.url = target;
        self.config = []
    def add(self,key,value):
        self.config.append(key + "=" + value);
        return self;
    def build(self):
        return self.url + "?" + "&".join(self.config)

import hashlib
def md5(str):
    p = hashlib.md5()
    p.update(str.encode("utf-8"))
    v = p.hexdigest()
    return v;
    
class FileCache:
    def __init__(self,dir = "cache/"):
        self.dir = dir;
    def set(self,key,value):
        path = root_path + self.dir + md5(key);
        with open(path,"wb") as fp:
            fp.write(value.encode("utf-8"))
    
    def get(self,key):
        pass
        path = root_path + self.dir + md5(key);
        if not os.path.exists(path):
            return None;
        with open(path,"rb") as fp:
            data = fp.read()
            return data.decode("utf-8")

def get_url_param(param,**args):
    params = param.copy();
    clr = [];
    for it in params.keys():
        if it in args:
            params[it] = args[it]
        if type(params[it]) == dict:
            if "status" in params[it]:
                clr.append(it)
    for it in clr:
        del params[it];
    data = [key + "=" + str(value)  for key,value in params.items() ];
    return data;