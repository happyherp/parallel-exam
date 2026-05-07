"""Render a Template's prose_template with concrete parameter values.

The prose_template field uses a two-level escaping convention:
  - {{param_name}}  →  value of that parameter (e.g. {{a}} → 70)
  - {{            →  literal {  (LaTeX brace)
  - }}            →  literal }  (LaTeX brace)

This mirrors Python str.format escaping but uses double-brace variable
delimiters so that LaTeX braces are written as {{ and }} while parameter
placeholders are written as {{name}}.

After substitution a simple cleanup pass fixes sign artifacts that arise
when a parameter is negative (e.g. "70x + -210" → "70x - 210").
"""

from __future__ import annotations

import re

from app.models import Template, Variant


def _substitute(text: str, params: dict) -> str:
    """Replace {{param}} placeholders, unescape {{ / }}, fix sign artifacts."""
    def _replace(m: re.Match) -> str:
        name = m.group(1)
        if name not in params:
            return m.group(0)
        val = params[name]
        if isinstance(val, float) and val == int(val):
            val = int(val)
        return str(val)

    text = re.sub(r"\{\{(\w+)\}\}", _replace, text)
    text = text.replace("{{", "{").replace("}}", "}")
    text = text.replace("+ -", "- ").replace("- -", "+ ")
    return text


def render_prose(variant: Variant, template: Template) -> Variant:
    """Return a copy of *variant* with rendered_prose_latex and rendered_sub_parts filled in."""
    params = variant.parameters
    prose = _substitute(template.prose_template, params)
    sub_parts = [_substitute(task, params) for task in template.student_tasks]
    return variant.model_copy(update={
        "rendered_prose_latex": prose,
        "rendered_sub_parts": sub_parts,
    })
