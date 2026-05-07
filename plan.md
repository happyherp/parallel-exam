# Parallel Exam Generator — Project Plan

## Purpose

Generate **parallel/equivalent variants** of math exams for make-up tests. A teacher writes a quiz; one student misses it; she needs an equivalent-but-different exam to give that student. Today she does this by hand because off-the-shelf AI tools fail in two consistent ways: changes are too minor to defeat memorization, or numbers are changed in ways that break the math (ugly fractions, no real solutions, etc.).

The target user is a math teacher in Spain, teaching 1º Bachillerato (≈Grade 11). Her source documents are Microsoft Word `.docx` files in Spanish containing native Word equations (OMML).

## Why this is hard, and why naive LLM use fails

This is a known problem in the assessment-design literature: **parallel forms** in psychometrics, **isomorphic items** in item-generation theory. Two pieces of recent research are load-bearing for our architecture:

- **PutnamGAP (arXiv 2508.08833, Aug 2025)** — generated math-equivalent variants of competition problems and showed that even strong reasoning models (Claude Sonnet 4, Gemini 2.5 Pro) lose statistically significant accuracy on the variants vs. originals. If a frontier model can't reliably *solve* its own variants, it certainly can't reliably *author* them by free-form rewriting.
- **CBIT — Computational Blueprints for Isomorphic Twins (arXiv 2511.07932, Nov 2025)** — proposes the right architectural fix: don't ask the LLM to write the variant directly. Ask it to extract a *template* (a structural skeleton with parameters and constraints), then have **code** instantiate the template under those constraints, then have a **symbolic verifier** confirm the result.

Empirical confirmation: we tested **MathQuizily**'s "VARIANTS" feature on a real problem from the target teacher's exam. It returned a Grade 9 single-step linear equation in English instead of a 1º-Bachillerato Spanish calculus problem. The product appears to be a topic+difficulty prompt-to-question generator, not an isomorphic-from-source generator. Other category-leading products (Khanmigo, MagicSchool, Conker, Questgen, 4Docent) appear to share this architecture. **The off-the-shelf tooling does not solve this problem.**

## Architecture

The pipeline is a series of transforms with one inviolable rule: **the LLM never does math, only language**. Math is done by SymPy. Verification is the gate that prevents broken math from reaching output.

```
┌─────────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ .docx input │───▶│ extract  │───▶│  parse   │───▶│ template │
│             │    │ (pandoc) │    │ (regex)  │    │  (LLM)   │
└─────────────┘    └──────────┘    └──────────┘    └─────┬────┘
                                                          │
                          ┌───────────────────────────────┘
                          ▼
                   ┌──────────────┐    ┌──────────┐    ┌────────┐
                   │   generate   │───▶│  verify  │───▶│ reword │
                   │ (constraint  │◀───│ (SymPy)  │    │  (LLM) │
                   │   solver)    │    │ retry on │    └────┬───┘
                   └──────────────┘    │  failure │         │
                                       └──────────┘         ▼
                                                      ┌────────────┐
                                                      │   render   │
                                                      │(python-docx)│
                                                      └─────┬──────┘
                                                            ▼
                                                     .docx output
```

### Pipeline stages

| Stage | Tool | LLM? | What it does |
|---|---|---|---|
| **extract** | pandoc | No | docx → LaTeX. Math preserved as native LaTeX (frac, sup, etc.) via OMML. Verified empirically. |
| **parse** | regex/text | No | LaTeX string → list of `Problem` objects (one per numbered exercise) |
| **template** | Claude | **Yes** | `Problem` → `Template`. LLM extracts function form, parameters, invariants. *Hardest piece. Build this LAST.* |
| **generate** | Python | No | `Template` → candidate parameter values. Constraint-solving / sampling. |
| **verify** | SymPy | No | Substitute candidate params, evaluate invariants, return pass/fail. **The gate.** |
| **reword** | Claude | **Yes** | Vary surface text only (variable names, contexts). Math stays fixed. |
| **render** | python-docx | No | Approved variants → output .docx |

### The two architectural commitments

**1. Templates are first-class data, not embedded prompts.** A `Template` is a pydantic model with a function form (SymPy-parseable string), parameter constraints, and invariants. The LLM produces these from problems; the constraint solver consumes them. This means:

- Templates are inspectable, editable, versionable, testable
- We can build a library of hand-written templates over time
- Each problem-type only needs to be templated once; variants are infinite
- For v1, we ship with one hand-written template and validate the architecture before tackling LLM-based template extraction

