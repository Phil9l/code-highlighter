import re
from tokenizing import *


class BashTokenizer(BaseTokenizer):
    TOKENS = [
        (re.compile(r'^    '), INDENT),
        (re.compile(r'#!.*$'), COMMENT),
        (re.compile(r'"[^"]*"'), STRING),
        (re.compile(r"'[^']*'"), STRING),
        (re.compile(r"\d+"), NUMBER),          # INT
        (re.compile(r"\d+.\d+"), NUMBER),      # FLOAT
        (re.compile(r"(\+=|-=|/=|\*=|==|<|>|<=|>=|\+|-|\*|/|\*\*|"
                    r"//|:|\[|\]|\(|\)|`|%|%=|!=)"), OP),
        (re.compile(r'\d*[A-Za-z_$][A-Za-z0-9_$\{}#]*'), NAME),
        (re.compile(r"\n"), LINE_BREAK),
    ]
    CORRECT_NAME = re.compile(r'^[A-Za-z0-9_$#]\w*$')
    VARIABLE = re.compile(r'^\$\{?[A-Za-z0-9_$#]+\}?$')

    BUILTINS = {'alias', 'bg', 'bind', 'break', 'builtin', 'caller', 'cd',
                'command', 'compgen', 'complete', 'declare', 'dirs', 'disown',
                'echo', 'enable', 'eval', 'exec', 'exit', 'export', 'false',
                'fc', 'fg', 'getopts', 'hash', 'help', 'history', 'jobs',
                'kill', 'let', 'local', 'logout', 'popd', 'printf', 'pushd',
                'pwd', 'read', 'readonly', 'set', 'shift', 'shopt', 'source',
                'suspend', 'test', 'time', 'times', 'trap', 'true', 'type',
                'typeset', 'ulimit', 'umask', 'unalias', 'unset', 'wait'}

    KEYWORDS = {'if', 'fi', 'else', 'while', 'do', 'done', 'for', 'then',
                'return', 'function', 'case', 'select', 'continue', 'until',
                'esac', 'elif'}
