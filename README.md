This is an informal schema for the open source test suites for the [Authenticated Recieved Chain(ARC)](https://tools.ietf.org/html/draft-ietf-dmarc-arc-protocol-01) protocol, illustrated with examples.  This was prototyped from [the OpenSPF Test Suite](http://www.openspf.org/Test_Suite/Schema), and consists of two suites, one for the generation of the ARC header fields, the other for their validation.

The syntax is YAML. The top level object is a "scenario". A file can consist of multiple scenarios separated by '---' on a line by itself. Lexical comments are introduced by '#' and continue to the end of a line. Lexical comments are ignored. There are also comment fields which are part of a scenario, and used for purposes such as automating the annotated RFC.

Here are is an example validation scenario:


Here are is an example signing scenario:






cover all the RFC keywords
cover other important aspects (syntax, tables, common mistakes, tricky corner cases, etc.)


DNS errors
When the last entry for a DNS name is the string TIMEOUT, the test driver should simulate a DNS timeout exception for queries that do not match any preceding records. When the last map for a DNS name is the map RCODE: n, the test driver should simulate a DNS error with code n. The test suite currently uses TIMEOUT, but not RCODE.
