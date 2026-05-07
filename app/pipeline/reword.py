r"""Stage 6: vary the surface text of a variant while preserving all math.

Architecture rule: the LLM is allowed to touch words, not numbers.
After the LLM returns, _math_preserved() verifies that every LaTeX math
block (\(...\) and \[...\]) from the mechanically-rendered prose is present
verbatim in the LLM output.  If any block is missing or altered, the LLM
output is rejected and the mechanical prose is kept.

The LLM also receives a prompt-cached system message so repeated calls
within the same process share the cached prefix and reduce token costs.
"""

from __future__ import annotations

import re

from app.config import settings
from app.llm import get_client
from app.models import Template, Variant

# ── Prompts ───────────────────────────────────────────────────────────────────

_SYSTEM_PROMPT = """\
Eres un experto en didáctica de matemáticas para Bachillerato en España.
Tu única tarea es reformular el enunciado de un problema de matemáticas
cambiando el contexto aplicado (p.ej. empresa → fábrica, beneficios →
producción, euros → toneladas, años → meses) sin modificar en absoluto las
expresiones matemáticas.

REGLAS OBLIGATORIAS:
1. Copia EXACTAMENTE todos los fragmentos LaTeX tal y como aparecen,
   incluyendo los delimitadores \\( y \\). No cambies ningún número ni
   símbolo matemático dentro de ellos.
2. Cambia únicamente las palabras que describen el contexto real (la empresa,
   los beneficios, la unidad de tiempo, etc.). Usa un contexto diferente al
   original (no vuelvas a usar "empresa" ni "beneficios").
3. Mantén el mismo nivel académico y el idioma español de España.
4. Responde ÚNICAMENTE con el texto reformulado. Sin explicaciones, sin
   comillas adicionales, sin preamble.\
"""

_USER_TEMPLATE = """\
Reformula el siguiente enunciado cambiando el contexto aplicado. \
Mantén todas las expresiones matemáticas LaTeX idénticas.

{prose}\
"""


# ── Math preservation check ───────────────────────────────────────────────────

_MATH_RE = re.compile(r"\\\(.*?\\\)|\\\[.*?\\\]", re.DOTALL)


def _extract_math(text: str) -> list[str]:
    """Return all \\(...\\) and \\[...\\] blocks, whitespace-normalised."""
    return sorted(re.sub(r"\s+", " ", m) for m in _MATH_RE.findall(text))


def _math_preserved(original: str, reworded: str) -> bool:
    """True iff every math block from *original* appears unchanged in *reworded*."""
    return _extract_math(original) == _extract_math(reworded)


# ── Public API ────────────────────────────────────────────────────────────────

def reword_surface(
    variant: Variant,
    template: Template,  # noqa: ARG001 — reserved for future per-template hints
    language: str = "es",  # noqa: ARG001 — reserved for multi-language support
) -> Variant:
    """Return *variant* with varied surface prose, or the original on any failure.

    Calls the Anthropic API. Falls back to mechanical prose silently so the
    pipeline is never blocked by an LLM error or missing API key.
    """
    mechanical_prose = variant.rendered_prose_latex
    if not mechanical_prose:
        return variant

    try:
        client = get_client()
        response = client.messages.create(
            model=settings.reword_model,
            max_tokens=1024,
            system=[
                {
                    "type": "text",
                    "text": _SYSTEM_PROMPT,
                    # Cache the static system prompt across repeated calls.
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=[
                {
                    "role": "user",
                    "content": _USER_TEMPLATE.format(prose=mechanical_prose),
                }
            ],
        )
        reworded = response.content[0].text.strip()

        if not _math_preserved(mechanical_prose, reworded):
            # LLM modified a math expression — reject to preserve correctness.
            return variant

        return variant.model_copy(update={"rendered_prose_latex": reworded})

    except Exception:
        # Missing API key, network error, rate limit, etc. — degrade gracefully.
        return variant
