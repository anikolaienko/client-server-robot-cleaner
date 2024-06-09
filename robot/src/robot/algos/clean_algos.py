from .clean_blind_with_layout import clean_level as blind_with_layout
from .clean_blind_with_trace import clean_level as blind_with_trace
from .clean_level_aware import clean_level as level_aware

ALGOS = {
    "blind_with_layout": blind_with_layout,
    "blind_with_trace": blind_with_trace,
    "level_aware": level_aware
}
