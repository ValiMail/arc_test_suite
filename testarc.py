#!/usr/bin/env python3

# Run the ARC test suite in YAML format against an implementation

import unittest
import yaml
import argparse
import subprocess, os

from ddt import ddt, data
from arcdns import ArcTestResolver

DEFAULT_DNS_PORT = 8053
SIGN_TEST_FILE   = "arc-draft-sign-tests.yml"
VALIDATE_TEST_FILE = "arc-draft-validation-tests.yml"

def validate_test(self, script, test_case, port):
    with open('tmp/message.txt', 'w') as f:
        f.write(test_case.test["message"])
    with ArcTestResolver(test_case.txt_records, port):
        proc = subprocess.Popen([script, 'tmp/message.txt', str(port)], stdout=subprocess.PIPE)
        out  = proc.communicate()[0].decode("utf-8")

    os.remove('tmp/message.txt')

    self.assertEqual(out.lower(), test_case.test["cv"].lower())


def sign_test(self, script, test_case, port):
    with open('tmp/message.txt', 'w') as f:
        f.write(test_case.test["message"])
    with open('tmp/privatekey.pem', 'w') as f:
        f.write(test_case.privatekey)
    with open('tmp/authres.txt', 'w') as f:
        f.write(test_case.test["auth-res"])

    with ArcTestResolver(test_case.txt_records, port):
        proc = subprocess.Popen([script, 'tmp/message.txt', str(port), 'tmp/privatekey.pem', 'tmp/authres.txt',
                                 test_case.sel, test_case.domain, test_case.headers, str(test_case.test["t"])],
                                stdout=subprocess.PIPE)
        out  = proc.communicate()[0].decode("utf-8")

    for f in os.listdir('tmp/'):
        os.remove('tmp/' + f)

    as_valid = ams_valid = aar_valid = False
    print(out)
    for sig in out.split("\n\n"):
        sig = "".join(sig.split())
        (k, v) = sig.split(':', 1)
        sig_res = set(v.split(';'))
        if(k.lower() == "arc-authentication-results"):
            s1 = "".join(test_case.test["AAR"].split())
            s1 = set(s1.split(';'))
            aar_valid = (sig_res <= s1)
        elif(k.lower() == "arc-message-signature"):
            s1 = "".join(test_case.test["AMS"].split())
            s1 = set(s1.split(';'))
            ams_valid = (sig_res <= s1)
        elif(k.lower() == "arc-seal"):
            s1 = "".join(test_case.test["AS"].split())
            s1 = set(s1.split(';'))
            as_valid = (sig_res <= s1)
        else:
            continue

    self.assertTrue(aar_valid)
    self.assertTrue(as_valid)
    self.assertTrue(ams_valid)

class ArcValidateTestCase(object):
    def __init__(self, tid, test, txt_records):
        self.tid = tid
        self.test = test
        self.txt_records = txt_records

    def __str__(self):
        return ""

class ArcSignTestCase(object):
    def __init__(self, tid, test, domain, sel, headers, privatekey, txt_records):
        self.tid = tid
        self.test = test
        self.domain = domain
        self.sel = sel
        self.headers = headers
        self.privatekey = privatekey
        self.txt_records = txt_records

    def __str__(self):
        return ""

# This is a little odd, but it lets us dynamically
# create tests from the test file
def genTestClass(op, tests, script, port):
    @ddt
    class ArcTest(unittest.TestCase):
        @data(*tests)
        def test(self, test_case):
            func = sign_test if op == "sign" else validate_test
            func(self, script, test_case, port)

    return ArcTest

def main(op, script, test=None, port=DEFAULT_DNS_PORT, verbose=False):
    tests = []

    if op == "validate":
        scenarios = list(yaml.safe_load_all(open(VALIDATE_TEST_FILE, 'rb')))
        for scenario in scenarios:
            tests += [ArcValidateTestCase(k, v, scenario["txt_records"]) for
                      (k, v) in scenario["tests"].items()]
    elif op == "sign":
        scenarios = list(yaml.safe_load_all(open(SIGN_TEST_FILE, 'rb')))
        for scenario in scenarios:
            tests += [ArcSignTestCase(k, v, scenario["domain"], scenario["sel"], scenario["headers"],
                                      scenario["privatekey"], scenario["txt_records"]) for
                      (k, v) in scenario["tests"].items()]
    else:
        raise ValueError("invalid operation")

    if test:
        tests = [t for t in tests if t.tid == test]

    testClass = genTestClass(op, tests, script, port)
    suite = unittest.TestLoader().loadTestsFromTestCase(testClass)

    v = 2 if verbose else 1
    unittest.TextTestRunner(verbosity=v).run(suite)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the ARC test suite in YAML format against an implementation.')
    parser.add_argument('op', choices=["sign", "validate"], default="sign", help='Operation to test')
    parser.add_argument('script', help='A command line implementation of an arc signing or verification routine. The arguments to the signing script must be [messagefile dnsport selector domain privatekeyfile headers], the arguments to the verification script must be [messagefile dnsport].')
    parser.add_argument('-t', dest='test', metavar='TEST', required=False, help='Specific test to run')
    parser.add_argument('-p', dest='port', default=DEFAULT_DNS_PORT, metavar='port', required=False, help='Port to run stubbed dns server on')
    parser.add_argument('-v', dest='verbose', action='store_true', required=False, help='verbose')

    args = parser.parse_args()
    main(args.op, args.script, args.test, args.port, args.verbose)
