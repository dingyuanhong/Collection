from task import app
import logging
import data.db as database

#arg : NAME 表名
#      PREFIX 表前缀
#      INDEX 主键,用于去重

@app.task(bind=True)
def output_data(self,data,arg):
    if data == None:
        logging.error("output_data: empty")
        logging.error(arg)
        logging.error(data)
        return;

    db = database.getDB(arg);
    if db == None:
        logging.error("db is empty")
        logging.error(arg)
        logging.error(data)
        return;
    index = None;
    if "INDEX" in arg:
        index = arg["INDEX"]
    db.append(data,index);

#数组结果解析
@app.task(bind=True)
def output_datas(self,data,arg):
    if data == None:
        logging.error("output_data: empty")
        logging.error(arg)
        logging.error(data)
        return;
    
    db = database.getDB(arg);
    if db == None:
        logging.error("db is empty")
        logging.error(arg)
        logging.error(data)
        return;

    index = None;
    if "INDEX" in arg:
        index = arg["INDEX"]
    for it in data:
        db.append(it,index);