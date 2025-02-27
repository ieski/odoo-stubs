import logging.handlers
from logging import Logger, LogRecord

def log(
    logger: Logger, level: int, prefix: str, msg, depth: int | None = ...
) -> None: ...

class PostgreSQLHandler(logging.Handler):
    def emit(self, record: LogRecord) -> None: ...

BLACK: int
RED: int
GREEN: int
YELLOW: int
BLUE: int
MAGENTA: int
CYAN: int
WHITE: int
DEFAULT: int
RESET_SEQ: str
COLOR_SEQ: str
BOLD_SEQ: str
COLOR_PATTERN: str
LEVEL_COLOR_MAPPING: dict[int, tuple[int, int]]

class PerfFilter(logging.Filter):
    def format_perf(
        self, query_count: int, query_time: float, remaining_time: float
    ): ...
    def filter(self, record: LogRecord): ...

class ColoredPerfFilter(PerfFilter):
    def format_perf(
        self, query_count: int, query_time: float, remaining_time: float
    ): ...

class DBFormatter(logging.Formatter):
    def format(self, record: LogRecord): ...

class ColoredFormatter(DBFormatter):
    def format(self, record: LogRecord): ...

def init_logger(): ...

DEFAULT_LOG_CONFIGURATION: list[str]
PSEUDOCONFIG_MAPPER: dict[str, list[str]]

def runbot(self, message, *args, **kws) -> None: ...
