
#https://www.cnblogs.com/ohyb/p/9084011.html
#详细参数见上图网页
#定时器参数

class Timer:
    def __init__(self,**arg):
        self.type = arg["type"];
        del arg["type"];
        if "param" in arg:
            self.param = self.filter(arg["param"]);
        else:
            self.param = self.filter(arg);

    def filter(self,param):
        lst = ["weeks","days","hours","minutes","seconds",
        # "year","month","day","hour","minute","second",
        # "week","day_of_week"
        ];
        for i in lst:
            if i in param:
                param[i] = int(param[i])
        return param;

