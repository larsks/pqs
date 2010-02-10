===========================
PQS -- Parse Quoted Strings
===========================

``pqs`` is a simple module that tokenizes strings.  It splits string on
whitespace but also understands quoted strings, so that it recognizes this
as four tokens::

  this is a test

And this as three tokens::

  this "is a" test

By default it understands about double-quoted and single-quoted substrings,
but you can teach it about others.

Example: Parsing Apache logs
============================

Apache's "combined" log format generates lines that look something like
this::

  10.100.100.100 - guest [10/Feb/2010:12:12:07 -0500] "GET /foo HTTP/1.0"
  200 14967 "http://www.google.com/" "Mozilla/4.0 (compatible; MSIE 6.0;
  Windows NT 5.1; SV1; .NET CLR 1.1.4322) NS8/0.9.6"

(Wrapped for your convenience; please keep in mind that it's actually all
one line.)

You could parse this with the following code::

  import sys
  import pqs
  p = pqs.Parser()
  p.addchars(('[', ']'))

  for line in sys.stdin:
      for tok in p.parse(line):
          print 'delimiters:', tok[0]
          print 'token:', tok[1]
          print '-'

Which, given the input above, would give you the following output::

  delimiters: None
  token: 10.100.100.100
  -
  delimiters: None
  token: -
  -
  delimiters: None
  token: guest
  -
  delimiters: ('[', ']')
  token: 10/Feb/2010:12:12:07 -0500
  -
  delimiters: ('"', '"')
  token: GET /foo HTTP/1.0
  -
  delimiters: None
  token: 200
  -
  delimiters: None
  token: 14967
  -
  delimiters: ('"', '"')
  token: http://www.google.com/
  -
  delimiters: ('"', '"')
  token: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322) NS8/0.9.6

Author
======

| Lars Kellogg-Stedman <lars@oddbit.com>
| http://blog.oddbit.com/

