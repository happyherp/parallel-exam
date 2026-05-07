"""FastAPI app entry. HTMX-style server-rendered HTML, no SPA."""

from __future__ import annotations

import re
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, Request, UploadFile
from fastapi.background import BackgroundTasks
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.jobs import create_job, get_job
from app.pipeline.extract import docx_to_latex
from app.pipeline.generate import sample_parameters
from app.pipeline.parse import latex_to_problems
from app.pipeline.prose import render_prose
from app.pipeline.render import variants_to_docx
from app.pipeline.reword import reword_surface
from app.pipeline.template import extract_template
from app.pipeline.templates_library import LIBRARY

BASE_DIR = Path(__file__).parent
jinja = Jinja2Templates(directory=BASE_DIR / "templates")

# Convert the small subset of LaTeX text-mode commands that pandoc emits into HTML.
def _latex_prose_filter(text: str) -> str:
    text = re.sub(r"\\textsuperscript\{([^}]*)\}", r"<sup>\1</sup>", text)
    text = re.sub(r"\\textsubscript\{([^}]*)\}", r"<sub>\1</sub>", text)
    return text

jinja.env.filters["latex_prose"] = _latex_prose_filter

app = FastAPI(title="Parallel Exam Generator")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


# ── Template library ─────────────────────────────────────────────────────────

def _find_template(prose_latex: str) -> Template | None:
    """Return the first matching library Template, or None."""
    for tmpl, matcher in LIBRARY:
        if matcher(prose_latex):
            return tmpl
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
        # Equation Editor 3.0 (OLE objects) produces no parseable LaTeX math.
        # Heuristic: pandoc output has text but almost no \( math delimiters.
        math_count = latex.count(r"\(")
        extra = (
            " Parece que el documento usa las Ecuaciones antiguas de Word"
            " (Equation Editor 3.0). Ábrelo en LibreOffice Writer, ve a"
            " Archivo → Guardar como → .docx, y vuelve a subir el archivo convertido."
            if math_count < 2
            else ""
        )
        return jinja.TemplateResponse(
            request,
            "upload.html",
            {"error": f"No se encontraron problemas numerados en el documento.{extra}"},
            status_code=422,
        )

    # Match against the hand-written library (fast, deterministic).
    # LLM-based extraction is deferred to the first /generate call for each problem.
    templates: dict[int, object] = {}
    variants: dict[int, object] = {}

    for i, problem in enumerate(problems):
        tmpl = _find_template(problem.prose_latex)
        templates[i] = tmpl
        if tmpl is not None:
            try:
                variant = sample_parameters(tmpl)
                variant = render_prose(variant, tmpl)
                variant = reword_surface(variant, tmpl)
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
    """HTMX endpoint — return a fresh variant card partial for one problem.

    If no template is stored yet (lazy-load path), tries LLM extraction first.
    """
    job = get_job(job_id)
    if job is None:
        return HTMLResponse("<p>Sesión no encontrada. Vuelve a subir el archivo.</p>", status_code=404)

    tmpl = job.templates.get(problem_idx)

    # Lazy LLM extraction: only runs when the user clicks "Generar variante".
    if tmpl is None:
        problem = job.problems[problem_idx]
        tmpl = extract_template(problem)
        job.templates[problem_idx] = tmpl

    if tmpl is None:
        return HTMLResponse(
            "<p>No se pudo extraer una plantilla para este problema."
            " Edítalo manualmente.</p>",
            status_code=400,
        )

    try:
        variant = sample_parameters(tmpl)
        variant = render_prose(variant, tmpl)
        variant = reword_surface(variant, tmpl)
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


@app.get("/download/{job_id}")
async def download(job_id: str, background_tasks: BackgroundTasks):
    """Render current variants to a .docx and stream it to the browser."""
    job = get_job(job_id)
    if job is None:
        return HTMLResponse("Sesión no encontrada. Vuelve a subir el archivo.", status_code=404)

    # Write to a named temp file; FileResponse streams it, then we delete it.
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as fh:
        out_path = Path(fh.name)

    try:
        variants_to_docx(job.problems, job.templates, job.variants, out_path)
    except Exception as exc:
        out_path.unlink(missing_ok=True)
        return HTMLResponse(f"Error al generar el documento: {exc}", status_code=500)

    stem = Path(job.filename).stem
    download_name = f"{stem}_variante.docx"

    background_tasks.add_task(out_path.unlink, missing_ok=True)

    return FileResponse(
        path=out_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=download_name,
    )
