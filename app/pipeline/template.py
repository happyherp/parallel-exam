r"""Stage 3: LLM-based template extraction (the hardest stage).

Given a Problem from the parser, ask Claude (Sonnet) to identify the
mathematical structure: function form, parameter constraints, invariants,
prose template with placeholders, and the original parameter values.

The LLM uses Anthropic's tool-use feature so the output is guaranteed to
match our schema. The system prompt is prompt-cached (≈2.5 KB of static
explanation + worked example) so repeated calls in the same session
amortise the token cost.

After the LLM returns, the extracted template is run through verify()
against the original parameters. If verification fails — i.e. SymPy says
the LLM's invariants do not hold for the source problem — the template
is rejected and the function returns None. Output is correct by
construction, never by hope.
"""

from __future__ import annotations

import logging
from typing import Any

from app.config import settings
from app.llm import get_client
from app.models import ParameterConstraint, Problem, Template
from app.pipeline.verify import verify

log = logging.getLogger(__name__)


# ── System prompt ─────────────────────────────────────────────────────────────

_SYSTEM_PROMPT = r"""Eres un asistente que extrae plantillas (templates) de problemas matemáticos para un generador de exámenes paralelos en español, nivel 1º Bachillerato.

ARQUITECTURA. Tú nunca calculas. Tu trabajo es identificar la ESTRUCTURA del problema. Un sistema en Python instanciará después la plantilla con nuevos parámetros, y SymPy verificará que tus invariantes se cumplen. Si fallan, tu plantilla será rechazada.

UNA TEMPLATE TIENE 6 CAMPOS

1. function_form: la función f(x) como expresión SymPy con parámetros simbólicos. Usa "x" como variable y letras minúsculas (a, b, c, ...) como parámetros.
   Ejemplo: "(a*x + b) / (x**2 + c)"

2. parameters: lista de restricciones, una por parámetro.
   Cada elemento: {"name": "a", "type": "int"|"rational"|"real", "sign": "positive"|"negative"|"any", "min": null|number, "max": null|number}.

3. invariants: propiedades matemáticas que cualquier variante DEBE cumplir.
   Cada invariante: {"description": "...", "sympy_expr": "...", "must_be": "integer"|"positive_integer"|"negative_integer"|"rational"}.
   El sympy_expr es código Python que se evalúa con estos nombres disponibles:
     - x       (símbolo SymPy)
     - f       (la función con los parámetros sustituidos)
     - solve, diff, sympify, integrate, limit, simplify, expand, factor
     - todo el módulo sympy (Symbol, Rational, Eq, …)
   Patrones útiles:
     - "f.subs(x, 0)"                                  → f(0)
     - "f.subs(x, 5)"                                  → f(5)
     - "solve(f.as_numer_denom()[0], x)[0]"            → raíz del numerador
     - "max(s for s in solve(diff(f, x), x) if s > 0)" → punto crítico positivo
     - "f.subs(x, max(s for s in solve(diff(f, x), x) if s > 0))" → valor de f en el pico

4. prose_template: el enunciado en español con marcadores. Sintaxis:
     - {{a}}  → se sustituye por el valor del parámetro a (idem b, c, …)
     - {{    → llave LaTeX literal {
     - }}    → llave LaTeX literal }
   Ejemplo: r"La función \(f(x) = \frac{{ {{a}}x + {{b}} }}{{x^2 + {{c}} }}\) ..."

5. student_tasks: lista de las sub-preguntas que el estudiante debe responder, ya generalizadas (sin números concretos).

6. original_parameters: el diccionario con los VALORES NUMÉRICOS exactos del problema original.
   Ejemplo: {"a": 80, "b": -160, "c": 5}
   CRÍTICO: el sistema verificará tus invariantes con estos valores. Si alguno falla, tu plantilla será rechazada.

EJEMPLO COMPLETO

Problema original:
"(3 puntos) La función f(x) = (80x − 160) / (x² + 5) indica las ganancias o pérdidas que una empresa ha tenido desde que fue constituida, expresada f(x) en miles de euros, x en años.
a) Estudia y representa gráficamente la función.
b) ¿Al cabo de cuánto tiempo obtiene la empresa una ganancia máxima? ¿Cuál es esa ganancia?
c) ¿Durante cuánto tiempo la empresa perdió dinero? ¿En qué momento perdió más?"

Plantilla extraída (llamada a la herramienta submit_template):
{
  "function_form": "(a*x + b) / (x**2 + c)",
  "parameters": [
    {"name": "a", "type": "int", "sign": "positive"},
    {"name": "b", "type": "int", "sign": "negative"},
    {"name": "c", "type": "int", "sign": "positive"}
  ],
  "invariants": [
    {"description": "f(0) es un entero negativo (pérdida inicial limpia)",
     "sympy_expr": "f.subs(x, 0)",
     "must_be": "negative_integer"},
    {"description": "raíz del numerador es entero positivo (año de equilibrio)",
     "sympy_expr": "solve(f.as_numer_denom()[0], x)[0]",
     "must_be": "positive_integer"},
    {"description": "f' tiene punto crítico positivo entero (año del pico)",
     "sympy_expr": "max(s for s in solve(diff(f, x), x) if s > 0)",
     "must_be": "positive_integer"},
    {"description": "f en el pico es entero positivo (ganancia máxima limpia)",
     "sympy_expr": "f.subs(x, max(s for s in solve(diff(f, x), x) if s > 0))",
     "must_be": "positive_integer"}
  ],
  "prose_template": "La función \\(f(x) = \\frac{{ {{a}}x + {{b}} }}{{x^2 + {{c}} }}\\) indica las ganancias o pérdidas que una empresa ha tenido desde que fue constituida, expresada \\(f(x)\\) en miles de euros, \\(x\\) en años.",
  "student_tasks": [
    "Estudia y representa gráficamente la función (ten en cuenta el contexto del problema).",
    "¿Al cabo de cuánto tiempo obtiene la empresa una ganancia máxima? ¿Cuál es esa ganancia?",
    "¿Durante cuánto tiempo la empresa perdió dinero? ¿En qué momento perdió más?"
  ],
  "original_parameters": {"a": 80, "b": -160, "c": 5}
}

REGLAS

- Identifica los parámetros que aparecen como números concretos en la función original. Esos son tus parameters.
- Los invariantes son las propiedades de "limpieza" del problema (resultados que tienen que ser enteros para que el ejercicio sea factible para un alumno).
- Si el problema no tiene una función matemática parametrizable (es puramente conceptual, una integral abstracta, una demostración, etc.), llama igualmente a submit_template pero deja parameters e invariants vacíos y original_parameters como objeto vacío. El sistema lo rechazará y se mostrará "sin plantilla disponible".
- Responde SIEMPRE llamando a la herramienta submit_template. No respondas en texto plano.
"""


