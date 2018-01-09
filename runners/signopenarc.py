#!/usr/bin/env python3

import os
import sys
import subprocess
import tempfile
import stat

OPEN_ARC_PATH = "/home/vagrant/OpenARC/openarc/"
PID_FILE = "/home/vagrant/OpenARC/openarc/"
USER = "vagrant"

if len(sys.argv) != 10:
    print("Usage: arcsigntest.py messagefile dnsport privatekeyfile authserv-id selector domain headers timestamp verbose", file=sys.stderr)
    sys.exit(1)

headers = ",".join(sys.argv[7].split(":"))
conf = '''KeepTemporaryFiles     no

Syslog                    yes
Domain                    %s
Selector                  %s
KeyFile                   %s
FixedTimestamp            %s

SignatureAlgorithm        rsa-sha256

UserID                    %s

Socket                    inet:8891@localhost

PidFile                   %s
Canonicalization          relaxed/relaxed
SignHeaders               %s
AuthservID                %s
Mode                      s
''' % (sys.argv[6], sys.argv[5], sys.argv[3], sys.argv[8], USER, PID_FILE, headers, sys.argv[4])

os.chmod(sys.argv[3], stat.S_IREAD | stat.S_IWRITE);

import tempfile
with tempfile.NamedTemporaryFile() as tmp:
    tmp.write(conf.encode('utf-8'))
    tmp.flush()

    cmd = [OPEN_ARC_PATH + "openarc", "-c", tmp.name, "-f", "-v", "-v", "-l", "-t",  sys.argv[1]]

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    out  = proc.communicate()[0].decode("utf-8").strip()
    if(sys.argv[9]):
        sys.stdout.write(out)

    for line in out.split("\n"):
        if(line.startswith("### INSHEADER: ")):
            pref = "'ARC-Message-Signature' hvalue='"
            idx = line.find(pref)
            if(idx != -1):
                sys.stdout.write("ARC-Message-Signature:" + line[idx + len(pref): -1] + "\n\n")

            pref = "'ARC-Authentication-Results' hvalue='"
            idx = line.find(pref)
            if(idx != -1):
                sys.stdout.write("ARC-Authentication-Results:" + line[idx + len(pref): -1] + "\n\n")

            pref = "'ARC-Seal' hvalue='"
            idx = line.find(pref)
            if(idx != -1):
                sys.stdout.write("ARC-Seal:" + line[idx + len(pref): -1])
