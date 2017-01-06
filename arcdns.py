from dnslib.server import DNSServer, DNSLogger
from dnslib.zoneresolver import ZoneResolver

class NullLogger:
    def __init__(self,log="",prefix=True):
        pass
    
    def log_pass(self,*args):
        pass

    def log_prefix(self,handler):
        pass
    
    def log_recv(self,handler,data):
        pass
    
    def log_send(self,handler,data):
        pass
    
    def log_request(self,handler,request):
        pass
    
    def log_reply(self,handler,reply):
        pass
    
    def log_truncated(self,handler,reply):
        pass
    
    def log_error(self,handler,e):
        pass
    
    def log_data(self,dnsobj):
        pass
    
class ArcTestResolver(object):
    def __init__(self, records, port=8053, verbose=False):
        self.records = records
        self.port = port
        self.verbose = verbose

    def __enter__(self):
        zones = []
        for (domain, txt) in self.records.items():
            n = 255
            frags = [("'" + txt[i:i+n] + "'") for i in range(0, len(txt), n)]
            zones.append(domain + " IN TXT " + " ".join(frags))

        resolver = ZoneResolver("\n".join(zones))
        
        if self.verbose:
            logger = DNSLogger()
        else:
            logger = NullLogger()

        self.server = DNSServer(resolver, port=self.port, logger=logger)
        self.server.start_thread()

    def __exit__(self, type, value, traceback):
        self.server.stop()
