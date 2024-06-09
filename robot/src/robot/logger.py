from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table, Column
from rich.live import Live
from rich.text import Text
from rich import box

from robot.models.stats import Stats
from robot.models import Direction


MAX_LOG_LINES = 100

_log_lines = []

_layout = Layout(size=50)
_layout.split_row(
    Layout(name="level"),
    Layout(name="logs"),
)
_layout["level"].split_column(
    Layout(name="table"),
    Layout(name="stats", size=3),
)

_logs_panel = Panel("", subtitle="logs")
_level_panel = Panel("", subtitle="level layout")
_stats_panel = Panel("", subtitle="stats")

_layout["level"]["table"].update(_level_panel)
_layout["level"]["stats"].update(_stats_panel)
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
        return ":red_square-emoji:"
    if ch == "R":
        return str(direction)
    if ch == "-":
        return "[on green]:money_bag-emoji:[/]" # other options: beer, pizza, gem
    return ch


def display_level(level: list[list[str]], stats: Stats, direction: Direction):
    columns = [Column(min_width=2) for i in range(len(level[0]))]
    table = Table(*columns, show_lines=True, show_header=False, box=box.ROUNDED)

    for row in level:
        table.add_row(
            *(format_ch(ch, direction) for ch in row)
        )    

    _layout["level"]["table"].update(Panel(table, subtitle="level layout"))
    _layout["level"]["stats"].update(Panel(Text(str(stats)), subtitle="stats"))