**2. Verification is non-negotiable.** `generate` produces candidate parameters. `verify` substitutes them into the template's function form and evaluates every invariant. If any invariant fails, `generate` retries with new parameters. After N failures, the problem escalates to the teacher's UI as "I couldn't make a clean variant — please edit manually." **Output is correct by construction, not by hope.** This is the architectural property that distinguishes this tool from existing failed tools.

## Worked example (for grounding)

For the rational-business-profit problem in `tests/fixtures/derivadas2.docx` (Problem 1):

> f(x) = (80x − 160) / (x² + 5) represents company profit (thousands of €) over time x (years). Find max profit, loss period, etc.

The extracted template is:

```
function_form:  (a*x + b) / (x**2 + c)
parameters:     a > 0 int, b < 0 int, c > 0 int
invariants:
  - f(0) is a negative integer  (clean initial loss)
  - numerator has positive integer root  (clean break-even)
  - f' has positive integer critical point  (clean peak year)
  - f at critical point is a positive integer  (clean max profit)
```

Solving the constraints by hand: parameterize by (k, m, n) where k = break-even year, k+m = peak year, then `a = 2mn`, `b = -ka`, `c = m² - k²`. Pick (k, m, n) = (3, 5, 7) and you get f(x) = (70x − 210)/(x² + 7), break-even at year 3, peak at year 7 with profit €5K, initial loss €30K — every output a clean integer. SymPy-verified.

This worked example should be the v0 acceptance test: upload `derivadas2.docx`, get back a valid parallel of problem 1.

## Current state

### Files in repo

- `.gitignore`
- `.github/workflows/test.yml` — CI: installs pandoc + uv, runs `pytest tests/ -v` on every push/PR
- `Dockerfile` — Python 3.12-slim base, installs `pandoc` via apt, uses `uv` for dep install
- `fly.toml` — region `mad` (Madrid), scale-to-zero, 1GB memory, port 8080
- `pyproject.toml` — deps pinned: fastapi, uvicorn, jinja2, anthropic, sympy, pypandoc, python-docx, pydantic
- `README.md` — architecture overview, pipeline diagram, phase status, quick start
- `app/__init__.py` (empty)
- `app/config.py` — pydantic-settings: `ANTHROPIC_API_KEY`, `REWORD_MODEL`
- `app/llm.py` — lazy singleton Anthropic client
- `app/main.py` — FastAPI app with 4 routes: `/`, `/upload`, `/generate/{job_id}/{problem_idx}` (all implemented), `/download/{job_id}` (Phase 4 stub)
- `app/models.py` — pydantic models: `Problem`, `ParameterConstraint`, `Invariant`, `Template`, `Variant`. **These shapes are the contract between pipeline stages.**
- `app/jobs.py` — in-memory job store keyed by UUID
- `app/pipeline/__init__.py` (empty)
- `app/pipeline/extract.py` — `docx_to_latex(path) -> str` via pypandoc
- `app/pipeline/parse.py` — `latex_to_problems(latex) -> list[Problem]`; handles pandoc's multi-block enumerate structure and free-text sub-parts
- `app/pipeline/generate.py` — `sample_parameters(template, max_attempts) -> Variant`; per-template sampler registry
- `app/pipeline/verify.py` — `verify(template, params) -> Variant`; SymPy gate, evaluates all invariants
- `app/pipeline/prose.py` — `render_prose(variant, template) -> Variant`; substitutes parameters into `prose_template`
- `app/pipeline/reword.py` — `reword_surface(variant, template) -> Variant`; LLM rewording with math preservation check and graceful fallback
- `app/pipeline/templates_library/__init__.py` (empty)
- `app/pipeline/templates_library/rational_business_profit.py` — hand-written `Template` for the rational-business-profit problem type
- `app/templates/` — Jinja2 HTML templates: `base.html`, `upload.html`, `review.html`, `partials/variant_card.html`
- `app/static/style.css`
- `tests/__init__.py` (empty)
- `tests/test_phase1.py` — 13 acceptance tests covering all Phase 1 stages (all passing)
- `tests/test_phase2.py` — 18 acceptance tests covering UI routes and prose rendering
- `app/pipeline/render.py` — `variants_to_docx()` builds a LaTeX document and calls pandoc to produce a `.docx`
- `app/pipeline/template.py` — `extract_template()` LLM-based template extraction with SymPy sanity check and parameter bound inference
- `tests/test_phase3.py` — tests for reword pipeline (mocked LLM)
- `tests/test_phase4.py` — tests for render pipeline and `/download` route
- `tests/test_phase5.py` — tests for template extraction and generic sampler (mocked LLM)
- `tests/fixtures/` — `.docx` exam files from the teacher
- `.env.example` — documents required environment variables

