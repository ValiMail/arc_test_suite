This is an informal schema for the open source test suites for the [Authenticated Recieved Chain(ARC)](https://tools.ietf.org/html/draft-ietf-dmarc-arc-protocol-01) protocol, illustrated with examples.  This was prototyped from [the OpenSPF Test Suite](http://www.openspf.org/Test_Suite/Schema), and consists of two suites, one for the generation of the ARC header fields, the other for their validation.

Their syntax is YAML. The top level object is a "scenario". A file can consist of multiple scenarios separated by '---' on a line by itself. Lexical comments are introduced by '#' and continue to the end of a line. Lexical comments are ignored. There are also comment fields which are part of a scenario, and used for purposes such as automating the annotated RFC.


## Example Validation Scenario

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

## Header Format Standardization
There is explicit ambiguity & indeterminism supported by the ARC & DKIM specs with respect to the format of signature headers.  Implementors are free to add aditional tags, whitespace, and to arbitrarily order tags, etc.  This degree of variability makes it impossible to predict message signatures from inputs.  Therefore, for the purposeses of the signing section of this test suite, we assume the signing implementer uses a standardized header format for both ARC-Message-Signature, and ARC-Seal header fields:
```
 - All tags are ordered alphabetically by key
 - All tag keys are lowercase
 - All tag values are lowercase except for b= and bh=
 - There is no whitespace(newlines, crlf, spaces) asside from exactly one space after separator semi-colons
 - There is no trailing semi-colon
 - The ARC-Seal tag set will be exactly - (a, b, cv, d, i, s, t)
 - The ARC-Message-Signature tag set will be exactly - (a, b, b, bh, d, h, i, s, t)
```

## Example Signing Scenario

```
description: >-
  dummy scenario
tests:
  test1:
    spec:        12/16
    description: basic signing test
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
    t: 12345
    auth-res:    |
      lists.example.org;
      spf=pass smtp.mfrom=jqd@d1.example;
      dkim=pass (1024-bit key) header.i=@d1.example;
      dmarc=pass
    AS:          |
      a=rsa-sha256; b=IaZ4npLgFgc9i3JDL6oFfcVQ7iQSqG/FwG/yxWuU9AXQo+Ok/XQFeAWw
      ggU7R4EoHtMJx8EPeZUn6phEeSKV9OEBzYOHwIsOlwROiMrJWZLou2BWmZLGa9aEPeBcwU6D
      A+irfTr1mZ5QpUMnNWS1fSfXr6F75PMKzIAC+2x6kZA=;
      cv=none; d=example.org; i=1; s=dummy; t=12345
    AMS:         |
      a=rsa-sha256;
      b=PPmj0EZEUoVzNwRTVP+XHllkfcG6A25l499LkWaI3D7SOeFA5DuPKnCFT9RwHXDaJc8Ee2
      3e18MOYEJ2xE4jrk2pSu65vpLMZYJ1DCcaYk3cXfHTcTDeZ3I+xjfQs0GdKR9YhHO0VBNUeM
      7HDAXXx6oZCbuKeM6NKHMq0uLDKus=;
      bh=KWSe46TZKCcDbH4klJPo+tjk5LWJnVRlP5pvjXFZYLQ=; d=example.org;
      h=from:to:subject:arc-authentication-results; i=1; s=dummy; t=12345
    AAR:         |
      i=1; lists.example.org;
      spf=pass smtp.mfrom=jqd@d1.example;
      dkim=pass (1024-bit key) header.i=@d1.example;
      dmarc=pass
domain:     example.org
sel:        dummy
headers:    from:to:subject
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
    v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDkHlOQoBTzWRiGs5V6NpP3idY6Wk08a5qhdR6wy5bdOKb2jLQiY/J16JYi0Qvx/byYzCNb3W91y3FutACDfzwQ/BC/e/8uBsCR+yz1Lxj+PL6lHvqMKrM3rG4hstT5QjvHO9PzoxZyVYLzBfO2EeC3Ip3G+2kryOTIKT+l/K4w3QIDAQAB
comment: >-
  This is a comment
```
