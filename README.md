This is an informal schema for the open source test suites for the [Authenticated Recieved Chain(ARC)](https://tools.ietf.org/html/draft-ietf-dmarc-arc-protocol-01) protocol, illustrated with examples.  This was prototyped from [the OpenSPF Test Suite](http://www.openspf.org/Test_Suite/Schema), and consists of two suites, one for the generation of the ARC header fields, the other for their validation.

Their syntax is YAML. The top level object is a "scenario". A file can consist of multiple scenarios separated by '---' on a line by itself. Lexical comments are introduced by '#' and continue to the end of a line. Lexical comments are ignored. There are also comment fields which are part of a scenario, and used for purposes such as automating the annotated RFC.

## Example validation scenario

```
description: >-
  dummy scenario
tests:
  test1:
    spec:        12/16
    description: basic test
    message:     |
      MIME-Version: 1.0
      Return-Path: <jqd@d1.example.org>
      Received: by 10.157.14.6 with HTTP; Tue, 3 Jan 2017 12:22:54 -0800 (PST)
      Message-ID: <54B84785.1060301@d1.example.org>
      Date: Thu, 14 Jan 2015 15:00:01 -0800
      From: John Q Doe <jqd@d1.example.org>
      To: arc@dmarc.org
      Subject: Example 1

      Hey gang,
      This is a test message.
      --J.
    cv:          None
txt_records:
  dummy._domainkey.example.org: >-
    v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAg1i2lO83x/r58cbo/JSBwfZrrct6S/yi4L6GsG3wNgFE9lO3orzBwnAEJJM33WrvJfOWia1fAx64Vs1QEpYtLFCzyeIhDDMaHv/G8NgKPgnWK4gI8/x2Q2SYCmiqil66oHaSOC2phMDRI+c/Q35MlZbc2FqlgevpKzdCg+YE6mYA0XN7/tdQplbx4meLVsVPIL9QCP4yu8oBsNqcwyxkQafJucVyoZI+VEO+dySw3QXNdmJhr7y1hD1tCNqoAG0iphKQVXPXmGnGhaxaVU92Kq5UKL6/LiTZ1piqyJfJyZ/zCgH+mtY8MNk9f7LHpwFljI7TbYmr7MmV3d6xj3sghwIDAQAB
comment: >-
  This is a comment
```

## Example signing scenario

```
description: >-
  dummy scenario
tests:
  test1:
    spec:        12/16
    description: basic test
    message:     |
      Return-Path: <jqd@d1.example>
      Received: from [10.10.10.131] (w-x-y-z.dsl.static.isp.com [w.x.y.z])
          (authenticated bits=0)
          by segv.d1.example with ESMTP id t0FN4a8O084569;
          Thu, 14 Jan 2015 15:00:01 -0800 (PST)
          (envelope-from jqd@d1.example)
      DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/simple; d=d1.example;
          s=20130426; t=1421363082;
          bh=EoJqaaRvhrngQxmQ3VnRIIMRBgecuKf1pdkxtfGyWaU=;
          h=Message-ID:Date:From:MIME-Version:To:CC:Subject:Content-Type:
           Content-Transfer-Encoding;
          b=HxsvPubDE+R96v9dM9Y7V3dJUXvajd6rvF5ec5BPe/vpVBRJnD4I2weEIyYijrvQw
           bv9uUA1t94kMN0Q+haFo6hiQPnkuDxku5+oxyZWOqtNH7CTMgcBWWTp4QD4Gd3TRJl
           gotsX4RkbNcUhlfnoQ0p+CywWjieI8aR6eof6WDQ=
      Message-ID: <54B84785.1060301@d1.example>
      Date: Thu, 14 Jan 2015 15:00:01 -0800
      From: John Q Doe <jqd@d1.example>
      To: arc@dmarc.org
      Subject: Example 1

      Hey gang,
      This is a test message.
      --J.
    t: 2000000000
    auth-res:    |
      lists.example.org;
      spf=pass smtp.mfrom=jqd@d1.example;
      dkim=pass (1024-bit key) header.i=@d1.example;
      dmarc=pass
    AS:          |
      i=1; cv=none; a=rsa-sha256; d=example.com; s=dummy; t=2000000000;
      b=YC/BQQ2kd2WpTZSAXDazUZ2DsAVtVDW1DrDHI9q96UuV4HUdBOl5bKCyTHr+t5W+l9uC3T
      KURK/Ti1aJlyRX0bmGMWFuBsKlMyjWe+qdLPoJZ7CoE2sJzXFC7R+K1DCOemOU3x6e+8GM5C
      roEJAWXry4KapgKcZgkEWIep/+Oo8=
    AAR:         |
      i=1; lists.example.org;
      spf=pass smtp.mfrom=jqd@d1.example;
      dkim=pass (1024-bit key) header.i=@d1.example;
      dmarc=pass
    AMS:         |
      i=1; a=rsa-sha256; d=example.com; s=dummy; t=2000000000;
      h=From:To:Subject:arc-authentication-results;
      bh=KWSe46TZKCcDbH4klJPo+tjk5LWJnVRlP5pvjXFZYLQ=;
      b=ulWd9KPJwbAoo8uIIpUHjlhpJE8iDSONYJqQxdVn6qxXLmjeGLHvqq5ggGIkL3oBxpwqO
      aEpR3iq+SmCAq0KgHOQtuZ1YG41TJaLOD8Cj5WdSu1luS9tNfwbwWK0RzchEJ0jeS0EaMc9
      eU2XpmxVIP7X/H0kZ9XBkNRw6pIIjCo=
domain:   example.com
sel: dummy
headers: From:To:Subject
privatekey: |
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
txt_records:
  dummy._domainkey.example.org: |
    v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAg1i2lO83x/r58cbo/JSBwfZrrct6S/yi4L6GsG3wNgFE9lO3orzBwnAEJJM33WrvJfOWia1fAx64Vs1QEpYtLFCzyeIhDDMaHv/G8NgKPgnWK4gI8/x2Q2SYCmiqil66oHaSOC2phMDRI+c/Q35MlZbc2FqlgevpKzdCg+YE6mYA0XN7/tdQplbx4meLVsVPIL9QCP4yu8oBsNqcwyxkQafJucVyoZI+VEO+dySw3QXNdmJhr7y1hD1tCNqoAG0iphKQVXPXmGnGhaxaVU92Kq5UKL6/LiTZ1piqyJfJyZ/zCgH+mtY8MNk9f7LHpwFljI7TbYmr7MmV3d6xj3sghwIDAQAB
comment: >-
  This is a comment
```
