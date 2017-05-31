#!/usr/bin/env python3

import sys
import subprocess

if len(sys.argv) != 10:
    print("Usage: arcsigntest.py messagefile dnsport privatekeyfile authresfile selector domain h\
eaders timestamp verbose", file=sys.stderr)
    sys.exit(1)

authres = open(sys.argv[4]).read()
authres = "\n\t".join(authres.split("\n")[0:-1])
val = "Authentication-Results: " + authres + "\n" + open(sys.argv[1]).read()
msgloc = "/home/vagrant/tmp/msg.txt"
f = open(msgloc, 'w')
f.write(val)
f.flush()

cmd = ["/home/vagrant/OpenARC/openarc/openarc",  "-c",  "/home/vagrant/misc/openarc.conf",  "-f", "-l"\
, "-t", msgloc]
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
out  = proc.communicate()[0].decode("utf-8").strip()
sys.stdout.write(out)
