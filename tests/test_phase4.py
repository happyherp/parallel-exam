"""Phase 4 acceptance tests — .docx output and /download route.

Tests that require pandoc are allowed to fail locally (pandoc not installed
in the dev environment) and pass in CI, consistent with Phase 1/2 tests.
"""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

FIXTURES = Path(__file__).parent / "fixtures"
DERIVADAS2 = FIXTURES / "derivadas2.doc.docx"


@pytest.fixture(scope="module")
def client():
    from app.main import app
    return TestClient(app)


# ── _build_latex unit tests (no pandoc needed) ────────────────────────────────

def test_build_latex_with_variant():
    from app.models import Problem, Variant
    from app.pipeline.render import _build_latex
    from app.pipeline.templates_library.rational_business_profit import (
        RATIONAL_BUSINESS_PROFIT,
    )

    problems = [Problem(number=1, points=3.0, prose_latex="original prose", sub_parts=[])]
    templates = {0: RATIONAL_BUSINESS_PROFIT}
    variants = {
        0: Variant(
            template_id="rational_business_profit_v1",
            parameters={"a": 70, "b": -210, "c": 7},
            rendered_prose_latex=r"La función \(f(x) = \frac{ 70x - 210 }{x^2 + 7 }\) indica algo.",
            verification={},
            verified=True,
        )
    }

    latex = _build_latex(problems, templates, variants)

    assert r"\begin{document}" in latex
    assert r"\end{document}" in latex
    assert r"\begin{enumerate}" in latex
    assert r"\item" in latex
    assert r"\frac" in latex
    # Student tasks should appear
    assert "gráficamente" in latex or "ganancia" in latex


def test_build_latex_without_variant_falls_back_to_original():
    from app.models import Problem
    from app.pipeline.render import _build_latex

    problems = [Problem(number=2, points=1.0, prose_latex="Calcula la derivada de \\(f(x)\\).",
                        sub_parts=["a) parte uno", "b) parte dos"])]
    templates = {0: None}
    variants = {0: None}

    latex = _build_latex(problems, templates, variants)

    assert "Calcula la derivada" in latex
    assert "parte uno" in latex
    assert "parte dos" in latex


def test_build_latex_escapes_percent_in_tasks():
    from app.pipeline.render import _escape

    assert _escape("50% de descuento") == r"50\% de descuento"
    assert _escape("precio & coste") == r"precio \& coste"


def test_build_latex_mixed_problems():
    """Two problems: first has variant, second is pass-through original."""
    from app.models import Problem, Variant
    from app.pipeline.render import _build_latex
    from app.pipeline.templates_library.rational_business_profit import (
        RATIONAL_BUSINESS_PROFIT,
    )

    problems = [
        Problem(number=1, points=3.0, prose_latex="original 1", sub_parts=[]),
        Problem(number=2, points=1.0, prose_latex="original 2", sub_parts=["a) foo"]),
    ]
    templates = {0: RATIONAL_BUSINESS_PROFIT, 1: None}
    variants = {
        0: Variant(
            template_id="rational_business_profit_v1",
            parameters={"a": 80, "b": -160, "c": 5},
            rendered_prose_latex=r"Reworded prose with \(f(x)\).",
            verification={},
            verified=True,
        ),
        1: None,
    }

    latex = _build_latex(problems, templates, variants)

    assert "Reworded prose" in latex
    assert "original 2" in latex
    assert "foo" in latex


# ── variants_to_docx integration test (needs pandoc) ─────────────────────────

def test_variants_to_docx_creates_file(tmp_path):
    from app.models import Problem, Variant
    from app.pipeline.render import variants_to_docx

    problems = [Problem(number=1, points=3.0, prose_latex="Prose.", sub_parts=[])]
    templates = {0: None}
    variants = {0: None}
    out = tmp_path / "output.docx"

    variants_to_docx(problems, templates, variants, out)

    assert out.exists()
    assert out.stat().st_size > 0


def test_variants_to_docx_with_variant(tmp_path):
    from app.models import Problem, Variant
    from app.pipeline.render import variants_to_docx
    from app.pipeline.templates_library.rational_business_profit import (
        RATIONAL_BUSINESS_PROFIT,
    )

    problems = [Problem(number=1, points=3.0, prose_latex="original", sub_parts=[])]
    templates = {0: RATIONAL_BUSINESS_PROFIT}
    variants = {
        0: Variant(
            template_id="rational_business_profit_v1",
            parameters={"a": 70, "b": -210, "c": 7},
            rendered_prose_latex=r"La función \(f(x) = \frac{ 70x - 210 }{x^2 + 7 }\) indica algo.",
            verification={},
            verified=True,
        )
    }
    out = tmp_path / "output.docx"

    variants_to_docx(problems, templates, variants, out)

    assert out.exists()
    # docx files start with the PK zip magic number.
    assert out.read_bytes()[:2] == b"PK"


# ── /download route ───────────────────────────────────────────────────────────

def test_download_unknown_job_returns_404(client):
    resp = client.get("/download/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404


def test_download_returns_docx(client):
    """Full round-trip: upload → download. Needs pandoc."""
    with open(DERIVADAS2, "rb") as f:
        upload_resp = client.post(
            "/upload",
            files={"file": ("derivadas2.docx", f,
                            "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
        )
    assert upload_resp.status_code == 200

    import re
    m = re.search(r"/download/([0-9a-f-]{36})", upload_resp.text)
    assert m, "No download link found in upload response"
    job_id = m.group(1)

    dl_resp = client.get(f"/download/{job_id}")
    assert dl_resp.status_code == 200
    assert dl_resp.headers["content-type"].startswith(
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    # docx is a zip — check magic bytes.
    assert dl_resp.content[:2] == b"PK"
    assert "variante" in dl_resp.headers.get("content-disposition", "")
