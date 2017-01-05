#!/usr/bin/env python3

import base64
import textwrap

from dkim.crypto import (
    HASH_ALGORITHMS,
    parse_pem_private_key,
    parse_public_key,
    RSASSA_PKCS1_v1_5_sign,
    RSASSA_PKCS1_v1_5_verify,
    )

class HashThrough(object):
  def __init__(self, hasher):
    self.data = []
    self.hasher = hasher
    self.name = hasher.name

  def update(self, data):
    self.data.append(data)
    return self.hasher.update(data)

  def digest(self):
    return self.hasher.digest()

  def hexdigest(self):
    return self.hasher.hexdigest()

  def hashed(self):
    return b''.join(self.data)



def sig_gen(public, private, body, amsh, arsh, fold=False, verbose=False):
    # body
    hasher = HASH_ALGORITHMS[b'rsa-sha256']
    h = hasher()
    h.update(body)
    bh = base64.b64encode(h.digest())

    print("ams bh= ")
    print(bh)

    #amsh
    hasher = HASH_ALGORITHMS[b'rsa-sha256']
    h = hasher()
    h = HashThrough(hasher())

    h.update(b"\r\n".join([x + b":" + y for (x,y) in amsh(bh)]))
    if verbose:
        print("\nsign ams hashed: %r" % h.hashed())

    pk = parse_pem_private_key(private)
    sig2 = RSASSA_PKCS1_v1_5_sign(h, pk)
    b = base64.b64encode(bytes(sig2))
    if fold:
        b = b[:70] + b" " + b[70:142] + b" " + b[142:]
    print("ams b= ")
    print(b)

    #pk = parse_public_key(base64.b64decode(public))
    #signature = base64.b64decode(b)
    #ams_valid = RSASSA_PKCS1_v1_5_verify(h, signature, pk)
    #print("ams sig valid: %r" % ams_valid)

    hasher = HASH_ALGORITHMS[b'rsa-sha256']
    h = hasher()
    h = HashThrough(hasher())

    h.update(b"\r\n".join([x + b":" + y for (x,y) in arsh(b, bh)]))
    if verbose:
        print("\nsign ars hashed: %r" % h.hashed())

    pk = parse_pem_private_key(private)
    sig2 = RSASSA_PKCS1_v1_5_sign(h, pk)
    b = base64.b64encode(bytes(sig2))
    print("arsh b=")
    print(b)

    #signature = base64.b64decode(b)
    #ams_valid = RSASSA_PKCS1_v1_5_verify(h, signature, pk)
    #print("arsh sig valid: %r" % ams_valid)
