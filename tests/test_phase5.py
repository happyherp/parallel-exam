"""Phase 5 acceptance tests — LLM-based template extraction.

The Anthropic API is mocked in every test so the suite runs without a real
key or network. Coverage:
  - generic brute-force sampler in generate.py
  - parameter bound inference from original_parameters
  - extract_template happy path (extracted template verifies)
  - extract_template rejects templates that fail SymPy verification
  - extract_template returns None for malformed / abstaining LLM output
  - extract_template falls back gracefully when API key is missing
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from app.models import Invariant, ParameterConstraint, Problem, Template


# ── helpers ───────────────────────────────────────────────────────────────────

# A reusable, well-formed template payload (matches the hand-written
# rational_business_profit template). Used as the LLM's response body.
_GOOD_PAYLOAD = {
    "function_form": "(a*x + b) / (x**2 + c)",
    "parameters": [
        {"name": "a", "type": "int", "sign": "positive"},
        {"name": "b", "type": "int", "sign": "negative"},
        {"name": "c", "type": "int", "sign": "positive"},
    ],
    "invariants": [
        {
            "description": "f(0) is a clean negative integer",
            "sympy_expr": "f.subs(x, 0)",
            "must_be": "negative_integer",
        },
        {
            "description": "numerator root is a positive integer",
            "sympy_expr": "solve(f.as_numer_denom()[0], x)[0]",
            "must_be": "positive_integer",
        },
    ],
    "prose_template": (
        r"La función \(f(x) = \frac{{ {{a}}x + {{b}} }}{{x^2 + {{c}} }}\)."
    ),
    "student_tasks": ["Estudia y representa gráficamente la función."],
    "original_parameters": {"a": 80, "b": -160, "c": 5},
}

_PROBLEM = Problem(
    number=1,
    points=3.0,
    prose_latex=r"\(f(x) = \frac{80x - 160}{x^{2} + 5}\)",
    sub_parts=[],
)


def _mock_response(payload: dict | None, *, stop_reason: str = "tool_use") -> MagicMock:
    """Build a fake Anthropic response with one tool_use block."""
    block = MagicMock()
    block.type = "tool_use"
    block.name = "submit_template"
    block.input = payload if payload is not None else {}

    response = MagicMock()
    response.content = [block] if payload is not None else []
    response.stop_reason = stop_reason
    return response


# ── generic brute-force sampler ───────────────────────────────────────────────

def test_generic_sampler_finds_verified_variant():
    """Brute force should find an (a, b, c) triple satisfying both invariants."""
    from app.pipeline.generate import sample_parameters

    # A template with relaxed enough invariants that random search succeeds.
    template = Template(
        template_id="brute_force_test_v1",
        function_form="a*x + b",  # linear
        parameters=[
            ParameterConstraint(name="a", type="int", sign="positive", min=1, max=10),
            ParameterConstraint(name="b", type="int", sign="negative", min=-20, max=-1),
        ],
        invariants=[
            Invariant(
                description="root is positive integer",
                sympy_expr="solve(f, x)[0]",
                must_be="positive_integer",
            ),
        ],
        prose_template="f(x) = {{a}}x + {{b}}",
        student_tasks=[],
    )
    variant = sample_parameters(template, max_attempts=50)
    assert variant.verified is True
    assert variant.parameters["a"] >= 1
    assert variant.parameters["b"] <= -1


def test_generic_sampler_respects_min_max():
    """Constraints with explicit min/max must be honoured by the sampler."""
    from app.pipeline.generate import _random_value

    c = ParameterConstraint(name="x", type="int", sign="positive", min=10, max=12)
    for _ in range(20):
        v = _random_value(c)
        assert 10 <= v <= 12


def test_generic_sampler_raises_when_unsatisfiable():
    """Tight, unsatisfiable invariants must lead to a clear error."""
    from app.pipeline.generate import sample_parameters

    template = Template(
        template_id="impossible_v1",
        function_form="a*x",
        parameters=[
            ParameterConstraint(name="a", type="int", sign="positive", min=1, max=2),
        ],
        invariants=[
            Invariant(
                description="impossible: a must be negative integer",
                sympy_expr="a",  # references a parameter directly
                must_be="negative_integer",
            ),
        ],
        prose_template="x",
        student_tasks=[],
    )
    with pytest.raises(RuntimeError):
        sample_parameters(template, max_attempts=20)


# ── _bound_constraint ────────────────────────────────────────────────────────

def test_bound_constraint_brackets_around_original():
    from app.pipeline.template import _bound_constraint

    c = ParameterConstraint(name="a", type="int", sign="positive")
    bounded = _bound_constraint(c, original=80.0)
    assert bounded.min == 1.0
    assert bounded.max >= 80 * 4  # 4× margin


def test_bound_constraint_negative_sign():
    from app.pipeline.template import _bound_constraint

    c = ParameterConstraint(name="b", type="int", sign="negative")
    bounded = _bound_constraint(c, original=-160.0)
    assert bounded.max == -1.0
    assert bounded.min <= -160 * 4


def test_bound_constraint_keeps_explicit_bounds():
    from app.pipeline.template import _bound_constraint

    c = ParameterConstraint(name="a", type="int", sign="positive", min=2, max=5)
    bounded = _bound_constraint(c, original=80.0)
    assert bounded.min == 2.0
    assert bounded.max == 5.0


# ── extract_template — happy path ─────────────────────────────────────────────

def test_extract_template_happy_path():
    from app.pipeline.template import extract_template

    fake_client = MagicMock()
    fake_client.messages.create.return_value = _mock_response(_GOOD_PAYLOAD)

    with patch("app.pipeline.template.get_client", return_value=fake_client):
        template = extract_template(_PROBLEM)

    assert template is not None
    assert template.template_id == "llm_extracted_p1"
    assert template.function_form == "(a*x + b) / (x**2 + c)"
    # Bounds were inferred from original_parameters.
    a_constraint = next(c for c in template.parameters if c.name == "a")
    assert a_constraint.max is not None and a_constraint.max >= 80


def test_extract_template_uses_tool_use_with_caching():
    """The system prompt must be sent with cache_control for token savings."""
    from app.pipeline.template import extract_template

    fake_client = MagicMock()
    fake_client.messages.create.return_value = _mock_response(_GOOD_PAYLOAD)

    with patch("app.pipeline.template.get_client", return_value=fake_client):
        extract_template(_PROBLEM)

    call_kwargs = fake_client.messages.create.call_args.kwargs
    assert call_kwargs["tools"][0]["name"] == "submit_template"
    assert call_kwargs["tool_choice"] == {"type": "tool", "name": "submit_template"}
    assert call_kwargs["system"][0]["cache_control"] == {"type": "ephemeral"}


# ── extract_template — failure modes ─────────────────────────────────────────

def test_extract_template_rejects_when_invariants_fail():
    """If the LLM's invariants don't hold for the original params, reject."""
    from app.pipeline.template import extract_template

    bad_payload = dict(_GOOD_PAYLOAD)
    # A bogus invariant that asks for f(0) to be a positive integer when in
    # fact f(0) = -160/5 = -32 (negative). Verification must catch this.
    bad_payload["invariants"] = [
        {
            "description": "wrong",
            "sympy_expr": "f.subs(x, 0)",
            "must_be": "positive_integer",
        },
    ]
    fake_client = MagicMock()
    fake_client.messages.create.return_value = _mock_response(bad_payload)

    with patch("app.pipeline.template.get_client", return_value=fake_client):
        template = extract_template(_PROBLEM)

    assert template is None


def test_extract_template_rejects_when_function_form_is_wrong():
    """Mismatched function_form vs original_parameters → SymPy errors → reject."""
    from app.pipeline.template import extract_template

    bad_payload = dict(_GOOD_PAYLOAD)
    bad_payload["function_form"] = "z*x + y"  # parameters are a/b/c, not z/y
    fake_client = MagicMock()
    fake_client.messages.create.return_value = _mock_response(bad_payload)

    with patch("app.pipeline.template.get_client", return_value=fake_client):
        template = extract_template(_PROBLEM)

    assert template is None


def test_extract_template_abstains_on_empty_payload():
    """LLM signals 'cannot template' via empty parameters/invariants/original."""
    from app.pipeline.template import extract_template

    payload = {
        "function_form": "x",
        "parameters": [],
        "invariants": [],
        "prose_template": "...",
        "student_tasks": [],
        "original_parameters": {},
    }
    fake_client = MagicMock()
    fake_client.messages.create.return_value = _mock_response(payload)

    with patch("app.pipeline.template.get_client", return_value=fake_client):
        template = extract_template(_PROBLEM)

    assert template is None


def test_extract_template_returns_none_when_no_tool_use():
    """If the model responds in text instead of calling the tool, return None."""
    from app.pipeline.template import extract_template

    response = MagicMock()
    response.content = []  # no tool_use block at all
    fake_client = MagicMock()
    fake_client.messages.create.return_value = response

    with patch("app.pipeline.template.get_client", return_value=fake_client):
        template = extract_template(_PROBLEM)

    assert template is None


def test_extract_template_falls_back_when_api_key_missing():
    """Missing key → get_client raises → extract_template returns None."""
    from app.pipeline.template import extract_template

    with patch("app.pipeline.template.get_client", side_effect=RuntimeError("no key")):
        template = extract_template(_PROBLEM)

    assert template is None


def test_extract_template_falls_back_on_api_error():
    """Network / rate-limit errors must degrade gracefully."""
    from app.pipeline.template import extract_template

    fake_client = MagicMock()
    fake_client.messages.create.side_effect = Exception("rate limit")

    with patch("app.pipeline.template.get_client", return_value=fake_client):
        template = extract_template(_PROBLEM)

    assert template is None
