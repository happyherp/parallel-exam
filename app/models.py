"""Core data models. These shapes are the contract between pipeline stages."""

from typing import Literal
from pydantic import BaseModel, Field


class Problem(BaseModel):
    """A single problem extracted from an input exam."""

    number: int                      # 1, 2, 3...
    points: float | None             # 3.0 puntos, etc.
    prose_latex: str                 # the problem statement, with \(...\) for inline math
    sub_parts: list[str] = []        # ["a) ...", "b) ...", ...] if multi-part


class ParameterConstraint(BaseModel):
    """A constraint on a single parameter in a Template."""

    name: str                        # "a", "b", "c"
    type: Literal["int", "rational", "real"]
    sign: Literal["positive", "negative", "any"] = "any"
    min: float | None = None
    max: float | None = None


class Invariant(BaseModel):
    """A property that any valid variant must satisfy.

    Expressed as a SymPy expression that should evaluate to a clean integer
    or rational. The verifier substitutes the candidate parameters and checks.
    """

    description: str                 # human-readable: "f(0) is a clean integer"
    sympy_expr: str                  # "f.subs(x, 0)"  — evaluated against the variant
    must_be: Literal["integer", "positive_integer", "negative_integer", "rational"]


class Template(BaseModel):
    """The structural skeleton of a problem, abstracted from a specific instance.

    This is the central object of the system. The LLM extracts these from
    problems; the constraint solver instantiates them; the verifier validates them.
    """

    template_id: str                 # e.g. "rational_business_profit_v1"
    function_form: str               # SymPy-parseable: "(a*x + b) / (x**2 + c)"
    parameters: list[ParameterConstraint]
    invariants: list[Invariant]
    prose_template: str              # Jinja-style with {{a}}, {{b}}, {{c}} placeholders
    student_tasks: list[str]         # the sub-questions, language-agnostic placeholders


class Variant(BaseModel):
    """A concrete generated variant: parameters chosen, prose rendered, math verified."""

    template_id: str
    parameters: dict[str, int | float]
    rendered_prose_latex: str
    verification: dict[str, str]     # invariant name → computed value as string
    verified: bool
