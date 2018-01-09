#!/usr/bin/env python3

import sys
import subprocess
import re

OPEN_ARC_PATH = "/home/vagrant/OpenARC/openarc/"
PID_FILE = "/home/vagrant/OpenARC/openarc/"
KEY_FILE = "/home/vagrant/misc/key.pem"
USER = "vagrant"

if len(sys.argv) != 4:
    print("Usage: arcverifytest.py messagefile dnsport verbose", file=sys.stderr)
    sys.exit(1)

conf = '''KeepTemporaryFiles     no

Syslog                    yes
Domain                    example.org
Selector                  dummy
KeyFile                   %s

SignatureAlgorithm        rsa-sha256

UserID                    %s

Socket                    inet:8891@localhost

PidFile                   %s
Canonicalization          relaxed/relaxed
AuthservID                n/a
''' % (KEY_FILE, USER, PID_FILE)

import tempfile
with tempfile.NamedTemporaryFile() as tmp:
    tmp.write(conf.encode('utf-8'))
    tmp.flush()
    
    cmd = [OPEN_ARC_PATH + "openarc",  "-c", tmp.name,  "-v", "-v", "-f", "-l", "-t", sys.argv[1]]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    out  = proc.communicate()[0].decode("utf-8").strip()

    for line in out.split("\n"):
        pref = "### INSHEADER"
        idx = line.find(pref)        
        if(idx != -1):
            regex = re.compile('arc=((\w)+)')
            sys.stdout.write(regex.search(line).groups()[0])
            
