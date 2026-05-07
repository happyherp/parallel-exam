"""Stage 5: sample parameter values for a Template and return a verified Variant.

For the rational_business_profit template the search space is parameterised
by (k, p, n):
    k = break-even year   (positive integer)
    p = peak year         (positive integer, must satisfy p > 2k so c > 0)
    n = scaling factor    (positive integer)

Derived parameters:
    a = 2 * p * n
    b = -k * a
    c = p * (p - 2*k)

An additional pre-filter checks that f(0) = -2kn/(p-2k) is an integer,
i.e. (p - 2k) divides 2kn, which avoids wasting verify calls.
"""

from __future__ import annotations

import random

from app.models import ParameterConstraint, Template, Variant
from app.pipeline.verify import verify

# Registry mapping template_id → sampler function.
_SAMPLERS: dict[str, object] = {}


def register_sampler(template_id: str):
    def decorator(fn):
        _SAMPLERS[template_id] = fn
        return fn
    return decorator


def sample_parameters(template: Template, max_attempts: int = 50) -> Variant:
    """Return a verified Variant for *template*, or raise RuntimeError.

    If a hand-written sampler is registered for ``template.template_id`` it
    is used (smart, problem-specific). Otherwise the generic brute-force
    sampler is invoked — useful for LLM-extracted templates.
    """
    sampler = _SAMPLERS.get(template.template_id)
    if sampler is not None:
        return sampler(template, max_attempts)
    # LLM-extracted templates have no smart parameterisation — invariants
    # like "f' has integer critical point" are restrictive, so we need a
    # much larger budget than for hand-written templates.
    return _generic_sampler(template, max_attempts=max(max_attempts * 50, 2500))


# ── generic brute-force sampler (LLM-extracted templates) ────────────────────

def _random_value(c: ParameterConstraint) -> int | float:
    """Sample a value satisfying *c*'s sign / min / max / type constraints."""
    lo, hi = -30, 30
    if c.sign == "positive":
        lo = 1
    elif c.sign == "negative":
        hi = -1

    if c.min is not None:
        lo = max(lo, int(c.min))
    if c.max is not None:
        hi = min(hi, int(c.max))

    if lo > hi:  # nonsense constraint — fall back to a single point
        return lo

    if c.type == "int":
        return random.randint(lo, hi)
    return round(random.uniform(lo, hi), 4)


def _generic_sampler(template: Template, max_attempts: int) -> Variant:
    """Random integer search over parameter space until verify() succeeds."""
    for _ in range(max_attempts):
        params = {c.name: _random_value(c) for c in template.parameters}
        variant = verify(template, params)
        if variant.verified:
            return variant

    raise RuntimeError(
        f"Generic sampler exhausted {max_attempts} attempts for "
        f"'{template.template_id}'. The template's invariants may be too "
        f"restrictive for blind random search."
    )


# ── rational_business_profit sampler ─────────────────────────────────────────

@register_sampler("rational_business_profit_v1")
def _sample_rational_business_profit(template: Template, max_attempts: int) -> Variant:
    for _ in range(max_attempts):
        k = random.randint(1, 6)
        # p must satisfy p > 2k (so c = p*(p-2k) > 0) and p > k.
        p = random.randint(2 * k + 1, 2 * k + 8)
        n = random.randint(1, 12)

        q = p - 2 * k  # must divide 2kn for f(0) to be an integer
        if (2 * k * n) % q != 0:
            continue

        a = 2 * p * n
        b = -k * a
        c = p * q

        variant = verify(template, {"a": a, "b": b, "c": c})
        if variant.verified:
            return variant

    raise RuntimeError(
        f"Could not find a verified variant for '{template.template_id}' "
        f"after {max_attempts} attempts."
    )