### All planned files created ✅

### Test fixtures (the user has these locally; copy into `tests/fixtures/`)

- `derivadas2.docx` — derivatives exam, 5 problems. Native Word equations except problem 3a/3b which are pasted PNG images.
- `derivadas3.docx` — likely teacher-made parallel of derivadas2. Same problems 1, 2, 5; varied 3, 4; adds a bonus problem.
- `Ex_Analisis_1º_Bach_.docx` — different topic (rational functions, asymptotes, piecewise continuity)
- `Ex_1º_B_Deriva_CCNN_con.docx` — was originally `.doc` containing legacy Equation Editor 3.0 OLE objects; teacher round-tripped through LibreOffice → docx and equations recovered cleanly

## Build order

Front-loaded with deterministic, testable pieces. LLM-dependent stages come last because they're the hardest to debug.

### Phase 1 — Deterministic foundation (no LLM) ✅ COMPLETE

**1.1 `app/pipeline/extract.py`**
- Function: `docx_to_latex(path: Path) -> str`
- Use `pypandoc.convert_file(path, 'latex')`
- pandoc binary is in the container via Dockerfile
- Returns full LaTeX document body
- Acceptance: round-trips `derivadas2.docx` to LaTeX containing `\frac{80x - 160}{x^{2} + 5}`

**1.2 `app/pipeline/parse.py`**
- Function: `latex_to_problems(latex: str) -> list[Problem]`
- Pandoc emits problems wrapped in `\begin{enumerate}` blocks with `\item` per problem
- Each `\item` typically starts with `\emph{\textbf{(N puntos)}}`
- Sub-parts (a, b, c) appear as separate paragraphs after the `\item`
- Build problems incrementally: each `\item` starts a new Problem, intervening text accumulates as prose, sub-parts are detected by leading `a)`, `b)`, etc.
- Acceptance: `derivadas2.docx` produces 5 `Problem` objects with correct point values and prose

**1.3 Hand-written template — `app/pipeline/templates_library/rational_business_profit.py`**
- Hardcoded `Template` instance for the rational-business-profit problem
- This unblocks 1.4 and 1.5 without depending on LLM template extraction
- Use the parameterization documented in the worked example above

**1.4 `app/pipeline/verify.py`**
- Function: `verify(template: Template, params: dict) -> Variant`
- Substitute params into `template.function_form` via `sympy.sympify`
- For each invariant, evaluate `invariant.sympy_expr` (also via sympify) against the substituted function
- Check the result matches `invariant.must_be` (integer, positive_integer, etc.)
- Return `Variant` with `verified: bool` and verification dict
- Acceptance: given the rational-business-profit template and params (a=70, b=-210, c=7), returns `verified=True` with f(0)=-30, break-even=3, peak=7, max=5

**1.5 `app/pipeline/generate.py`**
- Function: `sample_parameters(template: Template, max_attempts: int = 50) -> Variant`
- For the v1 hardcoded template: parameterize by (k, m, n) integers in reasonable ranges, derive (a, b, c), call `verify`. Return first verified variant.
- For future templates: each template will need a domain-specific search strategy. Consider whether a generic constraint-solver wrapper (z3? brute force?) is worth it later. For v1, per-template sampling is fine.
- Acceptance: returns a different verified variant each call with different (k, m, n)

**End of Phase 1** ✅: full pipeline minus LLM works on derivadas2 problem 1. 13 tests passing. No UI yet.

### Phase 2 — UI shell ✅ COMPLETE

**2.1 `app/templates/base.html`, `upload.html`, `review.html`** — Jinja2, HTMX-driven. KaTeX (CDN, `https://cdn.jsdelivr.net/npm/katex@0.16.x/dist/`) for math rendering on the page.

**2.2 Implement `/upload` and `/generate` routes in `main.py`** — call the Phase 1 pipeline, render template variants in HTML cards, HTMX swaps the card on regenerate.

**2.3 In-memory job store keyed by UUID** — no database needed for v1. Jobs expire after 1 hour. Document the decision; persistence can come later.