# ── Tool schema ───────────────────────────────────────────────────────────────

_TEMPLATE_TOOL: dict[str, Any] = {
    "name": "submit_template",
    "description": (
        "Submit the extracted template for the given math problem. "
        "All fields are required."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "function_form": {
                "type": "string",
                "description": "SymPy-parseable expression for f(x). Use 'x' for the variable and a, b, c, ... for parameters.",
            },
            "parameters": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "type": {"enum": ["int", "rational", "real"]},
                        "sign": {"enum": ["positive", "negative", "any"]},
                        "min": {"type": ["number", "null"]},
                        "max": {"type": ["number", "null"]},
                    },
                    "required": ["name", "type", "sign"],
                },
            },
            "invariants": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "sympy_expr": {"type": "string"},
                        "must_be": {
                            "enum": [
                                "integer",
                                "positive_integer",
                                "negative_integer",
                                "rational",
                            ]
                        },
                    },
                    "required": ["description", "sympy_expr", "must_be"],
                },
            },
            "prose_template": {
                "type": "string",
                "description": "Spanish prose with {{a}}, {{b}}, ... placeholders and {{ / }} for literal LaTeX braces.",
            },
            "student_tasks": {
                "type": "array",
                "items": {"type": "string"},
            },
            "original_parameters": {
                "type": "object",
                "additionalProperties": {"type": "number"},
                "description": "The exact numerical parameter values from the source problem.",
            },
        },
        "required": [
            "function_form",
            "parameters",
            "invariants",
            "prose_template",
            "student_tasks",
            "original_parameters",
        ],
    },
}


