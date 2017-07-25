#!/usr/bin/env python3

import sys
import logging
from dnslib.server import DNSRecord
from authheaders import authenticate_message
import dkim

if len(sys.argv) != 10:
    print("Usage: arcsigntest.py messagefile dnsport privatekeyfile authserv-id selector domain headers timestamp verbose", file=sys.stderr)
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

if(sys.argv[9].lower() == 'true'):
    logging.basicConfig(level=10)
    
with open(sys.argv[1],'rb') as mf, open(sys.argv[3],'rb') as pkf:
    message    = mf.read()
    privatekey = pkf.read()

    srv_id = sys.argv[4]    
    sig = dkim.arc_sign(message, sys.argv[5].encode(), sys.argv[6].encode(),
                        privatekey, srv_id.encode(), include_headers=sys.argv[7].encode().split(b':'),
                        timestamp=sys.argv[8], standardize=True)
    
sys.stdout.write(b"\n".join(sig).decode('utf-8'))