**End of Phase 2** ✅: teacher can upload derivadas2.docx, see problem 1 with a generated variant, click regenerate to get a different variant.

### Phase 3 — Surface text rewording ✅ COMPLETE

**3.1 `app/config.py`** — pydantic-settings for `ANTHROPIC_API_KEY` and `REWORD_MODEL`. `.env.example` documents required vars.

**3.2 `app/llm.py`** — lazy singleton Anthropic client; raises `RuntimeError` with a helpful message if the API key is not configured.

**3.3 `app/pipeline/reword.py`**
- Function: `reword_surface(variant: Variant, template: Template, language: str = "es") -> Variant`
- LLM call using `claude-haiku-4-5` (cheapest model; accurate enough for surface rewording). System prompt is prompt-cached to reduce token costs on repeated calls.
- Prompt instructs the model to keep all `\(...\)` LaTeX blocks verbatim while varying the applied context (e.g., "empresa" → "fábrica", "beneficios" → "producción").
- Post-condition: `_math_preserved()` extracts all math blocks from mechanical prose and LLM output and asserts they are identical. If the LLM altered any math, the output is rejected and mechanical prose is used.
- Falls back to mechanical prose silently on any error (missing key, network, rate limit) so the pipeline is never blocked.
- Integrated automatically into `/upload` and `/generate` routes — the variant card always shows reworded prose when the API key is set.

### Phase 4 — Output ✅ COMPLETE

**4.1 `app/pipeline/render.py`**
- Function: `variants_to_docx(problems, templates, variants, output_path)`
- Pandoc-reverse approach: construct a UTF-8 LaTeX document from the variant prose (which already has `\(...\)` inline math), write it to a temp `.tex` file, then call `pandoc --from=latex --to=docx`. Pandoc generates OMML equations in the docx automatically — no XSLT or `latex2mathml` needed.
- For problems with verified variants: renders the reworded prose + student tasks from the template.
- For problems without variants: passes the original `Problem.prose_latex` and sub-parts through unchanged.
- Acceptance: output file has valid zip/docx magic bytes; renders cleanly in LibreOffice and Word.

**4.2 `/download/{job_id}` route**
- Generates the docx on-demand, streams it as a `FileResponse`, deletes the temp file in a `BackgroundTask` after the response is sent.
- Response includes a human-readable filename (`{original_stem}_variante.docx`) in `Content-Disposition`.
- Download button added to the review page header.

### Phase 5 — LLM template extraction ✅ COMPLETE

**5.1 `app/pipeline/template.py`**
- Function: `extract_template(problem: Problem) -> Template | None`
- Calls `claude-sonnet-4-6` with Anthropic's tool-use feature so the response is guaranteed to match our pydantic schema (no JSON parsing / repair needed).
- System prompt (~2.5 KB) explains the Template structure with the rational-business-profit problem as a worked example. The prompt is prompt-cached so repeated calls in a session amortise the cost.
- After the LLM returns, the extracted template is run through `verify()` against the original numerical parameters provided by the model. If a single invariant fails on the source values, the LLM made a structural mistake and the template is rejected.
- Bound inference: after passing the sanity check, parameter constraints are post-processed so each parameter's `min`/`max` brackets the original value (default ±4×|original|, with a floor of ±30). This lets the generic brute-force sampler search a productive region of parameter space rather than the default `[-30, 30]` cube.
- Falls back to None on any failure (missing API key, network, schema mismatch, verification rejection) so the pipeline degrades gracefully.

**5.2 Generic brute-force sampler**
- `app/pipeline/generate.py::_generic_sampler()` is the fallback when no per-template sampler is registered. Uses random integer search over the parameter constraints (sign + min/max).
- Default budget is 50× the per-template budget (≥ 2500 attempts) because LLM-extracted templates often have restrictive invariants like "f' has integer critical point" that need many tries.
- Known limitation: very tightly constrained templates (e.g. 6+ invariants involving solve(diff(...))) may exhaust the budget on subsequent regenerations. v1 accepts this — the teacher edits manually when no variant can be generated. A smarter solver (z3, smt) is post-v1 work.

**5.3 Integration with `/upload`**
- `_find_template()` (library heuristic) is tried first — fastest, highest quality, hand-tuned per template.
- If no library template matches, `extract_template()` is the fallback. Each LLM call adds ~3-10 seconds to upload time; the cost is acceptable for v1.

