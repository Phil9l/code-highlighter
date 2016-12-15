import html
import logging
import collections
import tokenizing


with open('template.html') as f:
    HTML_TEMPLATE = f.read()
Position = collections.namedtuple('Position', 'row, column')
Token = collections.namedtuple('Token', 'content, type')


def _combine_range(lines, start, end):
    if start.row == end.row:
        return lines[start.row - 1][start.column:end.column], end
    rows = [lines[start.row - 1][start.column:]]
    rows += lines[start.row:end.row - 1]
    rows += [lines[end.row - 1][:end.column]]
    return ''.join(rows), end


def tokenize_source_code(source, tokenizer):
    lines = source.splitlines(True)
    written = Position(1, 0)
    for tok in tokenizer.tokenize(lines):
        t_type, t_str = tok.type, tok.content
        (srow, scol), (erow, ecol) = tok.start, tok.end

        start_pos, end_pos = Position(srow, scol), Position(erow, ecol)
        curent_token = Token(t_str, t_type)

        result_type = ''
        if curent_token.type == tokenizing.COMMENT:
            result_type = 'comment'
        elif curent_token.type == tokenizing.NUMBER:
            result_type = 'number'
        elif curent_token.type == tokenizing.OP:
            result_type = 'operator'
        elif curent_token.type == tokenizing.STRING:
            result_type = 'string'
        elif curent_token.type == tokenizing.BUILTIN:
            result_type = 'builtin'
        elif curent_token.type == tokenizing.KEYWORD:
            result_type = 'keyword'
        elif curent_token.type == tokenizing.INDENT:
            result_type = 'indent'
        elif curent_token.type == tokenizing.DEDENT:
            result_type = 'dedent'
        elif curent_token.type == tokenizing.NEW_INDENT:
            result_type = 'new-indent'
        elif curent_token.type == tokenizing.INCORRECT_NAME:
            result_type = 'incorrect-name'
        elif curent_token.type == tokenizing.LINE_BREAK:
            result_type = 'linebreak'
        elif curent_token.type == tokenizing.VARIABLE:
            result_type = 'variable'
        elif curent_token.type == tokenizing.IMPORT:
            result_type = 'import'
        elif curent_token.type == tokenizing.LIBRARY:
            result_type = 'library'
        elif curent_token.type == tokenizing.MAGIC_METHOD:
            result_type = 'magic-method'
        elif curent_token.type == tokenizing.DECORATOR:
            result_type = 'decorator'

        if result_type:
            if written != start_pos:
                text, written = _combine_range(lines, written, start_pos)
                if text:
                    yield Token(text, '')
            text, written = curent_token.content, end_pos
            if text:
                yield Token(text, result_type)
    line_upto_token, written = _combine_range(lines, written, end_pos)
    if line_upto_token:
        yield Token(line_upto_token, '')


def html_highlight(classified_text):
    result = []
    for token_content, token_type in classified_text:
        if token_type == 'linebreak':
            result.append('<br />')
            continue
        if token_type == 'dedent':
            result.append('</div></div>')
        if token_type:
            result.append('<span class="{}">'.format(token_type))
        result.append(html.escape(token_content))
        if token_type:
            result.append('</span>')
        if token_type == 'new-indent':
            result.append('<div class="content-block"><span class="toggle">-'
                          '</span><div class="line-container">'
                          '<div class="line"></div><br /></div>'
                          '<div class="content">')

    return ''.join(result)


def generate_html_page(classified_text, title='python'):
    result = html_highlight(classified_text)
    title = html.escape(title)
    return HTML_TEMPLATE.format(title=title, body=result, class_name=title)
