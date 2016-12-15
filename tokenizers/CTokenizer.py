import re
from tokenizing import *


class CTokenizer(BaseTokenizer):
    FLAGS = 0
    TOKENS = [
        (re.compile(r'^    '), INDENT),
        (re.compile(r"#include"), IMPORT),
        (re.compile(r"<[A-Za-z0-9_.]+>"), LIBRARY),
        (re.compile(r'//.*$'), COMMENT),
        (re.compile(r'"[^"]*"'), STRING),
        (re.compile(r"'[^']*'"), STRING),
        (re.compile(r"0b[01]+"), NUMBER),      # BIN
        (re.compile(r"0x[0-9a-f]+"), NUMBER),  # HEX
        (re.compile(r"\d+"), NUMBER),          # INT
        (re.compile(r"\d+.\d+"), NUMBER),      # FLOAT
        (re.compile(r"(\+=|-=|/=|\*=|==|<|>|<=|>=|\+|-|\*|/|\*\*|"
                    r"//|:|\[|\]|\(|\)|%|%=|!=)"), OP),
        (re.compile(r'\d*[A-Za-z_]\w*'), NAME),
        (re.compile(r"\n"), LINE_BREAK),
    ]
    CORRECT_NAME = re.compile(r'^[A-Za-z_]\w*$')

    BUILTINS = {'asm', 'auto', 'break', 'case', 'const', 'continue',
                'default', 'do', 'else', 'enum', 'extern', 'for', 'goto',
                'if', 'register', 'restricted', 'return', 'sizeof', 'static',
                'struct', 'switch', 'typedef', 'union', 'volatile', 'while',
                'bool', 'int', 'long', 'float', 'short', 'double', 'char',
                'unsigned', 'signed', 'void'}

    KEYWORDS = {'true', 'false', 'NULL'}
