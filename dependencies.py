#! /usr/bin/env python3

from setuptools.command import easy_install

requires = ["dnslib", "dkimpy>=0.7.1", "pyyaml", "ddt", "authheaders"]

for module in requires:
    easy_install.main( ["-U",module] )
