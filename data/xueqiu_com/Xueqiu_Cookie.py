import os
from Xueqiu_Spider.util import *

class XueqiuCookie:
    def update(self,areacode,userID,password,rememberMe):
        areacode = areacode if (areacode != None) else os.environ["xueqiu_login_area_code"];
        userID = userID if (userID != None) else os.environ["xueqiu_login_user_id"];
        password = password if (password != None) else os.environ["xueqiu_login_password"];
        rememberMe = rememberMe if (rememberMe != None) else os.environ["xueqiu_login_rememberMe"];
        if (userID != None and password != None):
            self.website = self.login(areacode, userID, password, rememberMe);
        else:
            return False;
#         print("请求地址:",self.website)
        res = RequestHelper(header={
            "Host": "xueqiu.com",
            "Referer": "https://xueqiu.com/",
        }).get(self.website)
#         print(res.text)
        cookies = res.cookies.items()
        cookie = ''
        for name, value in cookies:
            cookie += '{0}={1};'.format(name, value)
#         print("cookie:",cookie)
        return cookie;
    
    def url(self):
        return "http://xueqiu.com/user/login";
    
    def website(self):
        return self.website;
    
    def login(self,areacode,userID,password,rememberMe):
        areacode = "86" if(areacode == None) else areacode;
        builder = UrlBuilder(self.url()) \
            .add("areacode",areacode).add("telephone",userID) \
            .add("password",password).add("remember_me","on" if(rememberMe) else "off");
        return builder.build()

class XueQiuCookieFactory:
    def get(self,url):
        return FileLoader.cacheGet(url);

    def check(self,res):
        print(res.text)
        v = json.loads(res.text)
        if v["error_code"] == "400016":
            return True
        return False;

    def done(self,):
        cookie = XueqiuCookie()
        data = cookie.update("86","18923716519","3a425690",True)
        if data:
            FileLoader.cacheSet(data,cookie.website());
        else:
            FileLoader.cacheClear(cookie.website());

if __name__ == "__main__":
    cookie = XueqiuCookie()
    data = cookie.update("86","18923716519","3a425690",True)
    print(not data)
    print(data)