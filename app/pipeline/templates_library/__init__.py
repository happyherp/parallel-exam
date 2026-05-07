"""Template library registry.

Each entry is (Template, matcher_fn) where matcher_fn(prose_latex) -> bool.
_find_template in main.py iterates this list and returns the first match.
To add a template: create a new module, import it here, append to LIBRARY.
"""

from __future__ import annotations

from typing import Callable

from app.models import Template
from app.pipeline.templates_library import rational_business_profit

LIBRARY: list[tuple[Template, Callable[[str], bool]]] = [
    (
        rational_business_profit.RATIONAL_BUSINESS_PROFIT,
        rational_business_profit.matches,
    ),
]
