#!/usr/local/bin/python3.5

# Run the ARC test suite in YAML format agains an implementation

import unittest
import yaml
import argparse

from ddt import ddt, data

SIGN_TEST_FILE = "arc-draft-sign-tests.yml"
VERIFY_TEST_FILE = "arc-draft-verify-tests.yml"

def verify_test(script, test_case):
    print(test_case)
    print(test_case.tid)

def sign_test(script, test_case):
    print(test_case)
    print(test_case.tid)


class ArcVerifyTestCase(object):
    def __init__(self, tid, test, dkim_keys):
        self.tid = tid
        self.test = test
        self.dkim_keys = dkim_keys

    def __str__(self):
        return ""

class ArcSignTestCase(object):
    def __init__(self, tid, test, domain, sel, headers, private, dkim_keys):
        self.tid = tid
        self.test = test
        self.domain = domain
        self.sel = sel
        self.headers = headers
        self.private = private
        self.dkim_keys = dkim_keys

    def __str__(self):
        return ""

def main(op, script, verbose=False):
    tests = []

    if op == "verify":
        scenarios = list(yaml.safe_load_all(open(VERIFY_TEST_FILE, 'rb')))
        for scenario in scenarios:
            tests += [ArcVerifyTestCase(k, v, scenario["dkim_keys"]) for
                      (k, v) in scenario["tests"].items()]
    elif op == "sign":
        scenarios = list(yaml.safe_load_all(open(SIGN_TEST_FILE, 'rb')))
        for scenario in scenarios:
            tests += [ArcSignTestCase(k, v, scenario["domain"], scenario["sel"], scenario["headers"],
                                      scenario["private"], scenario["dkim_keys"]) for
                      (k, v) in scenario["tests"].items()]
    else:
        raise ValueError("invalid operation")

    # this is a little odd
    @ddt
    class ArcTest(unittest.TestCase):
        @data(*tests)
        def test(self, test_case):
            if op == "verify":
                verify_test(script, test_case)
            else:
                sign_test(script, test_case)

    suite = unittest.TestLoader().loadTestsFromTestCase(ArcTest)
    v = 2 if verbose else 1
    unittest.TextTestRunner(verbosity=v).run(suite)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the ARC test suite in YAML format against an implementation.')
    parser.add_argument('op', choices=["sign", "verify"], default="sign", help='Operation to test')
    parser.add_argument('script', help='A command line implementation of an arc signing or verification routing. ')
    parser.add_argument('-t', dest='test', metavar='TEST', required=False, help='Specific test to run')
    parser.add_argument('-v', dest='verbose', action='store_true', required=False, help='verbose')

    args = parser.parse_args()

    main(args.op, args.script, args.verbose)
