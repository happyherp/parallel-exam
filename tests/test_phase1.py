"""Phase 1 acceptance tests — deterministic pipeline, no LLM."""

from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"
DERIVADAS2 = FIXTURES / "derivadas2.doc.docx"
ANALISIS1 = FIXTURES / "Ex Analisis 1º Bach .docx"


# ── 1.1 extract ───────────────────────────────────────────────────────────────

def test_extract_returns_latex():
    from app.pipeline.extract import docx_to_latex

    latex = docx_to_latex(DERIVADAS2)
    assert isinstance(latex, str)
    assert len(latex) > 100


def test_extract_contains_problem1_formula():
    from app.pipeline.extract import docx_to_latex

    latex = docx_to_latex(DERIVADAS2)
    # Pandoc renders the OMML formula as LaTeX; check the key fraction.
    assert r"\frac{80x - 160}{x^{2} + 5}" in latex


# ── 1.2 parse ─────────────────────────────────────────────────────────────────

def test_parse_yields_five_problems():
    from app.pipeline.extract import docx_to_latex
    from app.pipeline.parse import latex_to_problems

    latex = docx_to_latex(DERIVADAS2)
    problems = latex_to_problems(latex)
    assert len(problems) == 5


def test_parse_problem_numbers():
    from app.pipeline.extract import docx_to_latex
    from app.pipeline.parse import latex_to_problems

    latex = docx_to_latex(DERIVADAS2)
    problems = latex_to_problems(latex)
    assert [p.number for p in problems] == [1, 2, 3, 4, 5]


def test_parse_problem_points():
    from app.pipeline.extract import docx_to_latex
    from app.pipeline.parse import latex_to_problems

    latex = docx_to_latex(DERIVADAS2)
    problems = latex_to_problems(latex)
    assert problems[0].points == 3.0
    assert problems[1].points == 1.0
    assert problems[2].points == 2.0
    assert problems[3].points == 1.0
    assert problems[4].points == 2.0


def test_parse_problem1_prose_contains_formula():
    from app.pipeline.extract import docx_to_latex
    from app.pipeline.parse import latex_to_problems

    latex = docx_to_latex(DERIVADAS2)
    problems = latex_to_problems(latex)
    # The fraction should survive pandoc → parse.
    assert r"\frac{80x - 160}{x^{2} + 5}" in problems[0].prose_latex


def test_parse_problem1_has_subparts():
    from app.pipeline.extract import docx_to_latex
    from app.pipeline.parse import latex_to_problems

    latex = docx_to_latex(DERIVADAS2)
    problems = latex_to_problems(latex)
    assert len(problems[0].sub_parts) == 3


# ── 1.3 hand-written template ─────────────────────────────────────────────────

def test_template_loads():
    from app.pipeline.templates_library.rational_business_profit import (
        RATIONAL_BUSINESS_PROFIT,
    )
    from app.models import Template

    assert isinstance(RATIONAL_BUSINESS_PROFIT, Template)
    assert RATIONAL_BUSINESS_PROFIT.template_id == "rational_business_profit_v1"
    assert len(RATIONAL_BUSINESS_PROFIT.invariants) == 4
    assert len(RATIONAL_BUSINESS_PROFIT.parameters) == 3


# ── 1.4 verify ────────────────────────────────────────────────────────────────

@pytest.fixture
def rbp_template():
    from app.pipeline.templates_library.rational_business_profit import (
        RATIONAL_BUSINESS_PROFIT,
    )
    return RATIONAL_BUSINESS_PROFIT


def test_verify_known_good_params(rbp_template):
    """Acceptance: (a=70, b=-210, c=7) → verified=True with correct values."""
    from app.pipeline.verify import verify

    variant = verify(rbp_template, {"a": 70, "b": -210, "c": 7})
    assert variant.verified is True
    assert variant.template_id == "rational_business_profit_v1"

    ver = variant.verification
    # f(0) = -210/7 = -30
    assert ver["f(0) is a clean negative integer (initial loss)"] == "-30"
    # break-even: 70x - 210 = 0 → x = 3
    assert ver["numerator root is a clean positive integer (break-even year)"] == "3"
    # peak: x = 7
    assert ver["f' has a clean positive integer critical point (peak year)"] == "7"
    # f(7) = (490 - 210) / 56 = 5
    assert ver["f at peak year is a clean positive integer (max profit)"] == "5"


