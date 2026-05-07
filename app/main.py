"""FastAPI app entry. HTMX-style server-rendered HTML, no SPA."""

from __future__ import annotations

import re
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.jobs import create_job, get_job
from app.models import Template
from app.pipeline.extract import docx_to_latex
from app.pipeline.generate import sample_parameters
from app.pipeline.parse import latex_to_problems
from app.pipeline.prose import render_prose
from app.pipeline.templates_library.rational_business_profit import (
    RATIONAL_BUSINESS_PROFIT,
)

BASE_DIR = Path(__file__).parent
jinja = Jinja2Templates(directory=BASE_DIR / "templates")

app = FastAPI(title="Parallel Exam Generator")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


# ── Template library (v1: one hand-written template) ─────────────────────────

def _find_template(prose_latex: str) -> Template | None:
    """Return the first matching Template from the library, or None.

    v1 heuristic: detect rational-function-over-quadratic by looking for
    \\frac{...x...}{x^{2}...} in the problem prose. Only one template in
    the library so far; extend this as the library grows.
    """
    if re.search(r"\\frac\{[^}]*x[^}]*\}\{x\^\{2\}", prose_latex):
        return RATIONAL_BUSINESS_PROFIT
    return None


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return jinja.TemplateResponse(request, "upload.html", {})


@app.post("/upload", response_class=HTMLResponse)
async def upload(request: Request, file: UploadFile = File(...)):
    """Receive .docx, run the deterministic pipeline, show the review page."""
    filename = file.filename or "exam.docx"

    if not filename.lower().endswith(".docx"):
        return jinja.TemplateResponse(
            request,
            "upload.html",
            {"error": "Solo se aceptan archivos .docx. "
                      "Si tienes un .doc antiguo, ábrelo con LibreOffice y guárdalo como .docx."},
            status_code=400,
        )

    # Save upload to a temp file so pypandoc (and the system pandoc binary)
    # can read it from disk.
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = Path(tmp.name)

    try:
        latex = docx_to_latex(tmp_path)
        problems = latex_to_problems(latex)
    except Exception as exc:
        return jinja.TemplateResponse(
            request,
            "upload.html",
            {"error": f"No se pudo procesar el archivo: {exc}"},
            status_code=422,
        )
    finally:
        tmp_path.unlink(missing_ok=True)

    if not problems:
        return jinja.TemplateResponse(
            request,
            "upload.html",
            {"error": "No se encontraron problemas numerados en el documento."},
            status_code=422,
        )

    # Match templates and generate initial variants.
    templates: dict[int, object] = {}
    variants: dict[int, object] = {}

    for i, problem in enumerate(problems):
        tmpl = _find_template(problem.prose_latex)
        templates[i] = tmpl
        if tmpl is not None:
            try:
                variant = sample_parameters(tmpl)
                variant = render_prose(variant, tmpl)
                variants[i] = variant
            except Exception:
                variants[i] = None
        else:
            variants[i] = None

    job = create_job(
        filename=filename,
        problems=problems,
        templates=templates,
        variants=variants,
    )

    return jinja.TemplateResponse(request, "review.html", {"job": job})


@app.post("/generate/{job_id}/{problem_idx}", response_class=HTMLResponse)
async def generate_variant(request: Request, job_id: str, problem_idx: int):
    """HTMX endpoint — return a fresh variant card partial for one problem."""
    job = get_job(job_id)
    if job is None:
        return HTMLResponse("<p>Sesión no encontrada. Vuelve a subir el archivo.</p>", status_code=404)

    tmpl = job.templates.get(problem_idx)
    if tmpl is None:
        return HTMLResponse("<p>No hay plantilla para este problema.</p>", status_code=400)

    try:
        variant = sample_parameters(tmpl)
        variant = render_prose(variant, tmpl)
        job.variants[problem_idx] = variant
    except Exception as exc:
        return HTMLResponse(f"<p>Error al generar la variante: {exc}</p>", status_code=500)

    return jinja.TemplateResponse(
        request,
        "partials/variant_card.html",
        {
            "variant": variant,
            "template": tmpl,
            "job_id": job_id,
            "problem_idx": problem_idx,
        },
    )


@app.get("/download/{job_id}", response_class=HTMLResponse)
async def download(job_id: str):
    """Render approved variants to a new .docx and return it. (Phase 4)"""
    raise NotImplementedError
