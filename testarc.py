#!/usr/bin/env python3

# Run the ARC test suite in YAML format against an implementation
#
# DEPENDENCIES:
#  ddt, pyyaml, dnslib
#

import unittest
import sys

try:
    import yaml
    import argparse
    import subprocess, os

    from ddt import ddt, data
    from arcdns import ArcTestResolver
except:
    print("Mising dependency. Please check requirements.txt")
    sys

DEFAULT_DNS_PORT = 8053
SIGN_TEST_FILE   = "tests/arc-draft-sign-tests.yml"
VALIDATE_TEST_FILE = "tests/arc-draft-validation-tests.yml"

def validate_test(self, script, test_case, port, verbose=False):
    if verbose:
        print("\nTEST: %s" % test_case.tid)
        print("DESC: %s" % test_case.test['description'])
        print("MSG:")
        print(test_case.test['message'])

    with open('tmp/message.txt', 'w') as f:
        f.write(test_case.test["message"])
    with ArcTestResolver(test_case.txt_records, port, verbose):
        proc = subprocess.Popen([script, 'tmp/message.txt', str(port), str(verbose)], stdout=subprocess.PIPE)
        out  = proc.communicate()[0].decode("utf-8").strip()

    os.remove('tmp/message.txt')

    if verbose:
        print("RESULT:")

    self.assertEqual(out.lower(), test_case.test["cv"].lower(), test_case.tid)


def sign_test(self, script, test_case, port, verbose=False):
    if verbose:
        print("\nTEST: %s" % test_case.tid)
        print("DESC: %s" % test_case.test['description'])
        print("MSG:")
        print(test_case.test['message'])

    with open('tmp/message.txt', 'w') as f:
        f.write(test_case.test["message"])
    with open('tmp/privatekey.pem', 'w') as f:
        f.write(test_case.privatekey)

    with ArcTestResolver(test_case.txt_records, port, verbose):
        proc = subprocess.Popen([script, 'tmp/message.txt', str(port), 'tmp/privatekey.pem', test_case.test["srv-id"],
                                 test_case.sel, test_case.domain, test_case.test["sig-headers"], str(test_case.test["t"]), str(verbose)],
                                stdout=subprocess.PIPE)
        out  = proc.communicate()[0].decode("utf-8")

    for f in os.listdir('tmp/'):
        os.remove('tmp/' + f)

    if verbose:
        print("\nOutput ARC-Set:")
        print(out)
        print("Expected ARC-Set:")
        print("ARC-Seal: %s" % test_case.test["AS"])
        print("ARC-Message-Signature: %s" % test_case.test["AMS"])
        print("ARC-Authentication-Results: %s" % test_case.test["AAR"])

    as_valid = ams_valid = aar_valid = False
    if out == "":
        aar_valid = test_case.test["AAR"] == ""
        ams_valid = test_case.test["AMS"] == ""
        as_valid  = test_case.test["AS"]  == ""
    else:
        for sig in out.split("\n\n"):
            sig = "".join(sig.split())
            (k, v) = sig.split(':', 1)
            sig_res = set(v.split(';'))
            if(k.lower() == "arc-authentication-results"):
                s1 = "".join(test_case.test["AAR"].split())
                s1 = set(s1.split(';'))
                aar_valid = (s1 == sig_res)
            elif(k.lower() == "arc-message-signature"):
                s1 = "".join(test_case.test["AMS"].split())
                s1 = set(s1.split(';'))
                ams_valid = (sig_res == s1)
            elif(k.lower() == "arc-seal"):
                s1 = "".join(test_case.test["AS"].split())
                s1 = set(s1.split(';'))
                as_valid = (sig_res == s1)
            else:
                continue

    print(aar_valid, ams_valid, as_valid)
    if verbose:
        print("RESULT:")

    self.assertTrue(aar_valid, test_case.tid)
    self.assertTrue(as_valid, test_case.tid)
    self.assertTrue(ams_valid, test_case.tid)

class ArcValidateTestCase(object):
    def __init__(self, tid, test, txt_records):
        self.tid = tid
        self.test = test
        self.txt_records = txt_records

    def __str__(self):
        return ""

class ArcSignTestCase(object):
    def __init__(self, tid, test, domain, sel, privatekey, txt_records):
        self.tid = tid
        self.test = test
        self.domain = domain
        self.sel = sel
        self.privatekey = privatekey
        self.txt_records = txt_records

    def __str__(self):
        return ""

