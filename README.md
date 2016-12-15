# Translator
Simple console application (written for my university python course) for translating some language source code into html-highlighted code by some patterns.

## Description
Translates some language (python / C / bash) source code into html-highlighted code by using some patterns.

## Usage
`main.py [-h] [-b] [-l {python,bash,c}] [-d] sourcefile outputfile`

### Example
`./main.py main.py main.py.html`

### Options
* `-h` / `--help` — show help
* `-b` / `--browser` — open html in default browser
* `-l {python,bash,c}` / `--language {python,bash,c}` — manually select language
* `-d` / `--debug` — run script in debug mode
* `sourcefile` — source file
* `outputfile` — output file

## Structure
### utils.py
Subsidiary functions.
* `_combine_range(lines, start, end)` — combines lines and text in lines into one string from `start` up to `end`
* `tokenize_source_code(source, tokenizer)` — generator, yielding tokens from `sourcecode`, provided with `tokenizer`
* `html_highlight(classified_text)` — generates html formatted text from `classified_text` tokens
* `generate_html_page(classified_text, title)` — generates full html page from `classified_text` tokens and adds `title` into it
### token_types.py
Token type constants.
### tokenizing.py
### main.py
Small script using utils to convert data from nroff into html format.
