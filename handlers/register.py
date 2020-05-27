
class tornado_handlers:
    handlers = [];
    def route(self,path):
        def registe(cls):
            self.handlers.append((path,cls));
        return registe;

fm = tornado_handlers()