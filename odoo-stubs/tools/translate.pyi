# Stubs for odoo.tools.translate (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

import csv
from typing import Any, Optional

WEB_TRANSLATION_COMMENT: str
SKIPPED_ELEMENTS: Any
ENGLISH_SMALL_WORDS: Any

class UNIX_LINE_TERMINATOR(csv.excel):
    lineterminator: str = ...

def encode(s: Any): ...

TRANSLATED_ELEMENTS: Any
TRANSLATED_ATTRS: Any
avoid_pattern: Any
node_pattern: Any

def translate_xml_node(node: Any, callback: Any, parse: Any, serialize: Any): ...
def parse_xml(text: Any): ...
def serialize_xml(node: Any): ...
def parse_html(text: Any): ...
def serialize_html(node: Any): ...
def xml_translate(callback: Any, value: Any): ...
def html_translate(callback: Any, value: Any): ...
def translate(cr: Any, name: Any, source_type: Any, lang: Any, source: Optional[Any] = ...): ...

class GettextAlias:
    def __call__(self, source: Any): ...

_ = GettextAlias()

def quote(s: Any): ...

re_escaped_char: Any
re_escaped_replacements: Any

def unquote(str: Any): ...

class PoFile:
    buffer: Any = ...
    def __init__(self, buffer: Any) -> None: ...
    lines: Any = ...
    lines_count: Any = ...
    first: bool = ...
    extra_lines: Any = ...
    def __iter__(self): ...
    def cur_line(self): ...
    def next(self): ...
    __next__: Any = ...
    def write_infos(self, modules: Any) -> None: ...
    def write(self, modules: Any, tnrs: Any, source: Any, trad: Any, comments: Optional[Any] = ...) -> None: ...

def trans_export(lang: Any, modules: Any, buffer: Any, format: Any, cr: Any) -> None: ...
def trans_parse_rml(de: Any): ...
def in_modules(object_name: Any, modules: Any): ...
def babel_extract_qweb(fileobj: Any, keywords: Any, comment_tags: Any, options: Any): ...
def trans_generate(lang: Any, modules: Any, cr: Any): ...
def trans_load(cr: Any, filename: Any, lang: Any, verbose: bool = ..., module_name: Optional[Any] = ..., context: Optional[Any] = ...): ...
def trans_load_data(cr: Any, fileobj: Any, fileformat: Any, lang: Any, lang_name: Optional[Any] = ..., verbose: bool = ..., module_name: Optional[Any] = ..., context: Optional[Any] = ...) -> None: ...
def get_locales(lang: Optional[Any] = ...) -> None: ...
def resetlocale(): ...
def load_language(cr: Any, lang: Any) -> None: ...