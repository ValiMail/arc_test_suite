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

sig_head = [
    (b'mime-version', b'1.0'),
    (b'date', b'Thu, 14 Jan 2015 15:00:01 -0800'),    
    (b'from', b'John Q Doe <jqd@d1.example.org>'),
    (b'to', b'arc@dmarc.org'),        
    (b'subject', b'Example 1'),
]

h = b":".join([x[0] for x in sig_head])

as_tmp = b'''    AS:          |
      a=rsa-sha256;
      b=%b; cv=pass; d=example.org; i=2; s=dummy;
      t=12346'''

ams_tmp = b'''    AMS:         |
      a=rsa-sha256;
      b=%b;
      bh=%bh; c=relaxed/relaxed;
      d=example.org; h=;
      i=2; s=dummy; t=12346'''.replace(b'h=;', b'h=' + h + b';')

# data
body = b'''Hey gang,
This is a test message.
--J.
'''.replace(b'\n', b'\r\n')

auth_res1 = b'i=1; lists.example.org; arc=none; spf=pass smtp.mfrom=jqd@d1.example; dkim=pass (1024-bit key) header.i=@d1.example; dmarc=pass'
auth_res2 = b'i=2; lists.example.org; arc=pass; spf=pass smtp.mfrom=jqd@d1.example; dkim=pass (1024-bit key) header.i=@d1.example; dmarc=pass'


d = b'example.org'
s = b'dummy'
t = b'12346'
i = 2

ams1 = b'''a=rsa-sha256; b=XWeK9DxQ8MUm+Me5GLZ5lQ3L49RdoFv7m7VlrAkKb3/C7jjw33TrTY0KYI5lkowvEGnAtm 5lAqLz67FxA/VrJc2JiYFQR/mBoJLLz/hh9y77byYmSO9tLfIDe2A83+6QsXHO3K6PxTz7+v rCB4wHD9GADeUKVfHzmpZhFuYOa88=; bh=KWSe46TZKCcDbH4klJPo+tjk5LWJnVRlP5pvjXFZYLQ=; c=relaxed/relaxed; d=example.org; h=mime-version:date:from:to:subject; i=1; s=dummy; t=12345'''
as1 = b'''a=rsa-sha256; b=KalMXVkx0O4PZIytFfe3i6B/c64408LkuF6rYR9HzBsTazolbsFg/nTah+zh9xmVnylcbg gZnvu+Rte97HXb9fCK6/rAJQJ97NvYVgzwnEiAzCDts/3dS3SO+PyoAV2HxGMQlUgNeqidAc mpm7kE3NbSpgq8Z/rsK5FZ7ADceXw=; cv=none; d=example.org; i=1; s=dummy; t=12345'''

ams = b'a=rsa-sha256; b=; bh=; c=relaxed/relaxed; d=%s; h=%s; i=%i; s=%s; t=%s' % (d, h, i, s, t)
amsh = (lambda bh: sig_head + [(b'arc-message-signature', ams.replace(b'bh=', b'bh=' + bh))])

arsh = lambda b, bh: [
    (b'arc-authentication-results', auth_res1),
    (b'arc-message-signature', ams1),
    (b'arc-seal', as1),
    (b'arc-authentication-results', auth_res2),
    (b'arc-message-signature', ams.replace(b'bh=', b'bh=' + bh).replace(b'b=', b'b=' + b)),
    (b'arc-seal', b'a=rsa-sha256; b=; cv=pass; d=%s; i=%i; s=%s; t=%s' % (d, i, s, t))
]

sig_gen(public, private, body, amsh, arsh, fold=False, verbose=True, as_tmp=as_tmp, ams_tmp=ams_tmp)
