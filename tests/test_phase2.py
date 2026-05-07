"""Phase 2 acceptance tests — UI shell (routes, job store, prose rendering)."""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

FIXTURES = Path(__file__).parent / "fixtures"
DERIVADAS2 = FIXTURES / "derivadas2.doc.docx"


@pytest.fixture(scope="module")
def client():
    from app.main import app
    return TestClient(app)


# ── Index ──────────────────────────────────────────────────────────────────────

def test_index_returns_200(client):
    resp = client.get("/")
    assert resp.status_code == 200


def test_index_contains_upload_form(client):
    resp = client.get("/")
    assert "<form" in resp.text
    assert 'action="/upload"' in resp.text


# ── /upload validation ─────────────────────────────────────────────────────────

def test_upload_rejects_non_docx(client):
    resp = client.post(
        "/upload",
        files={"file": ("exam.pdf", b"%PDF-1.4 fake", "application/pdf")},
    )
    assert resp.status_code == 400
    assert "docx" in resp.text.lower()


def test_upload_rejects_txt(client):
    resp = client.post(
        "/upload",
        files={"file": ("notes.txt", b"hello world", "text/plain")},
    )
    assert resp.status_code == 400


# ── /upload happy path ─────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def upload_response(client):
    with open(DERIVADAS2, "rb") as f:
        resp = client.post(
            "/upload",
            files={"file": ("derivadas2.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
        )
    return resp


def test_upload_derivadas2_succeeds(upload_response):
    assert upload_response.status_code == 200


def test_upload_shows_five_problems(upload_response):
    # Five problem cards should appear.
    text = upload_response.text
    assert text.count("Problema 1") >= 1
    assert text.count("Problema 5") >= 1


def test_upload_problem1_has_variant(upload_response):
    # Problem 1 is the rational-business-profit type; a variant card should appear.
    assert "Variante generada" in upload_response.text
    assert "Regenerar" in upload_response.text


def test_upload_contains_katex_math(upload_response):
    # The original formula should be in the page (KaTeX renders it client-side).
    assert r"\frac" in upload_response.text


def test_upload_other_problems_have_no_template(upload_response):
    # Problems without a library template show a "Generar variante" button (lazy path).
    assert "Generar variante" in upload_response.text


# ── /generate ─────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def job_id(client):
    """Extract job_id from a fresh upload so we can call /generate."""
    import re
    with open(DERIVADAS2, "rb") as f:
        resp = client.post(
            "/upload",
            files={"file": ("derivadas2.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
        )
    # job_id appears in HTMX URLs like /generate/{job_id}/0
    m = re.search(r"/generate/([0-9a-f-]{36})/", resp.text)
    assert m, "Could not extract job_id from upload response"
    return m.group(1)


def test_generate_returns_200(client, job_id):
    resp = client.post(f"/generate/{job_id}/0")
    assert resp.status_code == 200


def test_generate_returns_variant_html(client, job_id):
    resp = client.post(f"/generate/{job_id}/0")
    assert "Regenerar" in resp.text
    # The variant prose must contain KaTeX math.
    assert r"\frac" in resp.text


def test_generate_produces_different_variants(client, job_id):
    """Two consecutive /generate calls should (almost always) differ."""
    params_seen = set()
    for _ in range(5):
        resp = client.post(f"/generate/{job_id}/0")
        assert resp.status_code == 200
        params_seen.add(resp.text)
    assert len(params_seen) >= 2, "Five regenerations produced identical output every time"


def test_generate_unknown_job_returns_404(client):
    resp = client.post("/generate/00000000-0000-0000-0000-000000000000/0")
    assert resp.status_code == 404


def test_generate_problem_without_template_falls_back_when_extraction_fails(client, job_id):
    # When LLM extraction returns None (e.g. no API key, abstention), endpoint returns 400.
    from unittest.mock import patch
    with patch("app.main.extract_template", return_value=None):
        resp = client.post(f"/generate/{job_id}/1")
    assert resp.status_code == 400


# ── prose renderer unit tests ─────────────────────────────────────────────────

def test_render_prose_substitutes_params():
    from app.models import Variant
    from app.pipeline.prose import render_prose
    from app.pipeline.templates_library.rational_business_profit import (
        RATIONAL_BUSINESS_PROFIT,
    )

    variant = Variant(
        template_id="rational_business_profit_v1",
        parameters={"a": 70, "b": -210, "c": 7},
        rendered_prose_latex="",
        verification={},
        verified=True,
    )
    result = render_prose(variant, RATIONAL_BUSINESS_PROFIT)
    prose = result.rendered_prose_latex

    # Parameters substituted.
    assert "70" in prose
    assert "210" in prose
    assert "7" in prose
    # LaTeX braces are unescaped (no double-braces remain).
    assert "{{" not in prose
    assert "}}" not in prose
    # Sign cleanup: negative b should appear as subtraction, not "70x + -210".
    assert "+ -" not in prose
    assert "70x - 210" in prose or "- 210" in prose


def test_render_prose_preserves_math_delimiters():
    from app.models import Variant
    from app.pipeline.prose import render_prose
    from app.pipeline.templates_library.rational_business_profit import (
        RATIONAL_BUSINESS_PROFIT,
    )

    variant = Variant(
        template_id="rational_business_profit_v1",
        parameters={"a": 80, "b": -160, "c": 5},
        rendered_prose_latex="",
        verification={},
        verified=True,
    )
    prose = render_prose(variant, RATIONAL_BUSINESS_PROFIT).rendered_prose_latex
    # KaTeX delimiters must survive.
    assert r"\(" in prose
    assert r"\)" in prose
    assert r"\frac" in prose
