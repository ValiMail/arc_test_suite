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

as_tmp = b'''ARC-Seal: a=rsa-sha256;
    b=%b; cv=pass; d=example.org; i=4; s=dummy;
    t=12348'''

ams_tmp = b'''ARC-Message-Signature: a=rsa-sha256;
    b=%b;
    bh=%bh; c=relaxed/relaxed;
    d=example.org; h=from:to:date:subject:mime-version:arc-authentication-results;
    i=4; s=dummy; t=12348'''

# data
body = b'''Hey gang,
This is a test message.
--J.
'''.replace(b'\n', b'\r\n')

auth_res1 = b'i=1; lists.example.org; spf=pass smtp.mfrom=jqd@d1.example; dkim=pass (1024-bit key) header.i=@d1.example; dmarc=pass'
auth_res2 = b'i=2; lists.example.org; spf=pass smtp.mfrom=jqd@d1.example; dkim=pass (1024-bit key) header.i=@d1.example; dmarc=pass'
auth_res3 = b'i=3; lists.example.org; spf=pass smtp.mfrom=jqd@d1.example; dkim=pass (1024-bit key) header.i=@d1.example; dmarc=pass'
auth_res4 = b'i=4; lists.example.org; spf=pass smtp.mfrom=jqd@d1.example; dkim=pass (1024-bit key) header.i=@d1.example; dmarc=pass'

sig_head = [
    (b'from', b'John Q Doe <jqd@d1.example.org>'),
    (b'to', b'arc@dmarc.org'),
    (b'date', b'Thu, 14 Jan 2015 15:00:01 -0800'),
    (b'subject', b'Example 1'),
    (b'mime-version', b'1.0'),
    (b'arc-authentication-results', auth_res1)
]

d = b'example.org'
s = b'dummy'
t = b'12348'
i = 4

ams1 = b'''a=rsa-sha256; b=QsRzR/UqwRfVLBc1TnoQomlVw5qi6jp08q8lHpBSl4RehWyHQtY3uOIAGdghDk/mO+/Xpm 9JA5UVrPyDV0f+2q/YAHuwvP11iCkBQkocmFvgTSxN8H+DwFFPrVVUudQYZV7UDDycXoM6UE cdfzLLzVNPOAHEDIi/uzoV4sUqZ18=; bh=KWSe46TZKCcDbH4klJPo+tjk5LWJnVRlP5pvjXFZYLQ=; c=relaxed/relaxed; d=example.org; h=from:to:date:subject:mime-version:arc-authentication-results; i=1; s=dummy; t=12345'''

as1 = b'''a=rsa-sha256; b=dOdFEyhrk/tw5wl3vMIogoxhaVsKJkrkEhnAcq2XqOLSQhPpGzhGBJzR7k1sWGokon3TmQ 7TX9zQLO6ikRpwd/pUswiRW5DBupy58fefuclXJAhErsrebfvfiueGyhHXV7C1LyJTztywzn QGG4SCciU/FTlsJ0QANrnLRoadfps=; cv=none; d=example.org; i=1; s=dummy; t=12345'''

ams2 = b"a=rsa-sha256; b=2cDGNznUmp4YSSThCe9nrQIH2Gpd5qPFw3OU8sWFzZgEQ5UZtaVQifVUXUrsSyEzjro3Ul YPPDx+C1K+LbKRlOZ06il4ws2zlPafsrx1piKsKSCUq0KjFs01hYCDBa3tfdyITSfoWu2HHY pCjrhPMPH1jruIdBV/5Gk2Fvy+mW8=; bh=KWSe46TZKCcDbH4klJPo+tjk5LWJnVRlP5pvjXFZYLQ=; c=relaxed/relaxed; d=example.org; h=from:to:date:subject:mime-version:arc-authentication-results; i=2; s=dummy; t=12346"

as2 = b"a=rsa-sha256; b=IAqZJ5HwfNxxsrn9R4ayQgiu9RibPKEUVevbt7XFTkSh1baJ533D2Z6IZ2NaBreUhDBb2e K9Gtcv+eyUhWkD8VTmE6fq/F8CDIK3ScIiJykF8hNL1wpa/mGwWWwBnkozIJGAbTAAX7AgnH knAehnSW99TeU0lmib0XmOt4TN3sY=; cv=pass; d=example.org; i=2; s=dummy; t=12346"

ams3 = b"a=rsa-sha256; b=FEp53xrAEL1qQfytTEmR+Lp/ZpX4bXQvtj/peHauDtix/tlBN2v841lm72vOjK6WfqGB4E X/9vRfV7ZiSRMFvXAWlnDKw5wzoZFyQ3xebnvqraYnq9OA1CrDIFQVLqqGIaZrcZ+fTXt7Kp TBMU/BzIBERwfWXqBG1DqZGYXrHFw=; bh=KWSe46TZKCcDbH4klJPo+tjk5LWJnVRlP5pvjXFZYLQ=; c=relaxed/relaxed; d=example.org; h=from:to:date:subject:mime-version:arc-authentication-results; i=3; s=dummy; t=12347"

as3 = b"a=rsa-sha256; b=EcI6PD1XFx7uTngsG2JZQzTaAyhIGafcKJO+aTb4+PV1QKFHrLLrSv++W872urw2WnEsWJ Hs+YPSVbRGJXbHp4rSM0VasdFb6lf2UUJf8Lxy17f3CzqQQz5CGMO++75t+cManzaOmnjq/Z gGaqK7euJwWo6hzF3pNZYdTJ6JZOo=; cv=pass; d=example.org; i=3; s=dummy; t=12347"

# headers
ht = b":".join([x[0] for x in sig_head])

ams = b'a=rsa-sha256; b=; bh=; c=relaxed/relaxed; d=%s; h=%s; i=%i; s=%s; t=%s' % (d, ht, i, s, t)
amsh = (lambda bh: sig_head + [(b'arc-message-signature', ams.replace(b'bh=', b'bh=' + bh))])

arsh = lambda b, bh: [
    (b'arc-authentication-results', auth_res1),
    (b'arc-message-signature', ams1),
    (b'arc-seal', as1),
    (b'arc-authentication-results', auth_res2),
    (b'arc-message-signature', ams2),
    (b'arc-seal', as2),
    (b'arc-authentication-results', auth_res3),
    (b'arc-message-signature', ams3),
    (b'arc-seal', as3),
    (b'arc-authentication-results', auth_res4),
    (b'arc-message-signature', ams.replace(b'bh=', b'bh=' + bh).replace(b'b=', b'b=' + b)),
    (b'arc-seal', b'a=rsa-sha256; b=; cv=pass; d=%s; i=%i; s=%s; t=%s' % (d, i, s, t))
]

sig_gen(public, private, body, amsh, arsh, fold=True, verbose=True, as_tmp=as_tmp, ams_tmp=ams_tmp)
