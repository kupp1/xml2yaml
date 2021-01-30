import re
from typing import List
from operator import xor

tag_re = re.compile(
    r"""^(?!<[xX][mM][lL])
    (<\s*([a-zA-Z_][-a-zA-Z_.\d]*)
    ((\s*[a-zA-Z_][-a-zA-Z_.\d]*=(['\"]).*\5)*)
    \s*(/)?>|</\s*([a-zA-Z_][-a-zA-Z_.\d]*)\s*>)""",
    re.X)

open_tag_re = re.compile(
    r"""^(?!<[xX][mM][lL])
    <\s*(?P<name>[a-zA-Z_][-a-zA-Z_.\d]*)
    (?P<attrs>(\s*[a-zA-Z_][-a-zA-Z_.\d]*=(['\"]).*\4)*)\s*>""",
    re.X)

close_tag_re = re.compile(
    r"""^(?!<[xX][mM][lL])</(?P<name>[a-zA-Z_][-a-zA-Z_.\d]*)\s*>""",
    re.X)

self_closed_tag_re = re.compile(r"""^(?!<[xX][mM][lL])
<\s*(?P<name>[a-zA-Z_][-a-zA-Z_.\d]*)
(?P<attrs>(\s*[a-zA-Z_][-a-zA-Z_.\d]*=(['\"]).*\4)*)\s*/>""",
                                re.X)

data_re = re.compile(r'\s*(?P<data>\S[^<>]+)')

attribute_re = re.compile(
    r"""[a-zA-Z_][-a-zA-Z_.\d]*=(["']).*\1""")

decl_re = re.compile(
    r"""<\?xml\s+
    version=['"](?P<ver>\d\.\d)['"]
    (?:\s+encoding=['"](?P<enc>[-a-zA-Z\d]+)['"])?
    (?:\s+standalone=['"](?P<stand>yes|no)['"])?
    \s*\?>""", re.X)


class XmlLexerError(Exception):
    pass


def read_xml_file(f) -> str:
    s = f.read().replace('\n', '').lstrip().rstrip()
    return s


def get_tokens(f) -> List[str]:
    tokens: List[str] = []
    s = read_xml_file(f)
    tmp_p = 0
    for p in range(len(s)):
        c = s[p]
        if c == '<':
            pros_data_match = data_re.match(s[tmp_p:p])
            if pros_data_match and pros_data_match.group('data'):
                tokens.append(pros_data_match.group('data'))
            tmp_p = p
        elif c == '>':
            pros_tag_match = tag_re.match(s[tmp_p:p + 1])
            pros_decl_match = decl_re.match(s[tmp_p:p + 1])
            if xor(bool(pros_tag_match), bool(pros_decl_match)):
                match = pros_tag_match or pros_decl_match
                tokens.append(
                    match.group(0))
            else:
                raise XmlLexerError(
                    'Invalid tag: {}'.format(s[tmp_p:p + 1]))
            tmp_p = p + 1
    return tokens
