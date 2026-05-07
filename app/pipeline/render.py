r"""Stage 7: render approved variants to a .docx output file.

Uses pandoc (LaTeX → docx) so OMML equation generation comes for free —
pandoc knows how to turn \(...\) and \[...\] into Word's native equation
objects, the same approach as the input pipeline but in reverse.

The function constructs a minimal valid LaTeX document, writes it to a
temp .tex file, calls pandoc, and writes the output to *output_path*.
All temp files are cleaned up; the caller owns *output_path*.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pypandoc

from app.models import Problem, Template, Variant


# ── LaTeX helpers ─────────────────────────────────────────────────────────────

_PREAMBLE = r"""\documentclass[12pt,a4paper]{article}
\usepackage{amsmath}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[spanish]{babel}
\begin{document}
\begin{enumerate}
"""

_POSTAMBLE = r"""
\end{enumerate}
\end{document}
"""


def _escape(text: str) -> str:
    """Minimal escaping for plain Spanish text passed into a LaTeX document."""
    return text.replace("%", r"\%").replace("$", r"\$").replace("&", r"\&")


def _build_latex(
    problems: list[Problem],
    templates: dict[int, Template | None],
    variants: dict[int, Variant | None],
) -> str:
    """Return a complete LaTeX document combining variants and originals."""
    parts: list[str] = [_PREAMBLE]

    for i, problem in enumerate(problems):
        tmpl = templates.get(i)
        var = variants.get(i)

        pts = ""
        if problem.points is not None:
            p = int(problem.points) if problem.points == int(problem.points) else problem.points
            pts = f"({p} {'punto' if p == 1 else 'puntos'}) "

        parts.append(r"\item " + pts)

        if var and var.verified and var.rendered_prose_latex:
            # Use the generated, reworded variant prose.
            parts.append(var.rendered_prose_latex)
            parts.append("")

            sub_parts = var.rendered_sub_parts or (tmpl.student_tasks if tmpl else [])
            for j, task in enumerate(sub_parts):
                label = chr(ord("a") + j)
                parts.append(f"{label}) {_escape(task)}")
                parts.append("")
        else:
            # No variant — pass the original problem through unchanged.
            parts.append(problem.prose_latex)
            parts.append("")

            for part in problem.sub_parts:
                parts.append(_escape(part))
                parts.append("")

    parts.append(_POSTAMBLE)
    return "\n".join(parts)


# ── Public API ────────────────────────────────────────────────────────────────

def variants_to_docx(
    problems: list[Problem],
    templates: dict[int, Template | None],
    variants: dict[int, Variant | None],
    output_path: Path,
) -> None:
    """Write a .docx exam to *output_path* combining variants and originals.

    Raises RuntimeError if pandoc is not available.
    Raises OSError if the output file cannot be written.
    """
    latex = _build_latex(problems, templates, variants)

    with tempfile.NamedTemporaryFile(suffix=".tex", mode="w", encoding="utf-8", delete=False) as fh:
        fh.write(latex)
        tex_path = Path(fh.name)

    try:
        pypandoc.convert_file(
            str(tex_path),
            "docx",
            outputfile=str(output_path),
            extra_args=["--standalone"],
        )
    finally:
        tex_path.unlink(missing_ok=True)
