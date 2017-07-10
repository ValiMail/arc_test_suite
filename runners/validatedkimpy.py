#!/usr/bin/env python3

import sys
import logging
from dnslib.server import DNSRecord
import dkim

if len(sys.argv) != 4:
    print("Usage: arcverifytest.py messagefile dnsport verbose", file=sys.stderr)
    sys.exit(1)

def arctestdns(name):
    try:
        q = DNSRecord.question(name.decode("utf-8"), "TXT")
        a = q.send("localhost", int(sys.argv[2]))
        r = DNSRecord.parse(a)
        if not r.get_a().rdata:
            return None
        return "".join([x.decode('utf-8') for x in r.get_a().rdata.data])
    except:
        return None

if(sys.argv[3].lower() == 'true'):
    logging.basicConfig(level=10)

with open(sys.argv[1],'rb') as mf:
    cv, results, comment = dkim.arc_verify(mf.read(), dnsfunc=arctestdns)

if cv == None:
    cv = b''
    
sys.stdout.write(cv.decode("utf-8"))
