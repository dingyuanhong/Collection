
from datetime import datetime
import os

import tornado
import tornado.web
from tornado import web
import tornado.ioloop
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
import logging
logging.basicConfig(level=logging.DEBUG,
	# filename='server.log',
	# filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
	format="%(asctime)s %(filename)s[%(lineno)d] %(name)s %(levelname)s %(message)s",
	datefmt = '%Y-%m-%d %H:%M:%S %a'
)

from handlers.register import *
from config import *
from db.mongo import MongoFactory
from Scheduler import *
import init

class Application(web.Application):
    def __init__(self):
        handlers = fm.handlers;
        logging.debug("可用方法:"+str(handlers))
        static_handlers = [
            (r"/(.*)",tornado.web.StaticFileHandler, {"path": "./Web/public/"})
        ]
        settings = dict(
            debug=True,
            autoescape=None,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        super(Application, self).__init__(handlers + static_handlers, **settings)
        self.db = MongoFactory();
        self.scheduler = start_scheduler(**{"db":self.db});

def main():
    http_server = HTTPServer(Application(), xheaders=True)
    http_server.bind(PORT, HOST)
    http_server.start()
    IOLoop.instance().start()

if __name__ == "__main__":
    main()