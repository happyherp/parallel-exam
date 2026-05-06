"""Stage 2: parse a pandoc-generated LaTeX string into Problem objects.

Pandoc's LaTeX output for a numbered-list docx uses this structure:

    \\begin{enumerate}
    \\def\\labelenumi{...}
    [\\setcounter{enumi}{N}]    <- present when restarting from N+1
    \\item
      \\emph{\\textbf{(X puntos)}} Prose text ...
    [\\item ...]
    \\end{enumerate}

    a) Sub-part text ...        <- free paragraphs between enumerate blocks
    b) ...

Multiple enumerate blocks appear in sequence; setcounter tells us which
problem number the next \\item represents.  Sub-parts appear as free text
after the block that owns them (i.e. they belong to the last item in the
preceding block).
"""

from __future__ import annotations

import re

from app.models import Problem


# ── helpers ──────────────────────────────────────────────────────────────────

_POINTS_RE = re.compile(
    r"\\emph\{\\textbf\{\((\d+(?:[.,]\d+)?)\s*punt[oa]s?\)\}\}",
    re.IGNORECASE,
)
_SETCOUNTER_RE = re.compile(r"\\setcounter\{enumi\}\{(\d+)\}")
_SUBPART_RE = re.compile(r"(?m)^([a-z]\))\s*")


def _clean_item_prose(text: str) -> str:
    """Remove LaTeX bookkeeping directives from an \\item body."""
    text = re.sub(r"\\def\\labelenumi\{[^}]*\}", "", text)
    text = re.sub(r"\\setcounter\{[^}]*\}\{[^}]*\}", "", text)
    # Remove the points annotation itself (already captured separately).
    text = _POINTS_RE.sub("", text)
    return text.strip()


def _extract_points(text: str) -> float | None:
    m = _POINTS_RE.search(text)
    if not m:
        return None
    return float(m.group(1).replace(",", "."))


def _parse_subparts(text: str) -> list[str]:
    """Split free-text block into labelled sub-parts (a), b), …).

    Lines/paragraphs that are not labelled are prepended to the next
    labelled part, or returned as an unlabelled part-0 if nothing follows.
    """
    # Split on the letter-) pattern at the start of a paragraph.
    parts = _SUBPART_RE.split(text.strip())
    # parts = [preamble, "a)", body_a, "b)", body_b, ...]
    result: list[str] = []
    preamble = parts[0].strip()
    i = 1
    while i < len(parts):
        label = parts[i]        # e.g. "a)"
        body = parts[i + 1].strip() if i + 1 < len(parts) else ""
        result.append(f"{label} {body}")
        i += 2
    # If there were image-only sub-parts before the first label, surface them.
    if preamble and not result:
        result.append(preamble)
    return result


# ── public API ────────────────────────────────────────────────────────────────

def latex_to_problems(latex: str) -> list[Problem]:
    """Parse pandoc LaTeX output into a list of Problem objects."""
    problems: list[Problem] = []

    enum_re = re.compile(
        r"\\begin\{enumerate\}(.*?)\\end\{enumerate\}",
        re.DOTALL,
    )

    # Walk the document as alternating (free_text, enum_block) segments.
    pos = 0
    for match in enum_re.finditer(latex):
        free_text = latex[pos : match.start()].strip()
        if free_text and problems:
            subparts = _parse_subparts(free_text)
            if subparts:
                problems[-1] = problems[-1].model_copy(
                    update={"sub_parts": subparts}
                )

        _parse_enum_block(match.group(1), problems)
        pos = match.end()

    # Trailing free text after the last enumerate block.
    trailing = latex[pos:].strip()
    if trailing and problems:
        subparts = _parse_subparts(trailing)
        if subparts:
            problems[-1] = problems[-1].model_copy(
                update={"sub_parts": subparts}
            )

    return problems


def _parse_enum_block(block: str, problems: list[Problem]) -> None:
    """Append Problem objects found in one enumerate block to *problems*."""
    setcounter_m = _SETCOUNTER_RE.search(block)
    next_number = int(setcounter_m.group(1)) + 1 if setcounter_m else (
        problems[-1].number + 1 if problems else 1
    )

    # Split on \item; first segment is preamble (\def, \setcounter, etc.)
    raw_items = re.split(r"\\item", block)
    for raw in raw_items[1:]:
        points = _extract_points(raw)
        prose = _clean_item_prose(raw)
        problems.append(
            Problem(
                number=next_number,
                points=points,
                prose_latex=prose,
                sub_parts=[],
            )
        )
        next_number += 1
