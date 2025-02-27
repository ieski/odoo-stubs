from types import CodeType
from typing import Any, Iterable, Iterator, Literal

from opcode import HAVE_ARGUMENT as HAVE_ARGUMENT

unsafe_eval = eval

def to_opcodes(
    opnames: Iterable[str], _opmap: dict[str, int] = ...
) -> Iterator[int]: ...
def assert_no_dunder_name(code_obj: CodeType, expr: str) -> None: ...
def assert_valid_codeobj(
    allowed_codes: set[int], code_obj: CodeType, expr: str
) -> None: ...
def test_expr(expr: str, allowed_codes: set[int], mode: str = ...): ...
def const_eval(expr: str): ...
def expr_eval(expr: str): ...
def safe_eval(
    expr: str,
    globals_dict: dict | None = ...,
    locals_dict: dict | None = ...,
    mode: str = ...,
    nocopy: bool = ...,
    locals_builtins: bool = ...,
): ...
def test_python_expr(expr: str, mode: str = ...) -> str | Literal[False]: ...
def check_values(d: dict): ...

class wrap_module:
    def __init__(self, module, attributes) -> None: ...
    def __getattr__(self, item): ...

mods: list[str]
datetime: wrap_module
json: wrap_module
time: wrap_module
pytz: wrap_module
