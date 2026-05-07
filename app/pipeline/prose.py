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


def render_prose(variant: Variant, template: Template) -> Variant:
    """Return a copy of *variant* with rendered_prose_latex filled in."""
    prose = template.prose_template
    params = variant.parameters

    def _replace(m: re.Match) -> str:
        name = m.group(1)
        if name not in params:
            return m.group(0)
        val = params[name]
        # Emit an integer string when the value is a whole number.
        if isinstance(val, float) and val == int(val):
            val = int(val)
        return str(val)

    # Step 1: replace {{param_name}} with the parameter value.
    prose = re.sub(r"\{\{(\w+)\}\}", _replace, prose)

    # Step 2: unescape remaining {{ / }} → { / }.
    prose = prose.replace("{{", "{").replace("}}", "}")

    # Step 3: clean up sign artifacts from negative substitutions.
    prose = prose.replace("+ -", "- ").replace("- -", "+ ")

    return variant.model_copy(update={"rendered_prose_latex": prose})
