"""Stage 2: parse a pandoc-generated LaTeX string into Problem objects.

Two document styles are supported:

Style A — numbered enumerate (derivadas2 style):
    \\begin{enumerate}
    \\def\\labelenumi{...}
    [\\setcounter{enumi}{N}]
    \\item
      \\emph{\\textbf{(X puntos)}} Prose text ...
    \\end{enumerate}
    a) Sub-part ...   <- free paragraphs after the block

Style B — textbf heading (analisis 1º Bach style):
    \\textbf{Problema N.} (X puntos) Prose text ...

    [\\begin{enumerate}...\\end{enumerate}  OR  a) ... b) ...]

    \\textbf{Problema N+1.} ...

Detection: if the document contains \\textbf{Problema, Style B is used.
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

# Style-B patterns (split on the full \textbf{Problema N.} token including closing brace)
_PROBLEMA_HEADING_RE = re.compile(r"\\textbf\{Problema\s+(\d+)\.\}")
_HEADING_POINTS_RE = re.compile(
    r"^\s*\((\d+(?:[.,]\d+)?)\s*punt[oa]s?\)",
    re.IGNORECASE,
)
_SUBPART_POINTS_RE = re.compile(
    r"\(\d+(?:[.,]\d+)?\s*punt[oa]s?\)\s*",
    re.IGNORECASE,
)


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
    """Parse pandoc LaTeX output into a list of Problem objects.

    Dispatches to the appropriate parser based on detected document style.
    """
    if _PROBLEMA_HEADING_RE.search(latex):
        return _parse_style_b(latex)
    return _parse_style_a(latex)


def _parse_style_a(latex: str) -> list[Problem]:
    """Style A: problems are \\item entries inside \\begin{enumerate} blocks."""
    problems: list[Problem] = []

    enum_re = re.compile(
        r"\\begin\{enumerate\}(.*?)\\end\{enumerate\}",
        re.DOTALL,
    )

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

    trailing = latex[pos:].strip()
    if trailing and problems:
        subparts = _parse_subparts(trailing)
        if subparts:
            problems[-1] = problems[-1].model_copy(
                update={"sub_parts": subparts}
            )

    return problems


def _parse_style_b(latex: str) -> list[Problem]:
    """Style B: problems start with \\textbf{Problema N.} (X puntos) headings."""
    problems: list[Problem] = []

    # Split into segments, one per problem (keep the heading delimiter).
    segments = _PROBLEMA_HEADING_RE.split(latex)
    # segments = [preamble, "1", body1, "2", body2, ...]
    i = 1
    while i < len(segments):
        number = int(segments[i])
        body = segments[i + 1] if i + 1 < len(segments) else ""
        i += 2

        # After split, body starts with " (X puntos) prose..."
        m_pts = _HEADING_POINTS_RE.match(body)
        points = float(m_pts.group(1).replace(",", ".")) if m_pts else None

        # Strip the points annotation to get pure prose.
        prose = _HEADING_POINTS_RE.sub("", body, count=1).strip() if m_pts else body.strip()

        # Separate inline enumerate block (if present) from trailing free text.
        enum_re = re.compile(
            r"\\begin\{enumerate\}(.*?)\\end\{enumerate\}",
            re.DOTALL,
        )
        sub_parts: list[str] = []
        enum_match = enum_re.search(prose)
        if enum_match:
            # Sub-parts are the \item entries inside the enumerate.
            enum_body = enum_match.group(1)
            raw_items = re.split(r"\\item", enum_body)
            for raw in raw_items[1:]:
                item_text = re.sub(r"\\def\\labelenumi\{[^}]*\}", "", raw)
                item_text = re.sub(r"\\setcounter\{[^}]*\}\{[^}]*\}", "", item_text)
                sub_parts.append(item_text.strip())
            # Prose is everything before the enumerate block.
            prose = prose[: enum_match.start()].strip()
        else:
            # Sub-parts may be free a) b) paragraphs; strip them from prose.
            parts = _SUBPART_RE.split(prose.strip())
            if len(parts) > 1:
                prose = parts[0].strip()
                j = 1
                while j < len(parts):
                    label = parts[j]
                    body_part = parts[j + 1].strip() if j + 1 < len(parts) else ""
                    sub_parts.append(f"{label} {body_part}")
                    j += 2

        problems.append(
            Problem(
                number=number,
                points=points,
                prose_latex=prose.strip(),
                sub_parts=sub_parts,
            )
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
