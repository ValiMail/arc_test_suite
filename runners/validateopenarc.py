#!/usr/bin/env python3

import sys
import subprocess

if len(sys.argv) != 4:
    print("Usage: arcverifytest.py messagefile dnsport verbose", file=sys.stderr)
    sys.exit(1)

cmd = ["/home/vagrant/OpenARC/openarc/openarc",  "-c",  "/home/vagrant/misc/openarc.conf",  "-f", "-l", "-t", sys.argv[1]]
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
out  = proc.communicate()[0].decode("utf-8").strip()
sys.stdout.write(out)
