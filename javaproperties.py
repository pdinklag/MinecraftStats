import re

# From jwodder/javaproperties v0.5.2, reading.py.
# Licensed under the MIT license.
# Slightly modified to not require Six (unichr -> chr).

def unescape(field):
    """
    Decode escape sequences in a ``.properties`` key or value.  The following
    escape sequences are recognized::
        \\t \\n \\f \\r \\uXXXX \\\\
    If a backslash is followed by any other character, the backslash is
    dropped.
    In addition, any valid UTF-16 surrogate pairs in the string after
    escape-decoding are further decoded into the non-BMP characters they
    represent.  (Invalid & isolated surrogate code points are left as-is.)
    .. versionchanged:: 0.5.0
        Invalid ``\\uXXXX`` escape sequences will now cause an
        `InvalidUEscapeError` to be raised
    :param field: the string to decode
    :type field: text string
    :rtype: text string
    :raises InvalidUEscapeError: if an invalid ``\\uXXXX`` escape sequence
        occurs in the input
    """
    return re.sub(r'[\uD800-\uDBFF][\uDC00-\uDFFF]', _unsurrogate,
                  re.sub(r'\\(u.{0,4}|.)', _unesc, field))

_unescapes = {'t': '\t', 'n': '\n', 'f': '\f', 'r': '\r'}

def _unesc(m):
    esc = m.group(1)
    if esc[0] == 'u':
        if not re.match(r'^u[0-9A-Fa-f]{4}\Z', esc):
            # We can't rely on `int` failing, because it succeeds when `esc`
            # has trailing whitespace or a leading minus.
            raise InvalidUEscapeError('\\' + esc)
        return chr(int(esc[1:], 16))
    else:
        return _unescapes.get(esc, esc)

def _unsurrogate(m):
    c,d = map(ord, m.group())
    return chr(((c - 0xD800) << 10) + (d - 0xDC00) + 0x10000)

class InvalidUEscapeError(ValueError):
    """
    .. versionadded:: 0.5.0
    Raised when an invalid ``\\uXXXX`` escape sequence (i.e., a ``\\u`` not
    immediately followed by four hexadecimal digits) is encountered in a simple
    line-oriented ``.properties`` file
    """

    def __init__(self, escape):
        #: The invalid ``\uXXXX`` escape sequence encountered
        self.escape = escape
        super(InvalidUEscapeError, self).__init__(escape)

    def __str__(self):
        return 'Invalid \\u escape sequence: ' + self.escape
