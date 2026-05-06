"""Stage 1: convert a .docx file to a LaTeX string via pandoc."""

from pathlib import Path

import pypandoc


def docx_to_latex(path: Path) -> str:
    """Convert *path* (a .docx file) to a LaTeX string.

    Uses the system pandoc binary (installed in the container via apt).
    OMML equations in the docx are rendered as native LaTeX by pandoc.
    """
    return pypandoc.convert_file(str(path), "latex")
