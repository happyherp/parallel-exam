"""Stage 4: verify that a parameter set satisfies a Template's invariants.

The invariant expressions are evaluated against a SymPy function built by
substituting concrete parameter values into the template's function_form.
All math is done by SymPy; the LLM is never involved here.
"""

from __future__ import annotations

import sympy
from sympy import diff, solve, symbols, sympify

from app.models import Template, Variant


def verify(template: Template, params: dict[str, int | float]) -> Variant:
    """Substitute *params* into *template* and evaluate every invariant.

    Returns a Variant with ``verified=True`` only when every invariant
    passes its ``must_be`` condition.  Failed or erroring invariants are
    recorded in ``verification`` as explanatory strings.
    """
    x = symbols("x")

    # Build the concrete function by substituting integer/float params.
    param_subs = {symbols(k): sympify(v) for k, v in params.items()}
    f = sympify(template.function_form).subs(param_subs)

    # Evaluation namespace for invariant expressions.
    ns: dict = {name: getattr(sympy, name) for name in dir(sympy) if not name.startswith("_")}
    ns.update({"x": x, "f": f, "diff": diff, "solve": solve, "__builtins__": __builtins__})

    verification: dict[str, str] = {}
    all_pass = True

    for inv in template.invariants:
        try:
            raw = eval(inv.sympy_expr, ns)  # noqa: S307
            result = sympify(raw)
            verification[inv.description] = str(result)

            ok = _check_must_be(result, inv.must_be)
        except Exception as exc:
            verification[inv.description] = f"ERROR: {exc}"
            ok = False

        if not ok:
            all_pass = False

    return Variant(
        template_id=template.template_id,
        parameters=params,
        rendered_prose_latex="",
        verification=verification,
        verified=all_pass,
    )


def _check_must_be(result: sympy.Basic, must_be: str) -> bool:
    try:
        if must_be == "integer":
            return bool(result.is_integer)
        if must_be == "positive_integer":
            return bool(result.is_integer and result > 0)
        if must_be == "negative_integer":
            return bool(result.is_integer and result < 0)
        if must_be == "rational":
            return bool(result.is_rational)
        return False
    except Exception:
        return False
