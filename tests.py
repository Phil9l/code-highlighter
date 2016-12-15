#!/usr/bin/python3

import unittest
import tokenizers
from functools import partial
from tokenizers.PyTokenizer import PyTokenizer
from tokenizers.CTokenizer import CTokenizer
from tokenizers.BashTokenizer import BashTokenizer
from utils import tokenize_source_code, Token


class TestTokenizer(unittest.TestCase):
    TOKENIZE = None

    def _test_generator(self, text, result):
        self.assertEqual(list(self.TOKENIZE(text)), result)


class TestPyTokenizer(TestTokenizer):
    TOKENIZE = partial(tokenize_source_code, tokenizer=PyTokenizer)

    def test_comments(self):
        self._test_generator('# no', [Token('# no', 'comment')])
        self._test_generator('#', [Token('#', 'comment')])

    def test_numbers(self):
        self._test_generator('42', [Token('42', 'number')])
        self._test_generator('0x15', [Token('0x15', 'number')])
        self._test_generator('0b001', [Token('0b001', 'number')])
        self._test_generator('0o175', [Token('0o175', 'number')])

    def test_keywords(self):
        self._test_generator('break', [Token('break', 'keyword')])
        self._test_generator('while True',
                             [Token(content='while', type='keyword'),
                              Token(content=' ', type=''),
                              Token(content='True', type='keyword')])

    def test_builtins(self):
        self._test_generator('help()', [Token(content='help', type='builtin'),
                                        Token(content='(', type='operator'),
                                        Token(content=')', type='operator')])

    def test_variables(self):
        self._test_generator('x = 5', [Token(content='x = ', type=''),
                                       Token(content='5', type='number')])

    def test_indent(self):
        data = 'try:\n    pass\nexcept:\n    pass'
        self._test_generator(data, [Token(content='try', type='keyword'),
                                    Token(content=':', type='operator'),
                                    Token(content='\n', type='linebreak'),
                                    Token(content='    ', type='new-indent'),
                                    Token(content='pass', type='keyword'),
                                    Token(content='\n', type='linebreak'),
                                    Token(content='except', type='keyword'),
                                    Token(content=':', type='operator'),
                                    Token(content='\n', type='linebreak'),
                                    Token(content='    ', type='new-indent'),
                                    Token(content='pass', type='keyword')])


class TestCTokenizer(TestTokenizer):
    TOKENIZE = partial(tokenize_source_code, tokenizer=CTokenizer)

    def test_comments(self):
        self._test_generator('// no', [Token('// no', 'comment')])
        self._test_generator('//', [Token('//', 'comment')])

    def test_numbers(self):
        self._test_generator('42', [Token('42', 'number')])
        self._test_generator('0x15', [Token('0x15', 'number')])
        self._test_generator('0b001', [Token('0b001', 'number')])
        self._test_generator('break', [Token('break', 'builtin')])

    def test_keywords(self):
        self._test_generator('while (true)',
                             [Token(content='while', type='builtin'),
                              Token(content=' ', type=''),
                              Token(content='(', type='operator'),
                              Token(content='true', type='keyword'),
                              Token(content=')', type='operator')])

    def test_builtins(self):
        self._test_generator('NULL', [Token(content='NULL', type='keyword')])

    def test_variables(self):
        self._test_generator('x = 5', [Token(content='x = ', type=''),
                                       Token(content='5', type='number')])


if __name__ == '__main__':
    unittest.main()
