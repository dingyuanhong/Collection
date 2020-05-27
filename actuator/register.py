class actuator_handlers:
    handlers = {};
    def route(self,host,func):
        if not host  in self.handlers:
            self.handlers[host] = {};
        def registe(cls):
            self.handlers[host][func] = cls;
            return cls;
        return registe;

fm = actuator_handlers()