import re
from tokenizing import *


class PyTokenizer(BaseTokenizer):
    FLAGS = 0
    TOKENS = [
        (re.compile(r'^    '), INDENT),
        (re.compile(r'#.*$'), COMMENT),
        (re.compile(r'__\w+__'), MAGIC_METHOD),
        (re.compile(r'@\w+'), DECORATOR),
        (re.compile(r'"[^"]*"'), STRING),
        (re.compile(r"'[^']*'"), STRING),
        (re.compile(r"0b[01]+"), NUMBER),      # BIN
        (re.compile(r"0o[0-7]+"), NUMBER),     # OCT
        (re.compile(r"0x[0-9a-f]+"), NUMBER),  # HEX
        (re.compile(r"\d+"), NUMBER),          # INT
        (re.compile(r"\d+.\d+"), NUMBER),      # FLOAT
        (re.compile(r"(\+=|-=|/=|\*=|==|<|>|<=|>=|\+|-|\*|/|\*\*|"
                    r"//|:|\[|\]|\(|\)|%|%=|!=|&|\||\^|&=|\^=|\|=)"), OP),
        (re.compile(r'\d*[A-Za-z_]\w*'), NAME),
        (re.compile(r"\n"), LINE_BREAK),
    ]
    CORRECT_NAME = re.compile(r'^[A-Za-z_]\w*$')

    BUILTINS = {'abs', 'dict', 'help', 'min', 'setattr', 'all', 'dir', 'hex',
                'next', 'slice', 'any', 'divmod', 'id', 'object', 'sorted',
                'ascii', 'enumerate', 'input', 'oct', 'staticmethod', 'bin',
                'eval', 'int', 'open', 'str', 'bool', 'exec', 'isinstance',
                'ord', 'sum', 'bytearray', 'filter', 'issubclass', 'pow',
                'super', 'bytes', 'float', 'iter', 'print', 'tuple',
                'callable', 'format', 'len', 'property', 'type', 'chr',
                'frozenset', 'list', 'range', 'vars', 'classmethod', 'getattr',
                'locals', 'repr', 'zip', 'compile', 'globals', 'map',
                'reversed', '__import__', 'complex', 'hasattr', 'max',
                'round', 'delattr', 'hash', 'memoryview', 'set'}

    KEYWORDS = {'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
                'del', 'elif', 'else', 'except', 'exec', 'finally', 'for',
                'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
                'not', 'or', 'pass', 'print', 'raise', 'return', 'try',
                'while', 'with', 'yield', 'True', 'False'}
