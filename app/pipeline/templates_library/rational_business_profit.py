"""Hand-written Template for the rational-business-profit problem type.

Original instance (derivadas2.docx, Problem 1):
    f(x) = (80x - 160) / (x² + 5)
    a=80, b=-160, c=5  →  break-even=2, peak=5, max_profit=8, f(0)=-32

Parameterisation:
    Given (k, p, n) where k=break-even year, p=peak year, n=scaling factor:
        a = 2 * p * n
        b = -k * a          (so ax+b = 0 ↔ x = k)
        c = p * (p - 2*k)   (so f'(x) = 0 at x = p; requires p > 2k for c > 0)

    Derived clean values:
        f(0)   = b/c = -2kn/(p-2k)     [integer when (p-2k) | 2kn]
        break-even  = k
        peak year   = p
        max profit  = f(p) = a/(2p) = n
"""

from app.models import Invariant, ParameterConstraint, Template

RATIONAL_BUSINESS_PROFIT = Template(
    template_id="rational_business_profit_v1",
    function_form="(a*x + b) / (x**2 + c)",
    parameters=[
        ParameterConstraint(name="a", type="int", sign="positive"),
        ParameterConstraint(name="b", type="int", sign="negative"),
        ParameterConstraint(name="c", type="int", sign="positive"),
    ],
    invariants=[
        Invariant(
            description="f(0) is a clean negative integer (initial loss)",
            sympy_expr="f.subs(x, 0)",
            must_be="negative_integer",
        ),
        Invariant(
            description="numerator root is a clean positive integer (break-even year)",
            # Numerator of f is linear in x, so exactly one root.
            sympy_expr="solve(f.as_numer_denom()[0], x)[0]",
            must_be="positive_integer",
        ),
        Invariant(
            description="f' has a clean positive integer critical point (peak year)",
            sympy_expr="max(s for s in solve(diff(f, x), x) if s > 0)",
            must_be="positive_integer",
        ),
        Invariant(
            description="f at peak year is a clean positive integer (max profit)",
            sympy_expr="f.subs(x, max(s for s in solve(diff(f, x), x) if s > 0))",
            must_be="positive_integer",
        ),
    ],
    prose_template=(
        r"La función \(f(x) = \frac{{ {{a}}x + {{b}} }}{{x^2 + {{c}} }}\) indica"
        r" las ganancias o pérdidas que una empresa ha tenido desde que fue"
        r" constituida, expresada \(f(x)\) en miles de euros, \(x\) en años."
    ),
    student_tasks=[
        "Estudia y representa gráficamente la función (ten en cuenta el contexto del problema).",
        "¿Al cabo de cuánto tiempo obtiene la empresa una ganancia máxima? ¿Cuál es esa ganancia?",
        "¿Durante cuánto tiempo la empresa perdió dinero? ¿En qué momento perdió más?",
    ],
)
