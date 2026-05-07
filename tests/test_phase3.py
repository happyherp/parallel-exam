"""Phase 3 acceptance tests — surface text rewording via LLM.

All Anthropic API calls are mocked so these tests run without a real key or
network connection.  The tests verify:
  - _math_preserved() correctly validates LaTeX block identity
  - reword_surface() calls the API with the right arguments
  - reword_surface() returns the LLM output when math is preserved
  - reword_surface() falls back to mechanical prose when math is altered
  - reword_surface() falls back gracefully on API errors (key not set, etc.)
  - config and llm modules load and surface sensible errors
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from app.models import Variant
from app.pipeline.reword import _extract_math, _math_preserved, reword_surface
from app.pipeline.templates_library.rational_business_profit import (
    RATIONAL_BUSINESS_PROFIT,
)


# ── helpers ───────────────────────────────────────────────────────────────────

def _variant(prose: str) -> Variant:
    return Variant(
        template_id="rational_business_profit_v1",
        parameters={"a": 70, "b": -210, "c": 7},
        rendered_prose_latex=prose,
        verification={},
        verified=True,
    )


MECHANICAL_PROSE = (
    r"La función \(f(x) = \frac{ 70x - 210 }{x^2 + 7 }\) indica"
    r" las ganancias o pérdidas que una empresa ha tenido desde que fue"
    r" constituida, expresada \(f(x)\) en miles de euros, \(x\) en años."
)

REWORDED_PROSE = (
    r"La función \(f(x) = \frac{ 70x - 210 }{x^2 + 7 }\) representa"
    r" la producción de una fábrica desde su apertura,"
    r" expresada \(f(x)\) en toneladas, \(x\) en meses."
)

TAMPERED_PROSE = (
    r"La función \(f(x) = \frac{ 80x - 210 }{x^2 + 7 }\) indica algo."  # 80 instead of 70
)


# ── _extract_math ─────────────────────────────────────────────────────────────

def test_extract_math_finds_inline():
    math = _extract_math(r"Texto \(f(x) = x^2\) y más \(g(x)\).")
    assert r"\(f(x) = x^2\)" in math
    assert r"\(g(x)\)" in math


def test_extract_math_finds_display():
    math = _extract_math(r"Ver \[f(x) = \frac{1}{x}\] aquí.")
    assert len(math) == 1
    assert r"\[f(x) = \frac{1}{x}\]" in math


def test_extract_math_empty_string():
    assert _extract_math("no hay matemáticas") == []


# ── _math_preserved ───────────────────────────────────────────────────────────

def test_math_preserved_identical():
    assert _math_preserved(MECHANICAL_PROSE, MECHANICAL_PROSE) is True


def test_math_preserved_context_changed_math_same():
    assert _math_preserved(MECHANICAL_PROSE, REWORDED_PROSE) is True


def test_math_preserved_detects_tampered_number():
    assert _math_preserved(MECHANICAL_PROSE, TAMPERED_PROSE) is False


def test_math_preserved_detects_missing_block():
    # Drop the second math block from reworded
    truncated = r"La función \(f(x) = \frac{ 70x - 210 }{x^2 + 7 }\) algo."
    assert _math_preserved(MECHANICAL_PROSE, truncated) is False


# ── reword_surface — happy path ───────────────────────────────────────────────

def _mock_response(text: str):
    """Build a minimal fake Anthropic response object."""
    block = MagicMock()
    block.text = text
    resp = MagicMock()
    resp.content = [block]
    return resp


def test_reword_surface_uses_llm_output():
    variant = _variant(MECHANICAL_PROSE)
    mock_client = MagicMock()
    mock_client.messages.create.return_value = _mock_response(REWORDED_PROSE)

    with patch("app.pipeline.reword.get_client", return_value=mock_client):
        result = reword_surface(variant, RATIONAL_BUSINESS_PROFIT)

    assert result.rendered_prose_latex == REWORDED_PROSE


def test_reword_surface_passes_prose_in_user_message():
    variant = _variant(MECHANICAL_PROSE)
    mock_client = MagicMock()
    mock_client.messages.create.return_value = _mock_response(REWORDED_PROSE)

    with patch("app.pipeline.reword.get_client", return_value=mock_client):
        reword_surface(variant, RATIONAL_BUSINESS_PROFIT)

    call_kwargs = mock_client.messages.create.call_args.kwargs
    user_content = call_kwargs["messages"][0]["content"]
    assert MECHANICAL_PROSE in user_content


def test_reword_surface_includes_prompt_cache_control():
    variant = _variant(MECHANICAL_PROSE)
    mock_client = MagicMock()
    mock_client.messages.create.return_value = _mock_response(REWORDED_PROSE)

    with patch("app.pipeline.reword.get_client", return_value=mock_client):
        reword_surface(variant, RATIONAL_BUSINESS_PROFIT)

    call_kwargs = mock_client.messages.create.call_args.kwargs
    system = call_kwargs["system"]
    assert any(
        block.get("cache_control") == {"type": "ephemeral"}
        for block in system
        if isinstance(block, dict)
    )


# ── reword_surface — rejection / fallback ────────────────────────────────────

def test_reword_surface_rejects_tampered_math():
    """LLM changed a coefficient — output must be rejected."""
    variant = _variant(MECHANICAL_PROSE)
    mock_client = MagicMock()
    mock_client.messages.create.return_value = _mock_response(TAMPERED_PROSE)

    with patch("app.pipeline.reword.get_client", return_value=mock_client):
        result = reword_surface(variant, RATIONAL_BUSINESS_PROFIT)

    assert result.rendered_prose_latex == MECHANICAL_PROSE


def test_reword_surface_falls_back_on_api_error():
    variant = _variant(MECHANICAL_PROSE)
    mock_client = MagicMock()
    mock_client.messages.create.side_effect = Exception("network error")

    with patch("app.pipeline.reword.get_client", return_value=mock_client):
        result = reword_surface(variant, RATIONAL_BUSINESS_PROFIT)

    assert result.rendered_prose_latex == MECHANICAL_PROSE


def test_reword_surface_falls_back_when_api_key_missing():
    variant = _variant(MECHANICAL_PROSE)

    with patch("app.pipeline.reword.get_client", side_effect=RuntimeError("no key")):
        result = reword_surface(variant, RATIONAL_BUSINESS_PROFIT)

    assert result.rendered_prose_latex == MECHANICAL_PROSE


def test_reword_surface_skips_empty_prose():
    """No LLM call should be made if rendered_prose_latex is empty."""
    variant = _variant("")
    mock_client = MagicMock()

    with patch("app.pipeline.reword.get_client", return_value=mock_client):
        result = reword_surface(variant, RATIONAL_BUSINESS_PROFIT)

    mock_client.messages.create.assert_not_called()
    assert result.rendered_prose_latex == ""


# ── config / llm module ───────────────────────────────────────────────────────

def test_get_client_raises_without_key():
    from app.llm import get_client
    import app.llm as llm_module

    original = llm_module._client
    llm_module._client = None  # reset singleton
    try:
        with patch("app.llm.settings") as mock_settings:
            mock_settings.anthropic_api_key = ""
            with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY"):
                get_client()
    finally:
        llm_module._client = original
