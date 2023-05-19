from itertools import chain as chain
from socket import socket as socket_
from threading import Semaphore, Thread
from typing import Any, Callable, Literal, TypeVar

import werkzeug.serving
from gevent.pywsgi import WSGIServer
from inotify.adapters import InotifyTrees
from psutil import Process
from watchdog.observers import Observer

from ..modules.registry import Registry
from ..sql_db import Cursor

_WorkerT = TypeVar("_WorkerT", bound=Worker)

INOTIFY_LISTEN_EVENTS: Any
SLEEP_INTERVAL: int

def memory_info(process: Process): ...
def set_limit_memory_hard() -> None: ...
def empty_pipe(fd: int) -> None: ...

class LoggingBaseWSGIServerMixIn:
    def handle_error(self, request, client_address) -> None: ...

class BaseWSGIServerNoBind(LoggingBaseWSGIServerMixIn, werkzeug.serving.BaseWSGIServer):
    def __init__(self, app) -> None: ...
    def server_activate(self) -> None: ...

class RequestHandler(werkzeug.serving.WSGIRequestHandler):
    def setup(self) -> None: ...
    protocol_version: str
    def make_environ(self) -> dict[str, Any]: ...
    close_connection: bool
    def send_header(self, keyword, value) -> None: ...

class ThreadedWSGIServerReloadable(
    LoggingBaseWSGIServerMixIn, werkzeug.serving.ThreadedWSGIServer
):
    max_http_threads: Any
    http_threads_sem: Semaphore
    daemon_threads: bool
    def __init__(self, host: str, port: int, app) -> None: ...
    reload_socket: bool
    socket: socket_
    def server_bind(self) -> None: ...
    def server_activate(self) -> None: ...
    def process_request(self, request, client_address) -> None: ...
    def shutdown_request(self, request) -> None: ...

class FSWatcherBase:
    def handle_file(self, path: str) -> Literal[True]: ...

class FSWatcherWatchdog(FSWatcherBase):
    observer: Observer
    def __init__(self) -> None: ...
    def dispatch(self, event) -> None: ...
    def start(self) -> None: ...
    def stop(self) -> None: ...

class FSWatcherInotify(FSWatcherBase):
    started: bool
    watcher: InotifyTrees
    def __init__(self) -> None: ...
    def run(self) -> None: ...
    thread: Thread
    def start(self) -> None: ...
    def stop(self) -> None: ...

class CommonServer:
    app: Any
    interface: str
    port: int
    pid: int
    def __init__(self, app) -> None: ...
    def close_socket(self, sock: socket_) -> None: ...
    @classmethod
    def on_stop(cls, func: Callable) -> None: ...
    def stop(self) -> None: ...

class ThreadedServer(CommonServer):
    main_thread_id: int | None
    quit_signals_received: int
    httpd: ThreadedWSGIServerReloadable | None
    limits_reached_threads: set[Thread]
    limit_reached_time: float | None
    def __init__(self, app) -> None: ...
    def signal_handler(self, sig, frame) -> None: ...
    def process_limit(self) -> None: ...
    def cron_thread(self, number) -> None: ...
    def cron_spawn(self) -> None: ...
    def http_thread(self) -> None: ...
    def http_spawn(self) -> None: ...
    def start(self, stop: bool = ...): ...
    def stop(self) -> None: ...
    def run(self, preload: Any | None = ..., stop: bool = ...): ...
    def reload(self) -> None: ...

class GeventServer(CommonServer):
    port: int
    httpd: WSGIServer | None
    def __init__(self, app) -> None: ...
    def process_limits(self) -> None: ...
    ppid: int
    def watchdog(self, beat: int = ...) -> None: ...
    client_address: Any
    response_use_chunked: bool
    def start(self): ...
    def stop(self) -> None: ...
    def run(self, preload, stop: bool) -> None: ...

class PreforkServer(CommonServer):
    population: int
    timeout: int
    limit_request: int
    cron_timeout: int
    beat: int
    socket: socket_ | None
    workers_http: dict[int, WorkerHTTP]
    workers_cron: dict[int, WorkerCron]
    workers: dict[int, Worker]
    generation: int
    queue: list
    long_polling_pid: int | None
    def __init__(self, app) -> None: ...
    def pipe_new(self) -> tuple[int, int]: ...
    def pipe_ping(self, pipe: tuple[int, int]) -> None: ...
    def signal_handler(self, sig: int, frame) -> None: ...
    def worker_spawn(
        self, klass: Callable[..., _WorkerT], workers_registry: dict[int, _WorkerT]
    ) -> _WorkerT | None: ...
    def long_polling_spawn(self) -> None: ...
    def worker_pop(self, pid: int) -> None: ...
    def worker_kill(self, pid: int, sig: int) -> None: ...
    def process_signals(self) -> None: ...
    def process_zombie(self) -> None: ...
    def process_timeout(self) -> None: ...
    def process_spawn(self) -> None: ...
    def sleep(self) -> None: ...
    pipe: tuple[int, int]
    def start(self) -> None: ...
    def stop(self, graceful: bool = ...) -> None: ...
    def run(self, preload, stop: bool): ...

class Worker:
    multi: PreforkServer
    watchdog_time: float
    watchdog_pipe: tuple[int, int]
    eintr_pipe: tuple[int, int]
    watchdog_timeout: Any
    ppid: int
    pid: int | None
    alive: bool
    request_max: Any
    request_count: int
    def __init__(self, multi: PreforkServer) -> None: ...
    def setproctitle(self, title: str = ...) -> None: ...
    def close(self) -> None: ...
    def signal_handler(self, sig: int, frame) -> None: ...
    def signal_time_expired_handler(self, n, stack) -> None: ...
    def sleep(self) -> None: ...
    def check_limits(self) -> None: ...
    def process_work(self) -> None: ...
    def start(self) -> None: ...
    def stop(self) -> None: ...
    def run(self) -> None: ...

class WorkerHTTP(Worker):
    sock_timeout: float
    def __init__(self, multi: PreforkServer) -> None: ...
    def process_request(self, client: socket_, addr) -> None: ...
    def process_work(self) -> None: ...
    server: BaseWSGIServerNoBind
    def start(self) -> None: ...

class WorkerCron(Worker):
    db_index: int
    watchdog_timeout: int
    def __init__(self, multi: PreforkServer) -> None: ...
    def sleep(self) -> None: ...
    def process_work(self) -> None: ...
    dbcursor: Cursor
    def start(self) -> None: ...
    def stop(self) -> None: ...

server: CommonServer | None

def load_server_wide_modules() -> None: ...
def load_test_file_py(registry: Registry, test_file: str) -> None: ...
def preload_registries(dbnames: list[str] | None): ...
def start(preload: list[str] | None = ..., stop: bool = ...): ...
def restart() -> None: ...
