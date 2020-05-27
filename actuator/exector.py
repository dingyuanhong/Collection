from actuator.register import fm
import traceback
import logging

def Exec(content,task):
    if not "host" in task:
        return {"code":404,"msg":"Error Task,no host"};
    if not task["host"] in fm.handlers:
        return {"code":404,"msg":"Host Not Found"};
    host = fm.handlers[task["host"]]
    if not "function" in task:
        return {"code":404,"msg":"Error Task,no function"};
    
    if not task["function"] in host:
        return {"code":404,"msg":"Function Not Found"};
    func = host[task["function"]]
    if func == None:
        return {"code":404,"msg":"Function is None"};
    try:
        print("exec:" + content["exector_id"] +":"+task["host"] +"->"+ task["function"]);
        func(content,task);
        print("exec complite:"+ content["exector_id"] +":" + task["host"] +"->"+ task["function"]);
    except Exception as ex:
        logging.error(traceback.format_exc())
        return {"code":500,"msg":str(ex)};
    return {"code":200};