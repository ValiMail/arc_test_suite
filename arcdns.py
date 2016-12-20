from dnslib.server import DNSServer, DNSLogger
from dnslib.zoneresolver import ZoneResolver

class ArcTestResolver(object):
    def __init__(self, records, port=8053):
        self.records = records
        self.port = port

    def __enter__(self):
        zones = []
        for (domain, txt) in self.records.items():
            n = 255
            frags = [("'" + txt[i:i+n] + "'") for i in range(0, len(txt), n)]
            zones.append(domain + " IN TXT " + " ".join(frags))

        resolver = ZoneResolver("\n".join(zones))
        logger = DNSLogger()

        self.server = DNSServer(resolver, port=self.port, logger=logger)
        self.server.start_thread()

    def __exit__(self, type, value, traceback):
        self.server.stop()
