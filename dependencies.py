#! /usr/bin/env python3

import subprocess
import sys

requires = ["dnslib", "dkimpy>=0.7.1", "pyyaml", "ddt", "authheaders"]

def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

for module in requires:
    install(module)
