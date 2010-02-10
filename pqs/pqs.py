#!/usr/bin/python

import sys
import optparse

DEFAULT_QUOTECHARS = set((
        ('"', '"'),
        ("'", "'"),
        ))

class NewState (Exception):
    '''Raised by Parser._newstate to break out of a nested loop.'''
    pass

class Parser (object):
    '''A class for parsing lines that may contain quoted strings.'''

    def __init__ (self, quotechars=None):
        if quotechars is None:
            quotechars = DEFAULT_QUOTECHARS
        self.quotechars = set(tuple(quotechars))

    def addchars(self, chars):
        '''Add a pair of quote characters.'''
        self.quotechars.add(tuple(chars))

    def _setup(self):
        self._acc       = []
        self._state     = 0
        self._qp        = None

    def _dumpacc(self):
        if not self._acc:
            return

        text = ''.join(self._acc)
        self._acc = []
        return (self._qp, text)

    def _newstate(self, state, qp):
        self._state = state
        self._qp = qp
        raise NewState()

    def parse(self, s):
        '''Parse string ``s``.  Return a list of (quotes, data) tuples,
        where ``quotes`` is the pair of quotes characters that delimited
        the string (None for whitespace).'''

        self._setup()

        for ch in s:
            try:
                if self._state == 0:
                    if ch.isspace():
                        # Looks like a whitespace deliminted
                        # token.
                        self._newstate(0, None)
                    
                    for qp in self.quotechars:
                        if ch == qp[0]:
                            # Found opening quote.
                            self._newstate(1, qp)

                    self._acc.append(ch)
                elif self._state == 1:
                    if ch == self._qp[1]:
                        # Found closing quote.
                        self._newstate(0, None)
                    else:
                        self._acc.append(ch)
            except NewState:
                tok = self._dumpacc()
                if tok:
                    yield(tok)

        tok = self._dumpacc()
        if tok:
            yield(tok)

def parse_args():
    p = optparse.OptionParser()
    p.add_option('-a', '--apache', action='store_true')
    return p.parse_args()

def  main():
    opts, args = parse_args()

    p = Parser()
    if opts.apache:
        p.addchars(('[',']'))

    for line in sys.stdin:
        print '=' * 70
        for tok in p.parse(line):
            print str(tok)

if __name__ == '__main__':
    main()

