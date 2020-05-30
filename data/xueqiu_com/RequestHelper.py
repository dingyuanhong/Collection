import requests
from Xueqiu_Spider.util import *

class Response:
    def __init__(self,v):
        self.__dict__.update(v)

class RequestHelper:
    def __init__(self,header={},cookie=None):
        self.factory = cookie;
        self.header = {**{
            "User-Agent":UserAgent.Random(),
        },**header};
    
    def post(self,url,data):
        res = self._post(url,data)
        if res.status_code != 200:
            if self.checkOrRelogin(res):
                return self._post(url,data)
        return res;

    def get(self,url):
        res = self._get(url)
        if res.status_code != 200:
            if self.checkOrRelogin(res):
                return self._get(url)
        return res;

    def _post(self,url,data):
        if not self.factory:
            header = {**self.header,**{"Cookie": self.factory.get(url)}}
        else:
            header = self.header;
        res = requests.post(url,headers=header,data=data)
        return res;
            
    def _get(self,url):
        if not self.factory:
            header = {**self.header,**{"Cookie": self.factory.get(url)}}
        else:
            header = self.header;
        res = requests.get(url,headers=header)
        return res;
    
    def checkOrRelogin(self,res):
        if self.factory == None:
            return False;
        if self.factory.check(res):
            return self.factory.done();
        return False;

class CacheRequestHelper(RequestHelper):
    def __init__(self,header={},cookie=None):
        RequestHelper.__init__(self,header=header,cookie=cookie)
        self.cache = FileCache()
    
    def post(self,url,data):
        data = self.cache.get(url)
        if data != None:
            return Response({"status_code":200,"text":data});

        res = RequestHelper.post(self,url,data)
        if res.status_code != 200:
            return res;
        
        self.cache.set(url,res.text);
        return res;

    def get(self,url):
        data = self.cache.get(url)
        if data != None:
            return Response({"status_code":200,"text":data});
        
        res = RequestHelper.get(self,url)
        if res.status_code != 200:
            return res;
        
        self.cache.set(url,res.text);
        return res;