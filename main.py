#!/usr/bin/python3

import argparse
import webbrowser
import os
import logging
from utils import generate_html_page, tokenize_source_code
from tokenizers.PyTokenizer import PyTokenizer
from tokenizers.BashTokenizer import BashTokenizer
from tokenizers.CTokenizer import CTokenizer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Add syntax highlighting to Python source code',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('sourcefile', help='Sourcecode file.')
    parser.add_argument('outputfile', help='Result file name.')
    parser.add_argument('-b', '--browser', action='store_true',
                        help='Run browser with rendered page.')
    parser.add_argument('-l', '--language', type=str,
                        help='Programming language to parse.',
                        choices=['python', 'bash', 'c'])
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Run program in debug mode.')
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    sourcename = args.sourcefile

    tokenizer = None
    if args.language:
        if args.language == 'python':
            tokenizer = PyTokenizer
        elif args.language == 'bash':
            tokenizer = BashTokenizer
        elif args.language == 'c':
            tokenizer = CTokenizer
    else:
        if sourcename.endswith('.py'):
            tokenizer = PyTokenizer
        elif sourcename.endswith('.sh'):
            tokenizer = BashTokenizer
        elif sourcename.endswith('.c'):
            tokenizer = CTokenizer

    if tokenizer is None:
        raise ValueError('No tokenizer found for you language. Specify it '
                         'manually with -l/--language')

    with open(sourcename, 'r') as f:
        source = f.read()

    encoded_text = generate_html_page(tokenize_source_code(source,
                                                           tokenizer))

    with open(args.outputfile, 'w') as f:
        f.write(encoded_text)

    if args.browser:
        webbrowser.open('file://' + os.path.abspath(args.outputfile))