def test_verify_original_params(rbp_template):
    """Original problem params (a=80, b=-160, c=5) must also verify."""
    from app.pipeline.verify import verify

    variant = verify(rbp_template, {"a": 80, "b": -160, "c": 5})
    assert variant.verified is True


def test_verify_bad_params_rejected(rbp_template):
    """Params that produce non-integer results must fail verification."""
    from app.pipeline.verify import verify

    # c=3 → f(0) = -160/3, not integer.
    variant = verify(rbp_template, {"a": 80, "b": -160, "c": 3})
    assert variant.verified is False


# ── 1.5 generate ──────────────────────────────────────────────────────────────

def test_generate_returns_verified_variant(rbp_template):
    from app.pipeline.generate import sample_parameters

    variant = sample_parameters(rbp_template)
    assert variant.verified is True


def test_generate_produces_variety(rbp_template):
    """Two successive calls should (almost certainly) differ."""
    from app.pipeline.generate import sample_parameters

    variants = [sample_parameters(rbp_template) for _ in range(5)]
    param_sets = [tuple(sorted(v.parameters.items())) for v in variants]
    # At least 2 distinct parameter sets among 5 samples.
    assert len(set(param_sets)) >= 2


# ── Ex Analisis 1º Bach — extract ────────────────────────────────────────────

def test_extract_analisis1_returns_latex():
    from app.pipeline.extract import docx_to_latex

    latex = docx_to_latex(ANALISIS1)
    assert isinstance(latex, str)
    assert len(latex) > 100


def test_extract_analisis1_contains_problem1_formula():
    from app.pipeline.extract import docx_to_latex

    latex = docx_to_latex(ANALISIS1)
    # Cubic polynomial from Problema 1.
    assert r"x^{3} + 4x^{2} + x - 6" in latex


def test_extract_analisis1_contains_problem2_fraction():
    from app.pipeline.extract import docx_to_latex

    latex = docx_to_latex(ANALISIS1)
    # Rational function from Problema 2.
    assert r"\frac{2x^{2} + 1}{x^{2} + 2x - 3}" in latex


# ── Ex Analisis 1º Bach — parse ───────────────────────────────────────────────

def test_parse_analisis1_yields_three_problems():
    from app.pipeline.extract import docx_to_latex
    from app.pipeline.parse import latex_to_problems

    latex = docx_to_latex(ANALISIS1)
    problems = latex_to_problems(latex)
    assert len(problems) == 3


def test_parse_analisis1_problem_numbers():
    from app.pipeline.extract import docx_to_latex
    from app.pipeline.parse import latex_to_problems

    latex = docx_to_latex(ANALISIS1)
    problems = latex_to_problems(latex)
    assert [p.number for p in problems] == [1, 2, 3]


def test_parse_analisis1_problem_points():
    from app.pipeline.extract import docx_to_latex
    from app.pipeline.parse import latex_to_problems

    latex = docx_to_latex(ANALISIS1)
    problems = latex_to_problems(latex)
    assert problems[0].points == 4.0
    assert problems[1].points == 4.0
    assert problems[2].points == 2.0


def test_parse_analisis1_problem1_prose_contains_formula():
    from app.pipeline.extract import docx_to_latex
    from app.pipeline.parse import latex_to_problems

    latex = docx_to_latex(ANALISIS1)
    problems = latex_to_problems(latex)
    assert r"x^{3} + 4x^{2} + x - 6" in problems[0].prose_latex


def test_parse_analisis1_problem1_has_subparts():
    from app.pipeline.extract import docx_to_latex
    from app.pipeline.parse import latex_to_problems

    latex = docx_to_latex(ANALISIS1)
    problems = latex_to_problems(latex)
    assert len(problems[0].sub_parts) == 3


def test_parse_analisis1_problem2_has_subparts():
    from app.pipeline.extract import docx_to_latex
    from app.pipeline.parse import latex_to_problems

    latex = docx_to_latex(ANALISIS1)
    problems = latex_to_problems(latex)
    assert len(problems[1].sub_parts) == 2


def test_parse_analisis1_problem3_no_subparts():
    from app.pipeline.extract import docx_to_latex
    from app.pipeline.parse import latex_to_problems

    latex = docx_to_latex(ANALISIS1)
    problems = latex_to_problems(latex)
    assert len(problems[2].sub_parts) == 0
