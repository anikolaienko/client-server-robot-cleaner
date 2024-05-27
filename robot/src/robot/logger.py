from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.live import Live

MAX_LOG_LINES = 100

_log_lines = []

_layout = Layout(size=50)
_layout.split_row(
    Layout(name="level"),
    Layout(name="logs"),
)

_level_table = Table(show_lines=True, show_header=False)

_logs_panel = Panel("", title="logs", subtitle="logs")
_level_panel = Panel(_level_table, title="level layout", subtitle="level layout")

_layout["level"].update(_level_panel)
_layout["logs"].update(_logs_panel)


def keep_alive() -> Live:
    return Live(_layout, refresh_per_second=5)


def _append_log(msg: str) -> str:
    global _log_lines
    _log_lines.append(f"- {msg}")

    if len(_log_lines) >= MAX_LOG_LINES:
        _log_lines = _log_lines[-MAX_LOG_LINES:]

    return "\n".join(reversed(_log_lines))


def log(msg: str):
    _logs_panel.renderable = _append_log(msg)
    _layout["logs"].update(_logs_panel)


def log_success(title: str, msg: str = ""):
    _logs_panel.renderable = _append_log(f"[green]{title}[/green]" + (f": {msg}" if msg else ""))
    _layout["logs"].update(_logs_panel)


def log_error(msg: str):
    _logs_panel.renderable = _append_log(f"[red]ERROR[/red]: {msg}")
    _layout["logs"].update(_logs_panel)

def log_warning(msg: str):
    _logs_panel.renderable = _append_log(f"[yellow]WARNING[/yellow]: {msg}")
    _layout["logs"].update(_logs_panel)

def format_ch(ch: str):
    if ch == "x":
        return "[white on red]X[/]"
    if ch == "R":
        return "[bold black on white]R[/]"
    if ch == "-":
        return "[white on green]-[/]"
    return ch

def display_level(level: list[list[str]]):
    table = Table(show_lines=True, show_header=False)

    for row in level:
        table.add_row(*(format_ch(x) for x in row))
    
    _layout["level"].update(table)
