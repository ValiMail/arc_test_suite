#!/usr/bin/env python3

# Run the ARC test suite in YAML format agains an implementation

import unittest
import yaml
import argparse

import subprocess, os

from ddt import ddt, data

from arcdns import ArcTestResolver

SIGN_TEST_FILE   = "arc-draft-sign-tests.yml"
VERIFY_TEST_FILE = "arc-draft-verify-tests.yml"

def verify_test(self, script, test_case, port=8053):
    tmp_file = 'tmp/message.txt'
    print(test_case.tid)

    with open(tmp_file,'w') as f:
        f.write(test_case.test["message"])

    with ArcTestResolver(test_case.txt_records, port):
        proc = subprocess.Popen([script, tmp_file, str(port)], stdout=subprocess.PIPE)
        out  = proc.communicate()[0].decode("utf-8")

    self.assertEqual(out.lower(), test_case.test["cv"].lower())

    os.remove(tmp_file)

def sign_test(self, script, test_case, port=8080):
    print(test_case)
    print(test_case.tid)


class ArcVerifyTestCase(object):
    def __init__(self, tid, test, txt_records):
        self.tid = tid
        self.test = test
        self.txt_records = txt_records

    def __str__(self):
        return ""

class ArcSignTestCase(object):
    def __init__(self, tid, test, domain, sel, headers, private, txt_records):
        self.tid = tid
        self.test = test
        self.domain = domain
        self.sel = sel
        self.headers = headers
        self.private = private
        self.txt_records = txt_records

    def __str__(self):
        return ""

def main(op, script, test=None, verbose=False):
    tests = []

    if op == "verify":
        scenarios = list(yaml.safe_load_all(open(VERIFY_TEST_FILE, 'rb')))
        for scenario in scenarios:
            tests += [ArcVerifyTestCase(k, v, scenario["txt_records"]) for
                      (k, v) in scenario["tests"].items()]
    elif op == "sign":
        scenarios = list(yaml.safe_load_all(open(SIGN_TEST_FILE, 'rb')))
        for scenario in scenarios:
            tests += [ArcSignTestCase(k, v, scenario["domain"], scenario["sel"], scenario["headers"],
                                      scenario["private"], scenario["txt_records"]) for
                      (k, v) in scenario["tests"].items()]
    else:
        raise ValueError("invalid operation")

    # use test variable here

    # This is a little odd, but it lets us dynamically
    # create tests from the test file
    @ddt
    class ArcTest(unittest.TestCase):
        @data(*tests)
        def test(self, test_case):
            if op == "verify":
                verify_test(self, script, test_case)
            else:
                sign_test(self, script, test_case)

    suite = unittest.TestLoader().loadTestsFromTestCase(ArcTest)
    v = 2 if verbose else 1
    unittest.TextTestRunner(verbosity=v).run(suite)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the ARC test suite in YAML format against an implementation.')
    parser.add_argument('op', choices=["sign", "verify"], default="sign", help='Operation to test')
    parser.add_argument('script', help='A command line implementation of an arc signing or verification routine. The arguments to the signing script must be [messagefile dnsport selector domain privatekeyfile headers], the arguments to the verification script must be [messagefile dnsport].')
    parser.add_argument('-t', dest='test', metavar='TEST', required=False, help='Specific test to run')
    parser.add_argument('-v', dest='verbose', action='store_true', required=False, help='verbose')

    args = parser.parse_args()
    main(args.op, args.script, args.test, args.verbose)
