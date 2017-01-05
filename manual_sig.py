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


public = b'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDkHlOQoBTzWRiGs5V6NpP3idY6Wk08a5qhdR6wy5bdOKb2jLQiY/J16JYi0Qvx/byYzCNb3W91y3FutACDfzwQ/BC/e/8uBsCR+yz1Lxj+PL6lHvqMKrM3rG4hstT5QjvHO9PzoxZyVYLzBfO2EeC3Ip3G+2kryOTIKT+l/K4w3QIDAQAB'

private = b'''
-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQDkHlOQoBTzWRiGs5V6NpP3idY6Wk08a5qhdR6wy5bdOKb2jLQi
Y/J16JYi0Qvx/byYzCNb3W91y3FutACDfzwQ/BC/e/8uBsCR+yz1Lxj+PL6lHvqM
KrM3rG4hstT5QjvHO9PzoxZyVYLzBfO2EeC3Ip3G+2kryOTIKT+l/K4w3QIDAQAB
AoGAH0cxOhFZDgzXWhDhnAJDw5s4roOXN4OhjiXa8W7Y3rhX3FJqmJSPuC8N9vQm
6SVbaLAE4SG5mLMueHlh4KXffEpuLEiNp9Ss3O4YfLiQpbRqE7Tm5SxKjvvQoZZe
zHorimOaChRL2it47iuWxzxSiRMv4c+j70GiWdxXnxe4UoECQQDzJB/0U58W7RZy
6enGVj2kWF732CoWFZWzi1FicudrBFoy63QwcowpoCazKtvZGMNlPWnC7x/6o8Gc
uSe0ga2xAkEA8C7PipPm1/1fTRQvj1o/dDmZp243044ZNyxjg+/OPN0oWCbXIGxy
WvmZbXriOWoSALJTjExEgraHEgnXssuk7QJBALl5ICsYMu6hMxO73gnfNayNgPxd
WFV6Z7ULnKyV7HSVYF0hgYOHjeYe9gaMtiJYoo0zGN+L3AAtNP9huqkWlzECQE1a
licIeVlo1e+qJ6Mgqr0Q7Aa7falZ448ccbSFYEPD6oFxiOl9Y9se9iYHZKKfIcst
o7DUw1/hz2Ck4N5JrgUCQQCyKveNvjzkkd8HjYs0SwM0fPjK16//5qDZ2UiDGnOe
uEzxBDAr518Z8VFbR41in3W4Y3yCDgQlLlcETrS+zYcL
-----END RSA PRIVATE KEY-----
'''

# body (manually canonicalized)
body = b'''Hey gang,
This is a test message.
--J.
'''.replace(b'\n', b'\r\n')

hasher = HASH_ALGORITHMS[b'rsa-sha256']
h = hasher()
h.update(body)
bh = base64.b64encode(h.digest())

print("ams bh= ")
print(bh)

# ARC-Message-Signature b=

d = b'example.org'
ht = b'from:to:subject:arc-authentication-results'
s = b'dummy'
t = b'12345'
i = 1

fold = False

auth_res = b'i=1; lists.example.org; spf=pass smtp.mfrom=jqd@d1.example; dkim=pass (1024-bit key) header.i=@d1.example; dmarc=pass'

amsh = [
  (b'from', b'John Q Doe <jqd@d1.example.org>'),
  (b'to', b'arc@dmarc.org'),
  (b'subject', b'Example 1'),
  (b'arc-authentication-results', auth_res),
  (b'arc-message-signature', b'a=rsa-sha256; b=; bh=%s; c=relaxed/relaxed; d=%s; h=%s; i=%i; s=%s; t=%s' % (bh, d, ht, i, s, t))
]


hasher = HASH_ALGORITHMS[b'rsa-sha256']
h = hasher()
h = HashThrough(hasher())

h.update(b"\r\n".join([x + b":" + y for (x,y) in amsh]))
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

# ARC-Seal b=

arsh = [
  (b'arc-authentication-results', auth_res),
  (b'arc-message-signature', b'a=rsa-sha256; b=%s; bh=%s; c=relaxed/relaxed; d=%s; h=%s; i=%i; s=%s; t=%s' % (b, bh, d, ht, i, s, t)),
  (b'arc-seal', b'a=rsa-sha256; b=; cv=none; d=%s; i=%i; s=%s; t=%s' % (d, i, s, t))
]

hasher = HASH_ALGORITHMS[b'rsa-sha256']
h = hasher()
h = HashThrough(hasher())

h.update(b"\r\n".join([x + b":" + y for (x,y) in arsh]))
print("\nsign ars hashed: %r" % h.hashed())

pk = parse_pem_private_key(private)
sig2 = RSASSA_PKCS1_v1_5_sign(h, pk)
b = base64.b64encode(bytes(sig2))
print("arsh b=")
print(b)

#signature = base64.b64decode(b)
#ams_valid = RSASSA_PKCS1_v1_5_verify(h, signature, pk)
#print("arsh sig valid: %r" % ams_valid)
