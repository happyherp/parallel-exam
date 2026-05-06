# Parallel Exam Generator

Generate **parallel / equivalent variants** of math exams for make-up tests.
A teacher writes a quiz; one student misses it; she needs an equivalent-but-different exam.
This tool does that correctly — without changing the difficulty or breaking the math.

## Why this is hard

Existing AI tools fail in two ways: changes are too minor to defeat memorisation, or numbers are changed in ways that break the math (ugly fractions, no real solutions).
This project follows the **CBIT** architecture (Computational Blueprints for Isomorphic Twins): the LLM never does math — it only extracts structure and rewrites surface text.
Math is done by SymPy; every output is verified before it reaches the teacher.

## Pipeline

```
.docx input ──▶ extract ──▶ parse ──▶ template ──▶ generate ──▶ verify ──▶ reword ──▶ render ──▶ .docx output
               (pandoc)   (regex)     (LLM)      (Python)    (SymPy)    (LLM)   (python-docx)
```

The one inviolable rule: **the LLM never does math**.
Numbers come from the constraint solver.
Verification is the gate — no variant reaches the teacher unless `Variant.verified == True`.

## Status

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Deterministic foundation (extract, parse, verify, generate) | ✅ Done |
| 2 | UI shell (upload, review page, HTMX) | Planned |
| 3 | Surface text rewording via LLM | Planned |
| 4 | .docx output via python-docx + pandoc | Planned |
| 5 | LLM-based template extraction | Planned |

## Quick start

```bash
# Requires Python 3.12+ and pandoc
pip install -e .

# Run the test suite
pytest tests/ -v

# Start the dev server
uvicorn app.main:app --reload
```

The app will be available at `http://localhost:8000`.

## Input format

Only `.docx` files are accepted.
Legacy `.doc` files must be round-tripped through LibreOffice first (open → Save As → .docx).
PDF and image input are out of scope for v1.

## Storage

v1 uses an **in-memory job store** keyed by UUID.
Jobs expire when the server restarts — there is no persistent storage.
This is intentional; persistence will be added (SQLite → Postgres) when it becomes a real need.

## Stack

- **Backend** — Python 3.12, FastAPI, uvicorn
- **Frontend** — Jinja2 + HTMX (no build step)
- **Math engine** — SymPy
- **Doc parsing** — pypandoc (system pandoc binary)
- **Doc output** — python-docx + pandoc
- **LLM** — Anthropic Claude (sonnet for rewording, opus for template extraction)
- **Deployment** — Fly.io, Madrid region (`mad`), scale-to-zero
