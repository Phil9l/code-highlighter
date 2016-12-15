import re
from token_types import *


class Token(object):
    def __init__(self, token_type, content, start, end):
        self._type = token_type
        self._content = content
        self._start = start
        self._end = end

    def __str__(self):
        return self._content

    def __repr__(self):
        return '<Token: {} ({}, {})>'.format(self._content, self._start,
                                             self._end)

    @property
    def type(self):
        return self._type

    @property
    def content(self):
        return self._content

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end


class BaseTokenizer(object):
    TOKENS = []
    CORRECT_NAME = re.compile(r'^[A-Za-z_]\w*$')
    BUILTINS = {}
    KEYWORDS = {}
    VARIABLE = None

    @classmethod
    def _check_builtin(cls, token):
        return token in cls.BUILTINS

    @classmethod
    def _check_keyword(cls, token):
        return token in cls.KEYWORDS

    @classmethod
    def _parse_line(cls, line):
        result = None, None
        for token, token_type in cls.TOKENS:
            cres = re.search(token, line)
            if cres is None:
                continue
            if result[0] is None or result[0].start() > cres.start():
                result = cres, token_type
        return result

    @classmethod
    def _handle_line(cls, line, line_index):
        offset = 0
        while line:
            regex_token, token_type = cls._parse_line(line)
            if token_type == NAME and cls._check_builtin(regex_token.group(0)):
                token_type = BUILTIN
            if token_type == NAME and cls._check_keyword(regex_token.group(0)):
                token_type = KEYWORD
            if regex_token is None:
                break
            start, end = (line_index, offset + regex_token.start()), \
                         (line_index, offset + regex_token.end()),

            content = regex_token.group(0)
            if token_type == NAME:
                if re.match(cls.CORRECT_NAME, content) is None:
                    # TODO: Make it work
                    token_type = INCORRECT_NAME
                if cls.VARIABLE is not None and \
                   re.match(cls.VARIABLE, content) is not None:
                    token_type = VARIABLE

            yield Token(token_type, content, start, end)
            offset += regex_token.end()
            line = line[regex_token.end():]

    @classmethod
    def tokenize(cls, lines):
        indent, cur_indent = 0, 0
        for index, line in enumerate(lines, 1):
            for data in cls._handle_line(line, index):
                if data.type == INDENT:
                    cur_indent += 1
                    if cur_indent > indent:
                        indent = cur_indent
                        data._type = NEW_INDENT
                elif data.type == LINE_BREAK:
                    cur_indent = 0
                else:
                    while indent > cur_indent:
                        indent -= 1
                        yield Token(DEDENT, '', data.start, data.start)
                yield data
