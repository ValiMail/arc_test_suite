#!/usr/bin/env python3

import base64
import textwrap
import os

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

def sig_gen(public, private, body, amsh, arsh, fold=False, verbose=False, as_tmp = None, ams_tmp = None):
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
    msb = base64.b64encode(bytes(sig2))
    if fold:
        msb = msb[:70] + b" " + msb[70:142] + b" " + msb[142:214]# + b" " + msb[214:286] + b" " + msb[286:]
    print("ams b= ")
    print(msb)

    #pk = parse_public_key(base64.b64decode(public))
    #signature = base64.b64decode(b)
    #ams_valid = RSASSA_PKCS1_v1_5_verify(h, signature, pk)
    #print("ams sig valid: %r" % ams_valid)

    hasher = HASH_ALGORITHMS[b'rsa-sha256']
    h = hasher()
    h = HashThrough(hasher())

    h.update(b"\r\n".join([x + b":" + y for (x,y) in arsh(msb, bh)]))
    if verbose:
        print("\nsign ars hashed: %r" % h.hashed())

    pk = parse_pem_private_key(private)
    sig2 = RSASSA_PKCS1_v1_5_sign(h, pk)
    sb = base64.b64encode(bytes(sig2))
    print("arsh b=")
    print(sb)

    #signature = base64.b64decode(b)
    #ams_valid = RSASSA_PKCS1_v1_5_verify(h, signature, pk)
    #print("arsh sig valid: %r" % ams_valid)

    spc = fold and b"" or b"  "
    accum = ''
    if as_tmp:
        sb = sb[:70] + b"\n    " + spc + sb[70:142] + b"\n    " + spc + sb[142:214]# + b"\n    " + sb[214:286] + b"\n    " + msb[286:]
        res = as_tmp.replace(b'%b', sb)
        accum = res
        print(res.decode('utf-8'))

    if ams_tmp:
        msb = msb.replace(b' ', b'')
        msb = msb[:70] + b"\n    " + spc + msb[70:142] + b"\n    " + spc + msb[142:214]# + b"\n    " + msb[214:286] + b"\n    " + msb[286:]
        res = ams_tmp.replace(b'%bh', bh)
        res = res.replace(b'%b', msb)
        accum += b"\n" + res
        print(res.decode('utf-8'))

    os.system(b'echo "' + accum + b'" | pbcopy')




def sig_gen_multi(public_as, private_as, public_ams, private_ams, body, amsh, arsh, fold=False, verbose=False, as_tmp = None, ams_tmp = None):
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

    pk = parse_pem_private_key(private_ams)
    sig2 = RSASSA_PKCS1_v1_5_sign(h, pk)
    msb = base64.b64encode(bytes(sig2))
    if fold:
        msb = msb[:70] + b" " + msb[70:142] + b" " + msb[142:214]# + b" " + msb[214:286] + b" " + msb[286:]
    print("ams b= ")
    print(msb)

    pk_ams = parse_public_key(base64.b64decode(public_ams))
    signature = base64.b64decode(msb)
    ams_valid = RSASSA_PKCS1_v1_5_verify(h, signature, pk_ams)
    print("ams sig valid: %r" % ams_valid)

    hasher = HASH_ALGORITHMS[b'rsa-sha256']
    h = hasher()
    h = HashThrough(hasher())

    h.update(b"\r\n".join([x + b":" + y for (x,y) in arsh(msb, bh)]))
    if verbose:
        print("\nsign ars hashed: %r" % h.hashed())

    pk = parse_pem_private_key(private_as)
    sig2 = RSASSA_PKCS1_v1_5_sign(h, pk)
    sb = base64.b64encode(bytes(sig2))
    print("arsh b=")
    print(sb)

    pk_as = parse_public_key(base64.b64decode(public_as))
    signature = base64.b64decode(sb)
    ams_valid = RSASSA_PKCS1_v1_5_verify(h, signature, pk_as)
    print("arsh sig valid: %r" % ams_valid)

    spc = fold and b"" or b"  "
    accum = ''
    if as_tmp:
        sb = sb[:70] + b"\n    " + spc + sb[70:142] + b"\n    " + spc + sb[142:214]# + b"\n    " + sb[214:286] + b"\n    " + msb[286:]
        res = as_tmp.replace(b'%b', sb)
        accum = res
        print(res.decode('utf-8'))

    if ams_tmp:
        msb = msb.replace(b' ', b'')
        msb = msb[:70] + b"\n    " + spc + msb[70:142] + b"\n    " + spc + msb[142:214]# + b"\n    " + msb[214:286] + b"\n    " + msb[286:]
        res = ams_tmp.replace(b'%bh', bh)
        res = res.replace(b'%b', msb)
        accum += b"\n" + res
        print(res.decode('utf-8'))

    os.system(b'echo "' + accum + b'" | pbcopy')