**End of Phase 5** ✅: every problem in an uploaded exam attempts to get a verified variant. Variants either come from a library template (best path), an LLM-extracted template that passes verification (good path), or fall through to "edit manually" (graceful degradation).

## Stack & deployment

- **Backend**: Python 3.12, FastAPI, uvicorn
- **Frontend**: Jinja2 + HTMX (no build step, no SPA framework)
- **Math rendering (browser)**: KaTeX via CDN
- **Math engine (server)**: SymPy
- **Doc parsing**: pypandoc (system pandoc binary)
- **Doc generation**: python-docx + pandoc-reverse for math
- **LLM**: Anthropic Claude (model TBD per stage; sonnet for rewording, opus for template extraction)
- **Container**: single Docker image, python:3.12-slim base
- **Host**: Fly.io, Madrid region, scale-to-zero
- **Auth**: none (v1)
- **Storage**: in-memory job store (v1); add S3/Tigris later if needed
- **Package manager**: `uv`

## Hard rules (do not violate)

1. **The LLM never does math.** Template extraction and surface rewording are the only LLM calls. Numbers come from the constraint solver. Verification comes from SymPy.
2. **Verification is the gate.** No variant reaches the user without `Variant.verified == True`. If verification fails N times, escalate to the teacher's UI; do not output a "best effort" broken variant.
3. **The reword step must not modify math.** Post-condition check: extracted equations match input equations. If they don't, reject.
4. **One canonical input format: `.docx`.** Reject anything else with a clear error message. PDF and image input are explicitly out of scope. Legacy `.doc` files: instruct user to round-trip through LibreOffice. Do not attempt server-side LibreOffice in v1.
5. **No persistent storage in v1.** In-memory only. Document this in README.

## Open questions / deferred decisions

- **Template extraction quality** for problem types outside our hand-written library. Will likely need per-problem-type prompt tuning. Defer until Phase 5.
- **Image-embedded equations** (e.g., derivadas2 problem 3a/3b are PNGs). These extract from pandoc as `\includegraphics{...}` references, not LaTeX. Either OCR them in v2 (Mathpix or vision LLM) or surface them in the UI as "this problem contains an image-formula; please retype manually." Lean toward the latter for v1.
- **Persistence**: when the in-memory job store becomes a problem (browser refresh loses state, scaling beyond one machine), add a database. Probably SQLite first (Fly volumes), Postgres later if needed.
- **Auth**: defer until there's a real reason. A shared password env var would be enough for early users.
- **Multi-language**: v1 is Spanish-only. Spanish is hardcoded in the reword prompt. Generalize later.
- **OMML output fidelity**: the docx output path may have subtle rendering issues. Test with both Word and LibreOffice. Acceptable to ship v1 with "renders correctly in LibreOffice; Word may have minor formatting differences."

## Key technical insights from prior work

- **`.docx` math is OMML**, structured XML. Pandoc converts it to clean LaTeX. We've verified this on the test fixtures.
- **`.doc` files claiming to be Word are sometimes RTF in disguise.** The `file` command reveals this.
- **Legacy `.doc` with Equation Editor 3.0 objects** (`\objclass Equation.3` in RTF) cannot be read by pandoc or LibreOffice headless on Linux. Fix: open in LibreOffice GUI and save as `.docx`. The conversion happens silently and recovers the equations.
- **The chat interface's `<documents>` block flattens math** when text-extracting attached files. Don't trust inline previews of uploaded math docs; always re-read via pandoc.
- **The teacher's parallel-form style** (visible in derivadas2 vs derivadas3): she keeps applied/word problems verbatim and varies only the mechanical-calculation problems. Worth surfacing as a default in the UI: an "this problem will not be varied" toggle, defaulted on for problems with rich applied context.

## Acceptance test for v1

Given `tests/fixtures/derivadas2.docx`:

1. Upload via UI → upload succeeds, redirects to review page
2. Review page shows 5 problems extracted, with their LaTeX rendered via KaTeX
3. Problem 1 (the rational-business-profit problem) has a "Generate variant" button; clicking it produces a verified variant with different (a, b, c) and clean integer outputs, rendered side-by-side
4. Clicking "Regenerate" produces a different valid variant
5. Click "Approve" → variant is staged for output
6. Click "Download" → returns a `.docx` file containing the approved variant, opens cleanly in Word and LibreOffice with formulas intact

Problems 2–5 can fall through to "no template available — please edit manually" in v1; they'll be picked up as the template library grows.