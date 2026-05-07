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
3. Si el input incluye una sección "---PREGUNTAS---", reformula también las
   preguntas para que el contexto sea coherente con el enunciado reformulado.
   Mantén la misma estructura: un ítem por línea con la misma etiqueta (a), b)…).
4. Mantén el mismo nivel académico y el idioma español de España.
5. Responde ÚNICAMENTE con el texto reformulado (con "---PREGUNTAS---" si lo
   había). Sin explicaciones, sin comillas adicionales, sin preamble.\
"""

_USER_TEMPLATE = """\
Reformula el siguiente enunciado cambiando el contexto aplicado. \
Mantén todas las expresiones matemáticas LaTeX idénticas.

{content}\
"""

_TASKS_SEPARATOR = "---PREGUNTAS---"


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
    """Return *variant* with varied surface prose (and sub-parts), or the original on failure.

    When rendered_sub_parts is non-empty the sub-questions are sent together
    with the main prose so the LLM can keep context consistent across both.
    Falls back to mechanical values silently on any error or bad output.
    """
    mechanical_prose = variant.rendered_prose_latex
    mechanical_tasks = variant.rendered_sub_parts
    if not mechanical_prose:
        return variant

    # Build combined input when sub-questions exist.
    if mechanical_tasks:
        tasks_block = "\n".join(
            f"{chr(ord('a') + i)}) {t}" for i, t in enumerate(mechanical_tasks)
        )
        content = f"{mechanical_prose}\n{_TASKS_SEPARATOR}\n{tasks_block}"
    else:
        content = mechanical_prose

    try:
        client = get_client()
        response = client.messages.create(
            model=settings.reword_model,
            max_tokens=1024,
            system=[
                {
                    "type": "text",
                    "text": _SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=[
                {
                    "role": "user",
                    "content": _USER_TEMPLATE.format(content=content),
                }
            ],
        )
        raw = response.content[0].text.strip()

        # Parse prose and (optionally) tasks from the response.
        if mechanical_tasks and _TASKS_SEPARATOR in raw:
            prose_part, tasks_part = raw.split(_TASKS_SEPARATOR, 1)
            reworded_prose = prose_part.strip()
            reworded_tasks = [
                re.sub(r"^[a-z]\)\s*", "", line.strip())
                for line in tasks_part.strip().splitlines()
                if line.strip()
            ]
            # If task count changed, the LLM mangled the structure — reject.
            if len(reworded_tasks) != len(mechanical_tasks):
                return variant
        elif not mechanical_tasks:
            reworded_prose = raw
            reworded_tasks = []
        else:
            # Expected separator not found — reject.
            return variant

        if not _math_preserved(mechanical_prose, reworded_prose):
            return variant
        if mechanical_tasks and not _math_preserved(
            " ".join(mechanical_tasks), " ".join(reworded_tasks)
        ):
            return variant

        return variant.model_copy(update={
            "rendered_prose_latex": reworded_prose,
            "rendered_sub_parts": reworded_tasks,
        })

    except Exception:
        return variant
