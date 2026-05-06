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

from app.models import Template, Variant
from app.pipeline.verify import verify

# Registry mapping template_id → sampler function.
_SAMPLERS: dict[str, object] = {}


def register_sampler(template_id: str):
    def decorator(fn):
        _SAMPLERS[template_id] = fn
        return fn
    return decorator


def sample_parameters(template: Template, max_attempts: int = 50) -> Variant:
    """Return a verified Variant for *template*, or raise RuntimeError."""
    sampler = _SAMPLERS.get(template.template_id)
    if sampler is None:
        raise NotImplementedError(
            f"No sampler registered for template '{template.template_id}'"
        )
    return sampler(template, max_attempts)


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