# This is a little odd, but it lets us dynamically
# create tests from the test file
def genTestClass(op, tests, script, port, verbose=False):
    @ddt
    class ArcTest(unittest.TestCase):
        @data(*tests)
        def test(self, test_case):
            func = sign_test if op == "sign" else validate_test
            func(self, script, test_case, port, verbose)

    return ArcTest

def main(op, script, test=None, port=DEFAULT_DNS_PORT, verbose=False):
    tests = []

    if op == "validate":
        scenarios = list(yaml.safe_load_all(open(VALIDATE_TEST_FILE, 'rb')))
        for scenario in scenarios:
            tests += [ArcValidateTestCase(k, v, scenario["txt-records"]) for
                      (k, v) in scenario["tests"].items()]
    elif op == "sign":
        scenarios = list(yaml.safe_load_all(open(SIGN_TEST_FILE, 'rb')))
        for scenario in scenarios:
            tests += [ArcSignTestCase(k, v, scenario["domain"], scenario["sel"],
                                      scenario["privatekey"], scenario["txt-records"]) for
                      (k, v) in scenario["tests"].items()]
    else:
        raise ValueError("invalid operation")

    if test:
        tests = [t for t in tests if t.tid == test]

    testClass = genTestClass(op, tests, script, port, verbose)
    suite = unittest.TestLoader().loadTestsFromTestCase(testClass)

    v = 2 if verbose else 1
    unittest.TextTestRunner(verbosity=v).run(suite)

desc = '''
OVERVIEW:
  This script can run either the signing or validation test suites against
  an ARC implementation, given a command line wrapper for this logic.

DEPENDENCIES:
  specified in requirements.txt

DNS:
  During execution of the script a DNS server is started on a local port and
  this port is passed to the runner.  This server hosts the key files needed
  for ARC signature validation.  There are two suggested methods of routing
  DNS traffic to this server:
  1. Stub out your dns calls.  You can see this in practice in
    runners/validatedkimpy.py
  2. OS level DNS rerouting. On *nix, prepending 'nameserver 127.0.0.1' to
    /etc/resolv.conf will check localhost:53 for DNS traffic.  You'll also
    need to pass -p 53 to the script, and run with sudo(to access port 53).
    This is only temporary and an be reverted once you're done.
  Something like this is necessary to correctly use this script.

VALIDATION:
  Running './testarc.py validate script' will call script once for each
  test case in the validation suite with the following arguments:
  >>> script messagefile dnsport verbose
  messagefile - a path to the message being validated
  dnsport     - a dns server will be running on locaclhost:dnsport
  verbose     - True/False, if the -v flag is passed to ./testarc.py

  The script is expected to return Pass/Fail/None, depending on the ARC
  validation status of the message.  If this matches the value in the
  suite, the test passes.

SIGNING:
  Running './testarc.py sign script' will call script once for each
  test case in the signing suite with the following arguments:
  >>> script messagefile dnsport privatekeyfile authresfile selector domain headers timestamp verbose
  messagefile    - a path to the message being validated
  dnsport        - a dns server will be running on locaclhost:dnsport
  privatekeyfile - the private key used to sign the message
  authserv-id    - the authserv-id of the Authentication-Results headers to prefix
  selector       - the signing selector
  domain         - the signing domain
  headers        - a colon separated list of headers to sign
  timestamp      - a simulated unix timestamp to sign the message with
  verbose        - True/False, if the -v flag is passed to ./testarc.py

  The script is expected to return the ARC-Authentication-Results,
  ARC-Seal, and ARC-Message-Signature of the signature, on successive lines.
  These are matched up to permutaion(of both headers & tags) to the results
  in the test suite.
'''


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('op', choices=["sign", "validate"], default="sign", help='Suite to test')
    parser.add_argument('script', help='A command line implementation of an arc signing or verification routine')
    parser.add_argument('-t', dest='test', metavar='TEST', required=False, help='Specific test to run')
    parser.add_argument('-p', dest='port', default=DEFAULT_DNS_PORT, metavar='port', required=False, help='Port to run stubbed dns server on', type=int)
    parser.add_argument('-v', dest='verbose', action='store_true', required=False, help='verbose')

    args = parser.parse_args()
    main(args.op, args.script, args.test, args.port, args.verbose)
