"""FastAPI app entry. HTMX-style server-rendered HTML, no SPA."""

from pathlib import Path
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")

app = FastAPI(title="Parallel Exam Generator")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Upload form."""
    return templates.TemplateResponse(request, "upload.html", {})


@app.post("/upload", response_class=HTMLResponse)
async def upload(request: Request, file: UploadFile = File(...)):
    """Receive .docx, extract problems, show review page.

    Pipeline:
        extract.docx_to_latex(file) -> str
        parse.latex_to_problems(latex) -> list[Problem]
        for each problem: template.extract(problem) -> Template
        store in session/memory under a job_id
    """
    raise NotImplementedError


@app.post("/generate/{job_id}/{problem_idx}", response_class=HTMLResponse)
async def generate_variant(request: Request, job_id: str, problem_idx: int):
    """HTMX endpoint — returns just the variant card partial.

    Pipeline:
        generate.sample_parameters(template) -> dict
        verify.verify(template, parameters) -> Variant   # retries on failure
        reword.reword_surface(variant, template) -> str  # LLM call
    """
    raise NotImplementedError


@app.get("/download/{job_id}", response_class=FileResponse)
async def download(job_id: str):
    """Render approved variants to a new .docx and return it."""
    raise NotImplementedError
