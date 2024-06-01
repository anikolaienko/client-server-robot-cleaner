from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.live import Live

from robot.models.types import Direction
from robot.algos.directions import DIRECTION_TO_CHAR


MAX_LOG_LINES = 100

_log_lines = []

_layout = Layout(size=50)
_layout.split_row(
    Layout(name="level"),
    Layout(name="logs"),
)


_logs_panel = Panel("", title="logs", subtitle="logs")
_level_panel = Panel("", title="level layout", subtitle="level layout")

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

def format_ch(ch: str, direction: Direction):
    if ch == "x":
        return "[on red]X[/]"
    if ch == "R":
        ch = DIRECTION_TO_CHAR[direction]
        return f"[bold on black]{ch}[/]"
    if ch == "-":
        return "[on green]-[/]"
    return ch

def display_level(level: list[list[str]], direction: Direction):
    table = Table(show_lines=True, show_header=False)

    for row in level:
        table.add_row(
            *(format_ch(ch, direction) for ch in row)
        )
    
    _layout["level"].update(Panel(table, title="level layout", subtitle="level layout"))
