#!/usr/bin/env python3

from sig_gen import sig_gen

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

# ARC-Message-Signature b=

d = b'example.org'
ht = b'from:to:subject:arc-authentication-results'
s = b'dummy'
t = b'12345'
i = 1

auth_res = b'i=1; lists.example.org; spf=pass smtp.mfrom=jqd@d1.example; dkim=pass (1024-bit key) header.i=@d1.example; dmarc=pass'

amsh = lambda bh: [
  (b'from', b'John Q Doe <jqd@d1.example.org>'),
  (b'to', b'arc@dmarc.org'),
  (b'subject', b'Example 1'),
  (b'arc-authentication-results', auth_res),
  (b'arc-message-signature', b'a=rsa-sha256; b=; bh=%s; c=relaxed/relaxed; d=%s; h=%s; i=%i; s=%s; t=%s' % (bh, d, ht, i, s, t))
]

arsh = lambda b, bh: [
  (b'arc-authentication-results', auth_res),
  (b'arc-message-signature', b'a=rsa-sha256; b=%s; bh=%s; c=relaxed/relaxed; d=%s; h=%s; i=%i; s=%s; t=%s' % (b, bh, d, ht, i, s, t)),
  (b'arc-seal', b'a=rsa-sha256; b=; cv=none; d=%s; i=%i; s=%s; t=%s' % (d, i, s, t))
]

sig_gen(public, private, body, amsh, arsh, fold=True, verbose=True)