# ── User message ──────────────────────────────────────────────────────────────

def _user_message(problem: Problem) -> str:
    pts = ""
    if problem.points is not None:
        p = int(problem.points) if problem.points == int(problem.points) else problem.points
        pts = f"({p} puntos) "

    parts = [f"{pts}{problem.prose_latex}"]
    parts.extend(problem.sub_parts)
    body = "\n".join(parts)

    return (
        "Extrae la plantilla del siguiente problema. Llama a submit_template "
        "con todos los campos.\n\n"
        f"Problema:\n{body}"
    )


# ── Public API ────────────────────────────────────────────────────────────────

def extract_template(problem: Problem) -> Template | None:
    """Extract a Template from *problem* via Claude, sanity-checked by SymPy.

    Returns None if:
      - ANTHROPIC_API_KEY is not configured
      - The LLM call fails (network, rate limit, malformed output)
      - The extracted invariants do not verify against the original parameters
    """
    try:
        client = get_client()
    except RuntimeError:
        log.info("extract_template: no API key configured, skipping LLM call")
        return None

    try:
        response = client.messages.create(
            model=settings.template_model,
            max_tokens=4096,
            system=[
                {
                    "type": "text",
                    "text": _SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=[{"role": "user", "content": _user_message(problem)}],
            tools=[_TEMPLATE_TOOL],
            tool_choice={"type": "tool", "name": "submit_template"},
        )
    except Exception as exc:
        log.warning("extract_template: LLM call failed: %s", exc)
        return None

    tool_input: dict[str, Any] | None = None
    for block in response.content:
        if getattr(block, "type", None) == "tool_use" and block.name == "submit_template":
            tool_input = dict(block.input)
            break

    if tool_input is None:
        log.warning("extract_template: model did not call submit_template")
        return None

    original_params = tool_input.pop("original_parameters", None)
    if not isinstance(original_params, dict) or not original_params:
        log.info("extract_template: no original_parameters provided — abstaining")
        return None

    try:
        template = Template(
            template_id=f"llm_extracted_p{problem.number}",
            **tool_input,
        )
    except Exception as exc:
        log.warning("extract_template: invalid Template payload: %s", exc)
        return None

    if not template.parameters or not template.invariants:
        log.info("extract_template: empty parameters/invariants — abstaining")
        return None

    # SymPy gate: the LLM's structure must be consistent with the original
    # numerical answer. If a single invariant fails on the source values,
    # the template is wrong (e.g. function_form misread, sympy_expr typo).
    try:
        check = verify(template, original_params)
    except Exception as exc:
        log.warning("extract_template: verify raised: %s", exc)
        return None

    if not check.verified:
        log.info(
            "extract_template: rejected — invariants do not hold on original "
            "parameters %s. Verification: %s",
            original_params,
            check.verification,
        )
        return None

    # Use the original numerical values to seed reasonable parameter bounds
    # so the generic brute-force sampler searches in a productive region of
    # the parameter space rather than the default [-30, 30] cube.
    template = template.model_copy(
        update={
            "parameters": [
                _bound_constraint(c, original_params.get(c.name))
                for c in template.parameters
            ]
        }
    )

    return template


def _bound_constraint(c: ParameterConstraint, original: float | None) -> ParameterConstraint:
    """Tighten a constraint's min/max around an observed original value.

    The LLM is not required to provide min/max — relying on the original
    parameter's order of magnitude is more reliable than asking the model
    to estimate ranges. The generic sampler then searches a 4×|original|
    window around 1, which captures most clean variants.
    """
    if original is None or (c.min is not None and c.max is not None):
        return c

    margin = max(abs(int(original)) * 4, 30)
    if c.sign == "positive":
        lo = 1 if c.min is None else int(c.min)
        hi = margin if c.max is None else int(c.max)
    elif c.sign == "negative":
        lo = -margin if c.min is None else int(c.min)
        hi = -1 if c.max is None else int(c.max)
    else:
        lo = -margin if c.min is None else int(c.min)
        hi = margin if c.max is None else int(c.max)

    return c.model_copy(update={"min": float(lo), "max": float(hi)})
