# Robustness of LLMs in Mathematical Reasoning (arXiv:2508.08833)

*Source: iclr2026_conference.tex*

---

## Abstract

In this paper, we introduce a systematic framework beyond conventional methods to assess LLMs’ mathematical‑reasoning robustness by stress‑testing them on advanced math problems that are mathematically equivalent but with linguistic and parametric variation. These transformations allow us to measure the sensitivity of LLMs to non-mathematical perturbations, thereby enabling a more accurate evaluation of their mathematical reasoning capabilities. Using this new evaluation methodology, we created PutnamGAP, a new benchmark dataset with multiple mathematically-equivalent variations of competition-level math problems. With the new dataset, we evaluate multiple families of representative LLMs and examine their robustness. Across 18 commercial and open-source models we observe sharp performance degradation on the variants. OpenAI's flagship reasoning model, O3, scores 51.5 % on the originals but drops by 4.7 percentage points on surface-renaming variants, and by 12.9 percentage points on parametric variants, while smaller models fare far worse. Overall, the results show that the proposed new evaluation methodology is effective for deepening our understanding of the robustness of LLMs and generating new insights for further improving their mathematical reasoning capabilities.

## Introduction

**Motivation.**
Modern AI systems are increasingly entrusted with tasks that hinge on robust reasoning rather than pattern matching.
It is thus important to

precisely measure an LLM’s reasoning capacity and its ability to generalize beyond memorized textual surface forms. Existing math-reasoning benchmarks, however, exhibit two critical weaknesses: (i) leakage-induced score inflation, since benchmark items rapidly seep into pre-training corpora, and (ii) limited robustness coverage, because today’s datasets are too small or lack controlled transformations that probe true generalization. Addressing these weaknesses is urgent if we aim to benchmark reasoning with the same rigor demanded in safety-critical domains such as healthcare or cybersecurity.

**Benchmark inflation through training leakage.**
Recent studies show that public datasets, including GSM8K [Cobbe:2021] and MATH [hendrycks:2021], have leaked into the web‑scale corpora used to pre‑train large language models (LLMs), artificially inflating test‑time accuracy. A leaderboard score therefore no longer guarantees genuine reasoning ability; it may merely reflect memorization of benchmark items or their solutions. Simply releasing *yet another* dataset postpones the problem: once its items enter future training corpora, scores climb without real progress. What is needed is a *systematic method* that (i) measures a model’s capacity to generalize beyond verbatim memory and (ii) can generate an unbounded supply of evaluation items, limiting future leakage.

[Figure*: PutnamGAP variants performance relative to the original set (ref: fig:overview)]

**Competition mathematics reveals the next robustness bottleneck.**
Large language models (LLMs) now surpass 90% accuracy on widely‑used
benchmarks such as GSM8K and
MATH, prompting claims of
“near‑human” numerical reasoning yet still falter on Olympiad‑style or Putnam‑level problems that intertwine multiple domains.
Existing Putnam‑derived datasets are too small to expose this gap: Putnam‑AXIOM (236 originals + 52 variations) [huang:2025], and PutnamBench (640 formalized theorems) [tsoukalas:2024] remain in the hundreds, and none delivers systematic generalization and perturbations.
These facts expose Weakness (i) insufficient scale and Weakness (ii) lack of controlled, systematic transformations in existing evaluations.

**Existing perturbation-based robustness benchmarks.**
Recent work has begun to probe mathematical robustness by constructing perturbation-based benchmarks on top of GSM8K and related datasets. GSM-Plus augments GSM8K with eight families of adversarial variations per problem, revealing large accuracy drops even for models that nearly solve the original benchmark [Li:2024GSMPlus]. GSM-Symbolic builds symbolic templates over GSM8K-style problems and shows that merely changing numeric instantiations or adding logically irrelevant clauses can degrade performance by up to 65% [Mirzadeh:2024GSMSymbolic]. MathCheck-GSM further organizes GSM8K-derived problems into a checklist of task and robustness variants to study behavior across multiple evaluation formats [Zhou:2024MathCheck]. Beyond GSM8K, GSM8K\_MORE uses an ontology of perturbations to generate families of grade-school arithmetic variants [Hong:2025GSMore], while Putnam-AXIOM introduces a smaller set of functional variations for university-level Putnam problems [gulati:2025]. These efforts convincingly demonstrate that current LLMs are brittle under controlled perturbations; however, GSM-derived benchmarks remain confined to grade-school or pre-university word problems with short, single-answer numerical solutions and are built directly on GSM8K and related datasets that are already near-saturated and affected by training data contamination for frontier models [Cobbe:2021,gulati:2025,Shalyt:2025,glazer:2024], while Putnam-AXIOM introduces only a relatively small companion set of functional variants (100 over 522 problems) . Consequently, the existing perturbation benchmarks do not yet provide a large-scale, systematically structured robustness test for competition-level, proof-style mathematics.

**Generalization–and–Perturbation (GAP) framework for robustness evaluation.**

We address both leakage and robustness by
*stress-testing the model on mathematically equivalent versions of the same
problem*.
For a problem \(x\) with solution set \(S(x)\) and an LLM \(f\),
robustness is the expected accuracy when \(x\) is transformed by a family
\(T\) of equivalence-preserving operators.
We partition \(T\) into
\(T_surf\) (surface renames that alter symbol salience)
and \(T_para\) (kernel rewrites that preserve the same proof steps while changing the scenario and parameters).
This **GAP** framework (i) creates an *infinite* stream of *unseen* test items, mitigating future contamination, and (ii) quantifies how far a model can generalize beyond memorized surface
forms. In our setting, GAP serves as a general diagnostic evaluation methodology for analyzing and quantifying the robustness of an LLM's mathematical reasoning capacity at the level of competition problems.

**Limitations of existing perturbation benchmarks.** Several recent robustness benchmarks - such as GSM-Symbolic, GSM-Plus, and MathCheck -

**PutnamGAP: instantiating GAP on 85 years of problems.**
We instantiate GAP on every William Lowell Putnam Competition problem
from 1938–2024 (**1,051** originals) and expand each item into five
variants—four surface renames and one kernel rewrite—obtaining
**6,306** stress‑test questions. A two‑stage QA pass—15 rounds of o3 self‑review plus a 10% spot‑check found no substantive errors.

**Headline results.**
Across 18 models, as shown figure [fig:overview], all of them suffer from both simple renaming and step-based rewrites.
OpenAI’s o3 scores 51.5% on original statements but loses
**4.7 pp (9.12%)** under surface renames and **12.9 pp (25.22%)** under parametric rewrites.
These drops confirm that high leaderboard scores can collapse when
cosmetic or structural perturbations are applied—precisely the effect that data leakage masks.

**Contributions.**
**(1)** We propose *GAP*, a novel general framework for measuring
robustness via mathematically equivalent transformations that overcomes two common deficiencies of the current evaluation methods (i.e., data leakage and lack of robustness measures).
**(2)** We release *PutnamGAP*, the first 6k‑scale competition
benchmark that systematically disentangles surface‑level and structural generalization while limiting future leakage.
**(3)** We provide the first comprehensive robustness baseline across eighteen LLMs, plus an open‑source evaluation stack.

## The Generalization–and–Perturbation (GAP) Framework

### Evaluation Model

We start from a curated set of $N$ *canonical items* $P=\(x_i,y_i,_i)\_i=1^N$, where $x_i$ is a problem statement, $y_i$ is its reference answer(s), and $_i$ an unreleased expert solution path used internally for safe variant generation.
**Model interface.**
A language model $f_$ receives a prompt $x$ and returns $y=f_(x)$, which an automatic checker maps to a binary label $z=grade(y,y)\0,1\$.

**Variant families.**
For every $x_i$ we later apply *two* disjoint transformation super-families (defined in the next section but *left unchanged here*): $T_i^surf$ ($K_surf$ surface variants), $T_i^para$ ($K_para$ parametric variants). Each surface transformation $$ returns a new statement $x_i^()=(x_i)$ that preserves semantic correctness of $y_i$. For parametric variations, $y_i$ is transformed as well to match $(x_i)$.

**Evaluation matrix.**
The Cartesian product $D=\(i,)iN,\;T_i^surfT_i^para\id\\$ contains $N(K+1)$ aligned items (original + $K$ variants per source, $K = K_surf+K_para$). Running $f_$ on every pair populates a binary matrix $Z\0,1\^N(K+1)$. From the first column we extract the *easy* vector $e()\0,1\^N$, while the remaining columns feed family-specific aggregates: $h^surf()=maj(Z_[:,\,surf])$, $h^para()=Z_[:,\,para]\!$. The set of surface variants can be changed based on specific tasks.

**Robustness Metric**.

Let $e,h\0,1\^N$ denote per-item correctness on the *easy* (original) and *hard* (variant) sets.
With Jeffreys smoothing

$$
p_e=_j e_j+12N+1,p_h=_j h_j+12N+1,=12(p_e(1-p_e)+p_h(1-p_h)).
$$

Define the SD-normalized drop $d_j=(e_j-h_j)/$ and its soft-saturated version
$d_j=1k\!(1+e^k d_j)$ with $k0.5$.
Let $d=median\d_j\,|\,d_j>0\$
(with fallback $d:=(,median|d_j|)$, $=0.1$ when no positive drop exists) and set $=2/d$.
Our *penalty* robustness is

$$
R(e,h)=1N_j=1^N \!(-\,d_j)(0,1].
$$

Thus $R=1$ indicates invariance; a “typical” loss ($d_jd$) halves the per-item factor,
while improvements ($d_j<0$) are clamped to zero penalty (no reward).
We report $R_surf=R(e,h_surf)$, $R_para=R(e,h_para)$, and $R_global=R_surfR_para$. **Full derivation, statistical justification, and design discussion are in Appendix B.**

### Transformation Families

**The proposed general robustness measures can work for any variations.** As a first step in exploring this new evaluation methodology, we propose and study *five* aligned variants—
four *surface renamings* that perturb only symbol names,
and one *core‑step* instance that perturbs numeric slots while
preserving the reasoning chain.  This section details the synthesis
pipelines. Detailed descriptions can also be found in Appendix A.

#### Surface renaming variant family

[Figure: Surface renaming variant family pipeline (ref: fig:surfgap)]

We want to know whether a model recognizes an argument *because it has truly abstracted the pattern* or merely because it memorizes suggestive identifier strings. Therefore we systematically replace each token tagged `var` or `param`; all constants of category `sci\_const` remain untouched.

**Automated pipeline.**
[label=**.**]

- **Proposal.** A single call to o3 receives the token role ("free variable" or "fixed parameter") and the surrounding textual context, and returns a candidate replacement.

- **Collision check.** A deterministic post-validator rejects names colliding with any pre-existing identifier in the problem.

- **Family tagging.** The string is labelled as belonging to one of four families described below.

We use four types of surface variants: `Descriptive\_Long` (DL), with a single descriptive phrase; `Descriptive\_Long\_Confusing` (DLC), with 2–5 random unrelated nouns; `Descriptive\_Long\_Misleading` (DLM), with a mathematically suggestive but misleading term ; `Garbled\_String` (GS), with a 4–16-character hash, as shown in figure [fig:surfgap] where `Q' stands for the problem question and `A' stands for the official solution.

Each source item thus yields $4$ surface variants; accuracy deltas per family appear in Section Results & Analysis.

#### Parametric variant family

[Figure: Parametric variant family pipeline (ref: fig:paragap)]
 Symbol renaming probes only the lexical axis. To probe *structural transfer*, we resample numerical constants yet force the solution to reuse the original high-level moves. In this work, we call it `Kernel\_Variant` (KV). We convert each item into semantically-equivalent variants through a four-stage pipeline: (1) **slot discovery**; (2) **template back-synthesis**; (3) **question reverse-engineering**; and (4) **dual-verifier screening** (two-in-a-row rule). The pipeline generates a bounded number of validated variants for each problem within a few hours on commodity hardware using the OpenAI o3 API. See Appendix A for empirical bounds and details of our implementation.

### Implementation Overview

**Code release.**
To facilitate double‑blind reviewing we publish *only* the subset of
data (100 randomly chosen examples).
An automated evaluator, `putnam-cli.py`, receives the names of target solver model and grader model and variant type to test.
Supported back‑ends are (i) any HuggingFace‐compatible checkpoint via
`transformers`, (ii) a local `vllm` server, or (iii) API clients including OpenAI, Gemini, Anthropic and OpenRouter.
Full data and generation scripts will be released post‑decision.

**Surface generation.**
Renaming variants are produced on a CPU‑only node by streaming  o3
API calls.
A five‑stage *exponential‑back‑off* retry (max 5 attempts, doubling
timeout each time) masks transient API latency.
Processing all $1\,051$ items in parallel takes $$15 min wall‑clock.

**Core‑step generation.**
Kernel variant synthesis is more
expensive because of multi‑turn chain‑of‑thought reasoning:
end‑to‑end runtime is \(
\!3\,h
\)
for the full corpus on a single 8‑core CPU, dominated by the
15‑iteration repair‑and‑verify loop.

## PutnamGAP Dataset

### Data Sources, Extraction & Annotation

Our benchmark comprises all **Putnam Problems 1938–2024**
($N=1\,051$ items after deduplication). See Appendix E for source details.

Original scans are processed via a 3-stage OCR routine:
(i) Manual segmentation for every question-answer pair.
(ii) *MathPix* for formula‐aware PDF-to-LaTeX conversion
followed by
(iii) custom post-filters that merge multi-line expressions and fix
\ 4.2 % residual symbol errors.
Each item is manually spot-checked ($$2 min per problem) to ensure semantic
fidelity before variant generation.
**Complete corpus list, OCR accuracy study, and cleaning scripts appear in
Appendix E.**

### Dataset Statistics

**Overall scale and balance.**
The benchmark comprises **1,051** original Putnam problems
from 1938–2024 and five mathematically equivalent transformations, yielding **6,306** items.
Part distribution is balanced (**527 A** vs.\ **524 B**),
and the canonical identifier
$year*, *part*\A,B\, *index*$
provides a difficulty proxy.  Using indices
$1\!\!-\!2$ as *Easy*,
$3\!\!-\!4$ as *Medium*,
and $5\!\!-\!6$ as *Hard*,
the corpus contains
32.3\,% Easy, 32.3\,% Medium, 32.2\,% Hard,
plus a 3.0\,% extra–hard tail (indices 7–8).

**Topic coverage and Quality Control**
Automatic tags in `\_meta.tag` indicate broad mathematical
coverage—Algebra (641), Analysis (521), Number Theory (392),
Combinatorics (286), and Geometry (239). 803 of the questions are proofs, and 248 of them are calculations. At the same time, every item has undergone single‐pass manual validation.

## Experimental Setup

The constructed PutnamGAP dataset enables, for the first time, a robust analysis of an LLM's reasoning capacity. In this section, we describe how we set up the experiments to evaluate the robustness of 18 representative models.

### Model Pool & Prompting

We evaluated 18 models (see [tab:updated_model_scores_pct] or Appendix A for a complete list).All models are queried under a unified **zero‑shot template**.
A system instruction designates the model as *“an expert
mathematician”* and asks it to *show all work*, while the user
message embeds the problem. See Appendix G for our full prompt.
We fix `temperature`=0, `top\_p`=1, and
`max\_tokens`=32000 or maximum token amount available in case some models have `max\_tokens` maximum smaller than 32000. for every run except OpenAI O-series which require `temperature`=1.
Solutions are then re‑submitted to a second template that grades the
answer: a strict proof rubric for proof items and a
lenient numeric rubric for calculation items.
Both grader prompts require structured JSON output containing a binary
`grade` field plus detailed feedback.  Complete prompt code is available in Appendix G

### Scoring & Auto-Grader

We partition tasks into *computation* and *proof*
categories and evaluate them with distinct graders.

**Computation**
Each candidate answer is normalized (whitespace, units, LaTeX macros)
and passed to two scoring paths:
(i) a strict string match against the reference solution;
(ii) a *latent* grader—an LLM prompted to return
"`CORRECT"` or "`INCORRECT"` given the reference
answer and a rubric that disallows partial credit.
We adopt path (ii) to mitigate formatting artifacts; if the two paths
disagree we mark the item for manual audit (<1% of cases).

**Proof**
We provide the grader with an aligned, step-by-step reference proof and
ask it to assign a binary `grade` plus a natural-language
justification.  Any skipped logical step or missing citation triggers a
fail.  A random 10 % sample is double-checked by independent volunteers;
grader precision/recall is $>$97 %.

## Results & Analysis

### Robustness

  round-mode              = places,
  round-precision         = 3,
  table-number-alignment  = center,
  table-format            = 1.3,
  detect-weight           = true,
  detect-family           = true

[Table*: Model Accuracy Rates across Categories (Percent Scale) (ref: tab:updated_model_scores_pct)]


We evaluated 18 different LLMs on this benchmark, and results are summarized in Table [tab:updated_model_scores_pct]. For each variation of the model, we used a paired design (McNemar’s exact test) on matched problem pairs to test whether the accuracy rate decreases significantly compared to the original. Statistically significant differences are indicated using standard notation ($p<0.1$, $p<0.05$, $p<0.01$). We also computed 95 % CI (See Appendix D Figure [fig:overview] ) and our proposed robustness metrics $R$ (see Appendix B), and all models, especially those performed well on the original set.

We observe that almost all variants lead to a decrease in model accuracy, even when the transformation is merely changing the names of the variables. This indicates a notable lack of robustness: models often lack the capability to preserve their accuracy under mathematically identical but surface-modified representations. Particularly, transformations that rely on variable-name reasoning (such as Misleading or Garbled String) tend to disturb the model’s math accuracy most severely.

[Table: Robustness metrics \(R_surf (ref: tab:robustness_flat_two_block)]

Because the surface score aggregates the four renaming variants by per–item majority, the flip probability from the original to the aggregated surface set is suppressed; accordingly, \(R\!\!1\) is expected and should be interpreted as an approximate upper bound on surface invariance (see Table [tab:robustness_flat_two_block]). Practitioners can implement alternative mapping functions based on their model’s performance while retaining this core formulation. Across capable models we consistently observe \(R_para<R_surf\), and we summarize stress–type invariance via \(R_global=R_surfR_para\). Interpreting \(1-R\) as a penalty mass highlights nontrivial fragility even when raw accuracy is high. Conversely, for weak models a high \(R\) is not evidence of robustness: when base accuracy \(p_e\) is small, the pooled SD \(=12\!(p_e(1-p_e)+p_h(1-p_h))\) and the bound \(1-R\p_e,1-p_h\\,(1-q)\) with \(q=(-d_b+)\) limit the observable penalty, so \(R1\) reflects low headroom rather than invariance. Reporting both accuracy and \(\R_surf,R_para,R_global\\) therefore stabilizes cross–model comparison under mathematically equivalent stress and shows that robustness remains limited despite strong performance on canonical phrasing.

Another observation is that if a model is not robust to one variant, it tends to be not robust to other variants as well. Notable examples include kimi-k2, claude-opus-4, and gemini-2.5-pro.

### Transformation-wise Breakdown

**Descriptive Long (DL)**
The impact of this transformation is smallest overall: drops are marginal and mostly not significant. Some models such as o3 (+1.3), o4-mini(+1.5), and Qwen3-235B (+1.1) even improved slightly. This indicates that descriptive renaming preserving accuracy.

**Confusing (DLC)**
Long, semantically meaningless variable names moderately reduce accuracy. Models like Claude-opus-4 (–4.3***) and GPT-4o-mini (–1.8***) showed significant drops.

**Misleading (DLM)**
Replacing variables with misleading strings strongly hurts math accuracy. Nearly all models experienced a significant drop. Notably, Claude-Opus-4 (–4.8***), Gemini-2.5-pro (–5.6***), and Claude-Sonnet-4 (–4.4***) were among the most heavily affected.

**Garbled String (GS)**
Random character strings consistently degrade performance: every model
loses accuracy, over half significantly. Models such as Gemini-2.5-pro (–5.4***), Claude-Sonnet-4 (–4.9***), and Gemini-2.5-flash-lite (–4.7***) suffered the largest declines.

**Kernel Variant (KV)**
Kernel variants—which keep each question’s mathematical structure but replace constants and expressions with different values—led to the sharpest decline overall. All models experienced large drops, often in the range of –5 to –15 points, with Grok4 (–14.6***), Gemini-2.5-flash (–15.2***), and Gemini-2.5-pro (–14.9***) showing the steepest declines.\

Overall, state-of-the-art LLMs show inconsistent performance under semantics-preserving transformations and appear sensitive to superficial cues. This is consistent with the possibility that part of their gains reflects data-leakage–related memorization rather than stable mathematical reasoning. The pattern persists across topics and problem classes: bar plots with \(95%\) CIs (Appendix D, fig. [fig:overview]) and per-topic/per-class breakdowns (Appendix D, figs. [fig:types]-[fig:classes]) show similar robustness gaps across Algebra/Analysis/NT/Combinatorics/Geometry and for both proof and calculation items.

### Error Taxonomy

Our grading script returns a brief comment for every incorrect answer. Using these comments, we grouped errors into four categories: *Symbol Confusion*, *Step Omission*, *Arithmetic*, and *Logic Hallucination*. Figure [Error Composition] in Appendix D shows that the relative frequency of these error types is nearly identical across variants; logic hallucinations dominate, accounting for roughly three-fifths of all wrong answers regardless of prompt wording. Thus, the accuracy drop is distributed across all categories rather than driven by a single one, confirming that mathematically equivalent perturbation  consistently degrades LLM performance.

### Qualitative case studies of Kernel Variant failures

To complement the aggregate robustness metrics, we performed a small-scale qualitative analysis of Kernel Variant (KV) failures. We ran a GPT-based analyzer over model traces and automatically selected ORIGINAL/KV pairs where a strong model solves the ORIGINAL correctly but fails on the KERNEL-VARIANT; concrete case studies are deferred to Appendix I.

Across these examples we see three recurring KV-specific failure modes. First, *hallucinated algebraic infrastructure and missing premises*: in items such as 1938-B-1 and 1940-A-6 the KV solutions invoke strong algebraic identities or valuation equalities (e.g., $adj M = (M)M^-1$ or $v_i(JF)=e_i-1$) without checking that the hypotheses hold in the stated ring or characteristic, whereas the ORIGINAL proofs stay within a valid algebraic framework. Second, *computing the wrong global quantity after mostly correct setup*: in 1939-A-1, 1940-A-7, and 1940-B-7 the KV traces correctly identify the relevant points or bounds but then switch from arc length to chord length or from a clean monotonicity argument to a mis-indexed summation, producing false inequalities despite reasonable intermediate calculus or algebra. Third, *fragile geometric reductions and inconsistent conventions*: in 1939-B-1, 1939-B-7, 1940-A-2, and 1938-A-7 the KV arguments rely on incorrect symmetry reductions, ignore degenerate edge cases (e.g.\ $=0$), or briefly adopt sign conventions that contradict earlier definitions before silently reverting.

Overall, these qualitative patterns corroborate the quantitative gap $R_para < R_surf$. Kernel Variants do not merely inject harder arithmetic; they stress the model’s ability to re-bind parameters and maintain a coherent proof skeleton under resampled slots. When the model fails KV, it often does so by reusing an ORIGINAL template outside its domain of validity or by quietly changing the quantity or symmetry being computed (see Appendix I for detailed traces).

### External Validation

We applied our surface-renaming protocols—**DLC** and **GS**—to ALG514  [kushman-etal-2014-learning]. Accuracy decreased from Base 93.6% to DLC 90.9% (\(=-2.7\) pp) and GS 89.3% (\(=-4.3\) pp); McNemar tests (Base vs DLC: \(b=24,c=10,p=0.024\); Base vs GS: \(b=35,c=13,p=0.002\)). These statistically significant drops indicate that GAP's surface-renaming stress tests generalize to other math datasets and reveal nontrivial sensitivity to variable renaming.

## Discussion

### Key Findings

The proposed GAP framework allowed us to make the following new findings about the behavior of LLMs in performing mathematical reasoning:

**Symbol-level perturbations cause substantial drops.**
Across the four *surface* variants—DL, DLC, DLM, and GS—merely renaming variables lowers accuracy by $3–5$\,pp on average; for example, Gemini-2.5-pro falls from 78.3% to 72.9% (–5.4\,pp; see Table [tab:updated_model_scores_pct]).
This indicates that today’s SOTA models still rely on lexical "semantic anchors" rather than fully abstract proof structures.

**Maintaining structure but resampling parameters is even harsher.**
The Kernel Variant (KV) simultaneously resamples all mutable constants while preserving the original reasoning skeleton.
Accuracy losses reach $10$\,pp; OpenAI O3 declines from 51.5% to 38.6% (–12.9\,pp), showing that grasping a solution pattern does not automatically translate to parameter-invariant reasoning ability.

$R_global$ reveals fine-grained brittleness. We compute $R_surf, R_para, R_global$ where $R(,)$ is the SD–normalized robustness metric.
Because it exponentially penalizes rare but catastrophic flips, $R_global$ tracks *effective* robustness more faithfully than a plain hard/easy accuracy ratio.

Takeaway.* Across capable models we consistently observe \(R_para<R_surf\), and we summarize stress-type invariance via \(R_global=R_surfR_para\); interpreting \(1-R\) as penalty mass highlights non-trivial fragility even when raw accuracy is high.

### Implications

**A novel evaluation methodology:**
The GAP framework provides a novel methodology for analyzing and evaluating the robustness of LLMs' reasoning capacity by generating an (in principle) unbounded supply of semantically equivalent test items, which can limit future benchmark leakage and mitigate leaderboard inflation.

**Improving robustness via curriculum fine-tuning:**
Our results suggest curriculum fine-tuning that explicitly randomizes *(i)* symbol identities and *(ii)* numeric parameters, instead of simply enlarging pre-training corpora. That is, we can leverage the GAP framework to augment data for fine-tuning a model to improve robustness.

**Detecting potential security concerns:**
Surface-level fragility implies that production systems can be *prompt-injected* with mathematically innocuous renamings—highlighting the need to integrate robustness checks into red-team pipelines. Our evaluation framework enables such risk analysis before deploying any production system.

Reporting.* We recommend reporting bootstrap CIs for \(R_b\) together with per-item histograms of SD-normalized drops \(d_j=(e_j-h_j)/\); these visualize tail-risk (rare catastrophic flips) that raw accuracy masks and make robustness audits reproducible.

## Related Work

There have been multiple benchmarks for evaluating the mathematical-reasoning capabilities of large language models (LLMs). Early math‐reasoning benchmarks such as MATH(1.25 k problems) [hendrycks:2021], and GSM8K(8.5 k problems) [Cobbe:2021], revealed basic arithmetic/algebra skills. But their difficulty is now saturated as LLMs scale. For instance, with prompting strategies such as DUP, GPT-4 attains 97.1% accuracy on GSM8K [zhong:2025]. This ceiling at the high-school-competition level motivated the creation of a new generation of harder benchmarks.

Subsequent benchmarks target harder problems. Omni-MATH contributes 4 428 rigorously annotated Olympiad-level problems [gao:2024]. Likewise, OlympiadBench provides a bilingual, multimodal benchmark of 8 476 Olympiad-level math and physics problems with expert step-by-step solutions [he:2024]. The cross-disciplinary benchmark ARB consist questions in mathematics, physics, biology, chemistry, and law, with a rubric-based self-grading protocol [sawada:2023]. Some other benchmarks focuses specifically on formal proof. MiniF2F supplies 488 Olympiad-level problems formalized in multiple proof assistants [zheng:2022].  Putnambench, offers 1 692 rigorously hand-crafted formalizations of Putnam Competition problems [tsoukalas:2024].

Nevertheless, recent studies warn that scores on many NLP benchmarks may be artificially inflated by data contamination, when LLMs are trained on the benchmark questions. sainz:2023 point out that many benchmarks may be inflated because large language models often memorize test data seen during pre-training.  balloccu:2024 conduct a systematic audit of data leakage for closed-source LLMs and estimate that roughly 4.7 million test examples from 263 datasets were likely exposed to the models.

Preventing data leakage is central to obtaining a robust evaluation of LLMs’ reasoning capabilities. One approach is to construct entirely original problems: for example, FrontierMath provides a rigorously curated benchmark of hundreds of original, expert-level mathematics problems spanning fields from number theory to algebraic geometry [glazer:2024]. Another strategy is to introduce contrast sets—small, label-changing perturbations of existing test instances—to probe a model’s local decision boundary [gardner:2020]. Within this perturbation paradigm, GSM-Plus, GSM-Symbolic, MathCheck-GSM, and GSM8K\_MORE all build on GSM8K [Cobbe:2021], augmenting grade-school word problems with adversarial numeric, lexical, and contextual variations and revealing substantial robustness failures [Li:2024GSMPlus,Mirzadeh:2024GSMSymbolic,Zhou:2024MathCheck,Hong:2025GSMore]. At higher difficulty, huang:2025 construct MATH-Perturb by applying simple and hard perturbations to 279 level-5 MATH problems, Shalyt:2025 introduce ASyMOB, a 17k-problem benchmark focused on algebraic symbolic operations with numerical and symbolic perturbations, yu:2025 propose Math-RoB, a synthetic benchmark that uses instruction-based modifications to expose reasoning gaps under data contamination, and Putnam-AXIOM combines 522 original Putnam problems with 100 functional variants obtained by perturbing variables and constants [gulati:2025]. Collectively, these benchmarks demonstrate that current LLMs are far from robust, but GSM-based variants remain at grade-school arithmetic level on benchmarks that are increasingly saturated and contaminated for frontier models [Cobbe:2021,gulati:2025,Shalyt:2025,glazer:2024], MATH-Perturb and ASyMOB target relatively narrow slices of mathematics (hard MATH items and symbolic algebra, respectively), Math-RoB relies on synthetic instruction-style perturbations that are not strictly mathematically equivalent, and existing Putnam variants form only a small companion set to the original (potentially contaminated) problems.

Building on these prior efforts, we adopt a Generalization–and–Perturbation (GAP) framework that addresses both data leakage and robustness by generating mathematically equivalent variants of complex problems and jointly evaluating models on originals and variants. The framework is agnostic to any particular dataset and can in principle be applied to existing and future benchmarks, and to both proof-style and short-answer questions, to strengthen their reliability. To move beyond saturated, pre-university settings, we apply GAP to challenging college-level competition mathematics problems. Concretely, we instantiate GAP on every William Lowell Putnam Competition problem from 1938–2024 (1\,051 originals), expanding each item into five mathematically equivalent variants and thereby producing PutnamGAP, a corpus of 6\,306 stress-test questions. Finally, we release an open-source evaluation stack that rigorously grades solutions step by step, making assessment fully automated, transparent, and reproducible.

## Conclusion & Future Work

Robust reasoning is required in many applications of LLMs. In this paper, we proposed a novel **Generalization–and–Perturbation (GAP)** framework for analyzing and evaluating robustness of LLMs' reasoning capacity.   By instantiating GAP on *all* 1,051 Putnam Competition questions we produced the 6,306‑question PutnamGAP benchmark. A zero‑shot evaluation of 18 commercial and open‑source LLMs revealed sharp and consistent accuracy drops.  These results expose a clear robustness gap that leaderboard scores on unperturbed datasets have so far not shown.

Our findings highlight three actionable directions.


- *Benchmarking*: GAP offers an open‑ended supply of contamination‑resistant test items, limiting future data leakage and score inflation.

- *Training*: curricula that randomize both symbol identities and numeric parameters during fine‑tuning should become standard practice for models targeting formal reasoning domains.

- *Security*: the same surface‑level fragility that hurts accuracy can be weaponized for prompt‑injection attacks, so GAP‑style mutation should be built into red‑teaming pipelines.

There are multiple interesting future research directions based on our work: (i) diversify the verifier ensemble with symbolic provers and heterogeneous LLMs to rule out collusive blind spots, (ii) port GAP to applied mathematics, physics and multi-modal STEM corpora, and (iii) integrate on‑the‑fly GAP transformations into training so that invariance to symbol and parameter changes is learned rather than merely tested.

PutnamGAP makes one lesson unmistakable: genuine progress in mathematical AI will be measured not by ever‑higher raw scores, but by a model’s ability to stride across the hidden gulf between *symbols* and *substance*.  The next generation of top‑tier systems will earn their place only by refusing to be left behind on GAPs.

---

iclr2026_conference
iclr2026_conference

---

## Appendix A

To disentangle *symbol sensitivity* from *reasoning transfer*,
we create two orthogonal families of meaning‑preserving variants for each
canonical item $x_i$.  Surface
variants alter only the `var` / `param` strings, whereas
core‑step variants resample numerical constants while enforcing the
original logical skeleton.

### Surface Variants

We probe symbol‑level generalisation by automatically renaming every
`var` or `param` token extracted during pre‑processing,
while keeping all scientific constants (`sci\_const`) fixed.  A
single call to o3 proposes a replacement conditioned on the
token role (“free variable’’ vs.\ “fixed parameter’’), and a
post‑validation step rejects any collision with existing identifiers.

For each original problem we synthesise *four* independent renaming
families and instantiate exactly one variant per family, yielding in
total $1\,0514=4\,204$ surface items.  The families are:

- **Descriptive‑Long (DL).**
      A single, meaningful English phrase
      (e.g.\ |populationDensity|).
      Accuracy on DL is empirically indistinguishable from the original
      and therefore serves as a sanity check.

- **Descriptive‑Long‑Confusing (DLC).**
      A concatenation of 2–5 unrelated words
      (e.g.\ |walnutVioletTerrace|),
      designed to overload working memory without changing semantics.

- **Descriptive‑Long‑Misleading (DLM).**
      A phrase built from *mathematical jargon* that suggests a
      different concept—e.g.\ |primeFieldOrder| used as a real
      variable—to test whether models latch onto spurious lexical cues.

- **Garbled‑String (GS).**
      A 4–16 character alphanumeric hash
      (e.g.\ |xcQ7h2ZfRw9v|), eliminating any linguistic hint.

### Core‑step Variants

While surface renaming stresses symbol recognition, we also wish to test
whether a language model can transfer the *reasoning skeleton* to a
numerically distinct yet logically equivalent instance.  For every
original item we therefore generate a single **core‑step variant**
via the four‑stage pipeline:

- **Slot discovery** Forward $(x_i,_i)$ to o3;
      it lists every constant whose value is not logically fixed,
      emitting a `mutable\_slot` dictionary with human‑readable
      descriptors (e.g.\ “neighborhood half‑width $D$”).

- **Back‑synthesis** Each slot is resampled *uniformly*
      within a guard range derived from the problem’s own inequalities,
      yielding $\D,k,...\$. We feed
      $x_i,`slots`,_i,`mutable\_steps`$
      back to o3; it fills the new constants and regenerates a
      proof whose step order matches `mutable\_steps`, along with
      the fully worded problem statement.

- **question reverse-engineering** Once the full solution is processed successfully, we put the value from the solutions back into the original question, and thus generate our `Kernel\_Variant`

- **dual-verifier screening** Five o3 judge instances,
      each with an independent temperature seed, must *all* return
      “solvable and correct”. A rejection auto-triggers patching and
      re‑verification. After three consecutive clean passes we perform a
      10% human audit.

The output artifact, denoted `kernel\_variant`, stores the new
statement, regenerated proof, slot dictionary, and preserved
core‑step list.  Exactly one kernel variant is produced per source
item, totaling $1\,051$ items.

### Theoretical Guarantees

The variant pipeline combines stochastic LLM generation with a
*repair‑and‑verify* loop (Algorithm [alg:loop]).
Although 76.4\,% of the corpus are proof‑based items—i.e.\ cannot be
validated by simple numeric inequalities—we prove that the acceptance
criterion yields an exponential safety margin.

Notation
Each candidate undergoes at most
\(T = 15\) verification iterations.
Within one iteration \(t\) we launch
\(J = 5\) independent o3 judges, each returning
`accept` (1 bit) or `reject`.
Denote by
\(=[judge mis‑accepts a flawed candidate]\).
In a random audit of 25 rejected variants we observed
one false decision, hence we conservatively set \(=0.04\).

An iteration \(t\) is *passed* when all
\(J\) judges vote `accept`.
A candidate is *accepted* by the pipeline if it passes in *two
consecutive* iterations; otherwise the loop either repairs the artifact
or aborts after 15 attempts.  A 10% manual audit follows.

\(\)‑Soundness under two‑in‑a‑row rule

Let \(K=2\) be the required streak length.
Under independent‑judge assumption the probability that an
*unsolvable or incorrect* variant survives the pipeline is bounded
by

$$
\;\;
  (T-K+1)\;^\,KJ
  \;=\;
  14\;^10
  \;\;
  14(0.04)^10
  < 10^-10.
$$

The pipeline examines at most \(T\!-\!K\!+\!1=14\) distinct
length‑\(K\) windows \(t,...,t+K-1\).
For a flawed candidate to be accepted, *every* judge in
*both* iterations of some window must err, an event of probability
\(^KJ\).  A union bound over all windows yields the claim.

Why not pre‑computed guard ranges?
Because the majority (76.4\,%) of items require multi‑step proofs, the
notion of “feasible numeric interval’’ is ill‑defined.  We therefore
rely on the **rejection‑sampling loop** in
Algorithm [alg:loop]; Theorem [thm:soundness] shows that its
soundness is already more stringent than \(10^-9\), rendering an extra
symbolic guard unnecessary.

Reasoning‑step isomorphism

Stage 3 forces the regenerated proof to match the abstract skeleton
`mutable\_steps` step‑by‑step, hence every accepted core‑step
variant is isomorphic to the source solution \(_i\) under the
identifier mapping introduced in
Section [sec:transforms-core].  A regex verifier found zero
mismatches over all 1\,051 core variants.

Practical impact
Even if the true judge error rate were twice our empirical estimate
(\(=0.08\)), the bound remains
\(<10^-8\).
Thus all reported robustness numbers are *statistically safe* from
false positives introduced by the generation machinery.

---

## Appendix B

Motivation.
Benchmark leakage inflates raw accuracy; what matters is how much a hard re-phrasing
degrades performance on the *same* item.\;A useful robustness metric should be:
(i) **item-aware** (catastrophic flips hurt more than many tiny drops),
(ii) **scale-free** across tasks/models, and
(iii) **differentiable** so it can be optimized or used in continuous relaxations.
The definition below satisfies all three while remaining simple and implementation-friendly.

### Notation and Jeffreys Smoothing

Let $e,h\0,1\^N$ be per-item correctness on the *easy* (original) and *hard* (variant) sets.
To avoid boundary pathologies, we use Jeffreys smoothing (Beta$(12,12)$ prior):

$$
p_e=_j e_j+12N+1,p_h=_j h_j+12N+1.

$$

Define the pooled Bernoulli SD

$$
=12(p_e(1-p_e)+p_h(1-p_h)).

$$

*Rationale.* Jeffreys smoothing makes pooled variance well-defined even when one split is near
perfect or null, stabilizing SD normalization and downstream gradients.

### SD-normalized Per-item Drop and Soft Saturation

For aligned item $j$, define the SD-normalized drop

$$
d_j=e_j-h_j.

$$

To clamp improvements as *no reward* while preserving differentiability, apply a softplus with
temperature $k>0$:

$$
d_j=1k\!(1+e^k d_j),k0.5.

$$

Properties: $d_j0$; $_kd_j=\d_j,0\$;
$d_jd_j=\!(k d_j)(0,1)$ (logistic).

### Data-driven Slope: “Typical-loss halves’’

Let $d=median\d_jd_j>0\$ denote the median *positive* drop.
If no positive drop exists, fallback to $d:=(,median|d_j|)$ with $=0.1$.
Choose an exponential slope so that a “typical” loss halves the factor:

$$
=2d.

$$

### Per-item Penalty and Aggregate Robustness

Map each item to an exponential penalty

$$
r_j=(-\,d_j)(0,1],

$$

and define the *penalty robustness*

$$
R(e,h)=1N_j=1^N r_j
=1N_j=1^N \!(-2d\,d_j)(0,1].

$$

*Interpretation.* $R=1$ indicates invariance; a “typical” loss ($d_jd$)
contributes a factor $12$; improvements ($d_j<0$) are clamped to zero penalty (no upward reward).

### Basic Properties (Monotonicity, Sensitivity, Bounds)

- **Range.** $r_j(0,1]$ $$ $R(0,1]$.

- **Permutation-invariance.** $R$ depends on the multiset $\d_j\$ only.

- **Monotonicity.** If $d_j$ increases for any $j$, then $d_j$ increases, hence $r_j$ decreases;
thus $R$ is non-increasing in each $d_j$.

- **Catastrophe sensitivity.** Because $d_j$ grows at least linearly for large positive $d_j$ and enters
an exponential, a few large flips dominate many tiny drops (convex penalty).

- **Scale-free.** $d_j$ is SD-normalized (Eq. [eq:dj]); $$ (Eq. [eq:beta]) auto-calibrates to the empirical difficulty of the model–dataset pair.

- **Continuity.** With $k>0$ and Jeffreys smoothing, $R$ is continuous in $(e,h)$ and differentiable almost everywhere in the binary case; fully differentiable when $e_j,h_j[0,1]$.

Closed-form toy cases.
(1) If $m$ items flip from correct to wrong ($e_j=1,h_j=0$) and others unchanged with $$ constant,
then $d_j=1/$ on the $m$ items, $0$ otherwise; hence
$R 1-mN(1-2^-1/\,)$ where $=d_jd_j(0,1)$ depends on $k$.
(2) If some items improve ($d_j<0$), they contribute $r_j1$ (clamped), so $R$ does not exceed $1$.

### Why Not the Hard/Easy Ratio or Plain $$?

A naive ratio $A_h/A_e$ is undefined/unstable when $A_e\!\!0$ and treats “many tiny drops” $$ “few huge drops”.
In contrast, $R$ aggregates *per-item* SD-normalized drops and exponentially penalizes rare catastrophes.
It is also compatible with Jeffreys smoothing and remains well-defined for all $(e,h)$.

[Table: Side-by-side comparison of hard/easy accuracy ratio with our penalty (ref: tab:ratio-vs-R)]

### Relation to Effect Sizes (Paired Design)

Dropping the soft saturation and clamping gives $d_j=(e_j-h_j)/$.\;Averaging yields

$$
1N_j d_j
=p_e-p_h12(p_e(1-p_e)+p_h(1-p_h))
d_Cohen,
$$

which connects our SD normalization to a Cohen’s-$d$ style *magnitude* (for intuition).
Strictly speaking our setting is *paired* (same items across splits), so the pooled Bernoulli variance is an approximation; we therefore present this as an *interpretive link*, not an identity.

### Complementary Paired Significance Tests

While $R$ is an effect-like robustness index, significance on paired binaries is best tested with *McNemar*:

$$
^2=(n_10-n_01-1)^2n_10+n_01,=n_10n_01,CI:  \!(z_/21n_10+1n_01),
$$

where $n_10$ counts (orig correct, variant wrong) and $n_01$ counts the reverse.
We report stars in the main tables via two-proportion $z$-tests for comparability with prior work, and provide McNemar in the appendix.

### Soft-probability Variant and Gradients

Let $e_j,h_j[0,1]$. With $$ treated as a stop-gradient constant in backprop (to avoid median non-differentiability),

$$
Re_j
=1N_i=1^N[-\,e^-d_i\,(k d_i)\,d_ie_j],
$$

where for $i=j$,

$$
d_je_j
=1-(e_j-h_j)^2e_j,
e_j=1-2p_e4(N+1),
$$

and for $ij$,

$$
d_ie_j
=-(e_i-h_i)^2e_j.
$$

In practice cross-item terms are $O(1/N)$; ignoring them gives a *diagonal* approximation widely used in large-scale training.

### Concentration and CIs for $R$

Since $r_j(0,1]$, Hoeffding gives, for any $t>0$,

$$
(R-ERt)2(-2Nt^2).
$$

A conservative $(1-)$ CI is $R(2/)2N$ (ignoring the small dependence of $r_j$ on $$ across items).
For reporting, we recommend bootstrap CIs over items.

### Edge Cases and Implementation Notes

- **No positive drops.** Use the fallback $d:=(,median|d_j|)$; then $=2/d$ remains finite and $R1$.

- **Near-degenerate variance.** Jeffreys smoothing in Eq. eq:jeffreys avoids $0$ even for extreme accuracies.

- **Temperature $k$.** $k[0.3,1]$ yields similar rankings; we set $k=0.5$ by default.

- **Streaming computation.** One pass over items suffices once $p_e,p_h$ (hence $$) are cached.

### Pseudocode for Robustness Estimator

[Algorithm: Computation of $R$ (ref: alg:robustness)]

### Archived Symmetric Form (Not Used in Main Results)

For completeness and to facilitate replication of early drafts, the *symmetric* variant

$$
R_sym(e,h)=1N_j \!(-e_j-h_j)
$$

can exceed $1$ when improvements occur. We do *not* use $R_sym$ in the main paper; the penalty form $R$ avoids rewarding improvements and keeps $R(0,1]$ by construction.

Takeaway. The penalty form $R$ is the reportable index; $R_sym$ is archived for ablations only.

---

## Appendix C

### Algorithm for Parametric Variants LLM Self-Check Process

[Algorithm: Repair‑and‑verify loop (excerpt) (ref: alg:loop)]

---

## Appendix D

### Supplementary Figures

[Figure: Accuracies of each variant per model bar plot with 95% CI (ref: fig:overview)]

[Figure: Error composition ratio across variants (ref: Error Composition)]

[Figure: Problem topics and classes (ref: fig:enter-label)]

[Figure: Accuracies of five types of questions for each variant per model (ref: fig:types)]

[Figure: Accuracies of two classes of questions for each variant per model (ref: fig:classes)]

[Figure: Robustness by model (ref: fig:placeholder)]

---

## Appendix E

### Data Source

We obtain every official problem of the *William Lowell Putnam
Mathematical Competition* from 1938 to 2024 by digitizing the four
authoritative monographs shown in Table [tab:putnam-books].
Each volume is issued by the **Mathematical Association of America
(MAA)** and reprinted by the **American Mathematical Society (AMS)**
under the *MAA Press Problem Books* series. (footnote:
Softcover and e-book reprints are available from
https://bookstore.ams.org.)

[Table: Primary sources for PutnamGAP.  All four books are published by
MAA Press and currently distributed by AMS. (ref: tab:putnam-books)]

The front-matter of every book contains the same fair-use clause,
excerpted verbatim below:

2pt

2pt

This clause grants us the legal right to reproduce problems and
solutions for non-commercial academic evaluation.  In line with AMS
policy, we distribute only machine-readable IDs and LaTeX texts; raw
PDF scans remain under the original AMS license, and any further
redistribution must be cleared through the Copyright Clearance Center.

Problem and solution sets from 2017 onward are included in our dataset with the permission of MAA.

Across the early era (1938–1941) the competition featured $6$–$8$
problems per part (A and B); from 1942 onward the
format stabilised at $5$–$6$ problems per part, with difficulty
increasing monotonically from position 1 to 6. (footnote:
A few years, such as the wartime years 1943–1945, were canceled; our index skips these
years.)
These historical variations are preserved in our metadata and later
support the difficulty-gradient analysis in section **Statistics**

### Extraction & Annotation Pipeline

Our raw sources are scanned PDFs; no machine‑readable \ is
provided.  We therefore build a **four‑stage pipeline** that
converts each page into a fully annotated problem record suitable for
variant generation and automatic scoring.

1.\ Image segmentation & OCR.
Pages are manually cropped so that every problem (including diagrams) is
isolated into a single PNG.  We then send the image to
`MathPix`, receiving  that compiles without error.
Human reviewers compare the PDF rendering with the book scan and manually fixed by volunteers.

2.\ Minimal \ normalisation.
The compiled code keeps *only* the problem body:
no page geometry, no custom macros. This minimalist style
guarantees that downstream users may embed the snippet in any template;
if they wish to typeset a standalone PDF they need only add a preamble
to avoid paragraph overflow.

3.\ Semantic annotation via LLM
Given the cleaned “problem +\!  solution’’ pair, we prompt OpenAI's
o3 model to extract three kinds of metadata:

- **Topical tags** drawn from problem categories $\ALG,NT,
      COMB,GEO,ANA\$.
      The tag most central to the pivotal lemma is stored as the unique
      `type`.  These tags allow
      users to filter, e.g.\ “geometry only’’ subsets.

- **Symbol inventory** $\`var`,`param`,
      `sci\_const`\$:
      `var` denotes free variables, `param` denotes numeric
      parameters fixed in the statement, and `sci\_const` collects
      immutable objects like $$ or $e$.  During surface‑variant
      generation we replace only `var`/`param` so that
      scientific constants remain intact.

---

## Appendix F

### LLM usage

We used LLMs for 2 proposals:


- Finding relevant works;

- Polishing sentences, checking grammar, and adjusting layouts.

### Why ALG514?

We also tried to implement GAP method on better-known math datasets such as GSM8K [Cobbe:2021] and MATH [hendrycks:2021]. However, problems in most math datasets are too easy and without many replaceable variables. Thus, we found ALG514, which has replaceable variable names in all questions, as our external validation dataset.

### Practical Recommendations

Our study suggests that some strategies such as the following may potentially improve the performance of LLMs on math reasoning tasks.


- **Data augmentation.** Randomly apply $T_surfT_core$ during training to force symbol-invariant reasoning.

- **Symbol binding.** Separate *identifier* tokens from *literal* tokens (e.g., via a learnable symbol table) inside the Transformer.

- **Hybrid reasoning.** Embed SMT/CAS validators into decoding (e.g., value-head alignment) to tighten logical consistency.

### Compute & Reproducibility

All inference were performed through *publicly available APIs*.  Each
model was queried **exactly once per item** with the hyper-parameters
in Table [tab:updated_model_scores_pct]. Runs were executed from a single
Ubuntu 22.04 host (11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz); no local GPU was
used.  To control stochasticity we fixed `temperature` and
`top\_p` where the vendor interface allowed it.

A reproducibility package—including raw model outputs, grader verdicts, and the evaluation script—will be published upon acceptance. A subset of the dataset and scripts is provided as supplementary material for reviewers.

### Other observations

- Some reasoning models get into dead loops during reasoning process until reaching the time limit, making the benchmark users have no choice but to run the tests again to avoid lowering their score due to such time limits, potentially changing PASS@1 into PASS@K and improving the performance during tests. Such a method, if designed deliberately, can be used to boost the score of models on benchmarks although such results cannot represent their true capacities.

- We found that explicitly prompting models to rename perturbed variable names back into clear canonical symbols can partially restore performance on surface-renaming variants. We ran a small preliminary experiment and coducted an inference on the results using McNemar test. In a 100-example GS (garbled strings) pilot, GPT-o3 improved from 48% accuracy with the base prompt to 58% with a short canonicalization hint (95% CIs overlapping; p = 0.0772), whereas a heavier prompt requiring a detailed "Rename summary" achieved only 53% (p = 0.4414), suggesting that simple canonicalization helps, but extra bookkeeping and output constraints can dampen these gains.

[Table: Accuracy of a strong model on 100 GS variants under different prompting conditions.]

---

## Appendix G

---

## Appendix H

---

## Appendix I

This appendix provides a 4 1930s' concrete ORIGINAL vs.\ Kernel-Variant (KV) examples for a strong model(o3) from the instances we examined, complementing the aggregate robustness metrics in Section 5. The examples were restricted to cases where the model solves the ORIGINAL correctly but fails on the KERNEL-VARIANT, and we manually verified the failure annotations.

## 1938-B-1

### Original question

    8. Take either (i) or (ii).

(i) Let \(A_ik\) be the cofactor of \(a_ik\) in the determinant

$$
d
=|

|.
$$

Let \(D\) be the corresponding determinant with \(a_ik\) replaced by \(A_ik\).
Prove that \(D = d^3\).
(*page 86*)

(ii) Let \(P(y)=A y^2+B y+C\) be a quadratic polynomial in \(y\).
If the roots of the quadratic equation \(P(y)-y=0\) are \(a\) and \(b\) \((a b)\),
show that \(a\) and \(b\) are roots of the biquadratic equation

$$
P(P(y)) - y = 0.
$$

Hence write down a quadratic equation which will give the other two roots,
\(c\) and \(d\), of the biquadratic.

Apply this result to solving the following biquadratic equation:

$$
(y^2-3y+2)^2
-3(y^2-3y+2)
+2 - y = 0.
$$

### O3 solution on original

(ii)Iterating a quadratic and locating its 2-cycle

**1.\; Notation and preliminaries**

Let \(P(y)=A y^2+B y+C\) with \(A0\).
Put

$$
f(y)=P(y)-y = A y^2 + (B-1)y + C 1
$$

and

$$
F(y)=P(P(y)) - y.
$$

\((f)=2\), \((F)=4\).

**2.\; The fixed points propagate to the second iterate**

If a root \(a\) of (1) satisfies \(f(a)=0\), then \(P(a)=a\). Hence,

$$
F(a)=P(P(a)) - a = P(a) - a = 0,
$$

so every root of (1) is also a root of \(F\).
Thus two of the four roots of \(F\) are \(a,b\) (assumed \(ab\)).

**3.\; Dividing \(F(y)\) by \(f(y)\)**

We look for a quadratic \(g(y)=p y^2+q y+r\) such that

$$
F(y)=f(y)\, g(y). 2
$$

Write \(Q(y)=P(y)=A y^2+B y+C\).

A short expansion gives

$$

F(y)=\;&
A^3 y^4
+ 2A^2B\, y^3
+ (A B^2 + 2A^2C + A B) y^2 \\
&+ (2ABC + B^2 - 1) y + (A C^2 + B C + C).

$$

Comparing the coefficients of \(y^4\) and \(y^3\) in (2)–(3) fixes

$$
p = A^2, q = A(B+1).
$$

Matching the \(y^2\) and constant coefficients then gives

$$
r = AC + B + 1.
$$

Consequently,

$$
g(y)=A^2 y^2 + A(B+1) y + (AC + B + 1). 4
$$

Therefore,

$$
P(P(y)) - y
=
(P(y)-y)\,
(A^2y^2 + A(B+1)y + (AC+B+1)). 5
$$

**4.\; The other two roots**

The remaining roots \(c,d\) of \(F(y)=0\) are exactly the roots of

$$
A^2 y^2 + A(B+1) y + (AC + B + 1) = 0. 6
$$

**5.\; Application to the given biquadratic**

The given equation is

$$
(y^2-3y+2)^2
-3(y^2-3y+2)
+2 - y = 0,
$$

i.e.\ \(P(y)=y^2-3y+2\) with \(A=1,\; B=-3,\; C=2\).

*(a) Roots fixed by \(P(y)\)*

$$
P(y)-y = y^2 - 4y + 2 = 0
y = 2 2
$$

so \(a = 2+2,\; b = 2-2\).

*(b) Quadratic for the 2-cycle*

Insert \(A=1, B=-3, C=2\) into (6):

$$
y^2 + (-2)y + (2 - 3 + 1)
=
y^2 - 2y
=
0
y(y-2)=0.
$$

Thus \(c=0,\; d=2\).

**6.\; Verification (optional)**

$$

y=0:&P(0)=2,P(P(0))=P(2)=0 \;\; F(0)=0,\\
y=2:&P(2)=0,P(P(2))=P(0)=2 \;\; F(2)=0.

$$

Hence the biquadratic splits as

$$
(y-(2+2))(y-(2-2))\, y (y-2)=0.
$$

All four solutions are

$$
y\0,\;2,\;2+2,\;2-2\.
$$

### Kernel variant

Let \(n=5\). All matrices are \(55\) and all equalities hold in the
polynomial ring

$$
R = Z[a_ik]
$$

obtained by adjoining the \(25\) independent indeterminates \(a_ik\) to \(Z\).

**1.\; Preliminaries**

- \(= (a_ik)\) original matrix

- \(d = \) its determinant

- \(A_ik\) cofactor of \(a_ik\) in \(d\)

- \(= (A_ik)\) cofactor matrix (not transposed!)

- \(= ^T = adj \) classical adjugate

- \(= adj\) adjugate taken twice

Recall two well-known facts valid for every square matrix \(M\) of size \(n\):

$$
(F1)M adj M
=
adj M M
=
(M)\, I_n.
$$

$$
(F2)If \(M\) is not a zero-divisor in the ground ring, then
adj M = (M)\, M^-1. 1
$$

Because the determinant \(d\) of \(\) is an irreducible (hence non-zero)
polynomial in \(R\), it is not a zero-divisor; consequently we may use (1) for
both \(\) and \(\).

2.\; Proof of (i): \(= d^4\)

We have \(= adj\), so by (F1)

$$
= = d I_5. 2
$$

Taking determinants in (2) and using \((d I_5) = d^5\), we obtain

$$
()() = d^5
= d^5d = d^4.
$$

Because \(\) and \(\) differ only by a transpose, they have the same
determinant; hence

$$
= = d^4. $$

3.\; Proof of (ii): \(= d^3\)

Since \(\) is invertible when \(d 0\) and \(= d^4\),
identity (1) gives

$$
adj=
()\, ^-1
=
d^4 (1/d)\,=
d^3.
$$

But both sides are polynomial matrices whose entries coincide on the open set
\(\d0\\); therefore they are identical in the polynomial ring \(R\).
Hence

$$
= d^3 . $$

**4.\; Proof of (iii)**

*(a) Determinant of \(\).*

From (ii) we have \(= d^3\), so

$$
= (d^3)
= (d^3)^5 = d^15. $$

*(b) Rank and right-kernel when \(d 0\).*

If a specialisation of the indeterminates yields a numerical matrix with
\(d 0\), then \(\) is invertible; hence

$$
rank= 5,
() = \0\.
$$

Because \(= d^4\), the same specialisation also gives
\(0\), so \(\) is invertible, whence

$$
rank= 5,
() = \0\.
$$

Thus \(\) and \(\) have the same rank and the same right-kernel; explicitly, for every column vector \(v\),

$$
v = 0
v = 0
v = 0. $$

All three requested statements (i)–(iii) are thereby established.

### O3 solution on KV

Let \(n=5\). All matrices are \(55\) and all equalities hold in the
polynomial ring

$$
R = Z[a_ik]
$$

obtained by adjoining the \(25\) independent indeterminates \(a_ik\) to \(Z\).

**Preliminaries.**

- \(= (a_ik)\) original matrix

- \(d = \) its determinant

- \(A_ik\) cofactor of \(a_ik\) in \(d\)

- \(= (A_ik)\) cofactor matrix (not transposed!)

- \(= ^T = adj \) classical adjugate

- \(= adj\) adjugate taken twice

Recall two well-known facts valid for every square matrix \(M\) of size \(n\):

$$
(F1)M adj M
=
adj M M
=
(M)\, I_n.
$$

$$
(F2)If \(M\) is not a zero-divisor in the ground ring, then
adj M = (M)\, M^-1. 1
$$

Because the determinant \(d\) of \(\) is an irreducible (hence non-zero)
polynomial in \(R\), it is not a zero-divisor; consequently we may use (1) for
both \(\) and \(\).

Proof of (i): \(= d^4\).

We have \(= adj\), so by (F1)

$$
= = d I_5. 2
$$

Taking determinants in (2) and using \((d I_5) = d^5\), we obtain

$$
()() = d^5
= d^5d = d^4.
$$

Because \(\) and \(\) differ only by a transpose, they have the same
determinant; hence

$$
= = d^4. $$

Proof of (ii): \(= d^3\).

Since \(\) is invertible when \(d 0\) and \(= d^4\),
identity (1) gives

$$
adj=
()\, ^-1
=
d^4 (1/d)\,=
d^3.
$$

But both sides are polynomial matrices whose entries coincide on the open set
\(\d0\\); therefore they are identical in the polynomial ring \(R\).
Hence

$$
= d^3 . $$

**Proof of (iii).**

*(a) Determinant of \(\).*

From (ii) we have \(= d^3\), so

$$
= (d^3)
= (d^3)^5 = d^15. $$

*(b) Rank and right-kernel when \(d 0\).*

If a specialisation of the indeterminates yields a numerical matrix with
\(d 0\), then \(\) is invertible; hence

$$
rank= 5,
() = \0\.
$$

Because \(= d^4\), the same specialisation also gives
\(0\), so \(\) is invertible, whence

$$
rank= 5,
() = \0\.
$$

Thus \(\) and \(\) have the same rank and the same right-kernel;
explicitly, for every column vector \(v\),

$$
v = 0
v = 0
v = 0. $$

All three requested statements (i)–(iii) are thereby established.

**Failure types:** logic\_hallucination, step\_omission.

**Breakdown location.**
The KV solution asserts $adj M = (M)\,M^-1$ inside the ambient polynomial ring and claims it can be used for the parameters $$ and $$, even though $M^-1$ does not exist in that ring unless one localizes at $M$. This misuse first appears in the "Preliminaries" with (F2) and is then applied in proving (ii).

**Caption / takeaway.**
KV misapplies the identity $adj M = (M)\,M^-1$ in the polynomial ring without localization, leading to a rigor gap. The ORIGINAL stays within valid algebraic operations and justifies each step.

**Contrast summary.**
The ORIGINAL solution proceeds entirely within an appropriate algebraic setting, expanding and factoring polynomials with fully justified coefficient comparisons. In contrast, the KV solution invokes a false general identity in the stated ring: it treats $adj M = (M)\,M^-1$ as an equality in the polynomial ring without inverting $M$, effectively assuming inverses that do not exist there. It then bases the key step $= d^3 $ on this illegitimate manipulation, only implicitly appealing to a localization without stating it. Although the final equalities hold over a field, the logical chain in the KV write-up fails at the foundational ring-theoretic level. This highlights a robustness failure where the model hallucinates a lemma and omits the necessary localization step.

## 1939-A-1

### Original question

    1. Find the length of the curve \(y^2 = x^3\) from the origin to the point where the tangent makes an angle of \(45^\) with the \(x\)-axis.

### O3 solution on original

Let the curve be given by \(y^2=x^3\) (Neile's parabola).

**1. Slope of the tangent**

Differentiate implicitly:

$$
2y\,dydx=3x^2
\;\;\;\;
dydx=3x^22y.
$$

The tangent makes an angle of \(45^\) with the \(x\)-axis when its slope equals
\(45^=1\):

$$
3x^22y=1
3x^2=2y. 1
$$

But on the curve \(y=x^3/2\). Substitute into (1):

$$
3x^2=2x^3/2
\;\;\;\;
3x^1/2=2
\;\;\;\;
x=(23)^2=49.
$$

Hence \(y=(4/9)^3/2=(23)^3=827\).
So the required point is

$$
P(49,827).
$$

**2. Parametrisation**

Put \(x=t^2,\; y=t^3\) \((t0)\). Then indeed

$$
y^2=t^6=(t^2)^3=x^3.
$$

At \(P\) we have \(t^2=4/9 \;\; t_0=2/3\).

**3. Arc-length element**

$$
dxdt=2t,dydt=3t^2
\;\;
(dxdt)^2+(dydt)^2
=
(2t)^2+(3t^2)^2
=
4t^2+9t^4
=
t4+9t^2.
$$

**4. Length from the origin (\(t=0\)) to \(P\) (\(t=2/3\))**

$$
L=_0^2/3 t4+9t^2\,dt.
$$

Substitute \(u=4+9t^2\) \((du=18t\,dt t\,dt=du/18)\).
When \(t=0\), \(u=4\); when \(t=2/3\), \(u=8\).

$$
L=118_4^8u^1/2\,du
  =118[23u^3/2]_4^8
  =127\,u^3/2|_4^8.
$$

Compute the bounds:

$$
u^3/2=uu
\;\;
8^3/2=88=822=162,4^3/2=44=42=8.
$$

Therefore

$$
L=127(162-8)
  =827(22-1).
$$

Hence the length of the curve from the origin to the point where the tangent is at \(45^\) is

$$
827(22-1).
$$

### Kernel variant

    For the curve \(y^4 = 16 x^6\) in the first quadrant, determine the exact length of the segment whose end-points are the two points at which the tangent to the curve forms angles of \(30^\) and \(60^\) with the positive \(x\)-axis.

### O3 solution on KV

Curve: \(y^4 = 16 x^6\) (first quadrant \(x>0,\, y>0\)).

**1.\; Compute the derivative.**

$$
y^4 = 16x^6
\;\;
4y^3\,dydx = 96x^5
\;\;
dydx = 24x^5y^3.
$$

**2.\; Express \(y\) and the derivative only in terms of \(x\).**

$$
y = (16x^6)^1/4 = 2x^3/2,
y^3 = (2x^3/2)^3 = 8x^9/2.
$$

Hence

$$
dydx
=
24x^58x^9/2
=
3x^1/2
=
3x.
$$

**3.\; Slopes corresponding to the required tangents.**

$$
= 30^\;\; m_1 = 30^= 13,
= 60^\;\; m_2 = 60^= 3.
$$

**4.\; Find the \(x\)-coordinates where the derivative equals these slopes.**

(i)\;
\(
3x = 13
x = 133
x_1 = (133)^2 = 127.
\)

(ii)\;
\(
3x = 3
x = 13
x_2 = (13)^2 = 13.
\)

5.\; Corresponding \(y\)-coordinates (using \(y = 2x^3/2\)).

(i)\;

$$
y_1
= 2 x_1^3/2
= 2(127)^3/2
= 2\,3^-9/2
= 2813.
$$

(ii)\;

$$
y_2
= 2 x_2^3/2
= 2(13)^3/2
= 233.
$$

Thus the points are

$$
P_1\!(127,\, 2813),
P_2\!(13,\, 233).
$$

**6.\; Vector between the two points.**

$$
x = 13 - 127 = 827,
y = 233 - 2813
= 52813.
$$

**7.\; Distance \(L\).**

$$
L^2
=
(x)^2 + (y)^2
=
(827)^2
+
(52813)^2
=
64729
+
270419683.
$$

Bring to the common denominator \(19683 = 3^9\):

$$
64729 = 642719683 = 172819683.
$$

Thus

$$
L^2
=
1728 + 270419683
=
443219683
=
162773^9.
$$

Therefore

$$
L
=
162773^9
=
42773^9/2
=
4277813.
$$

**8.\; Rationalising the denominator (optional).**

$$
L
=
4277813 33
=
4831243.
$$

Thus the exact length of the required segment is

$$
4277813
4831243.
$$

**Failure types:** step\_omission, logic\_hallucination.

**Breakdown location.**
After correctly locating the two tangent-angle points, the KV solution (steps 6–7) computes the straight-line (chord) distance between them instead of setting up and evaluating the arc-length integral along the curve.

**Caption / takeaway.**
KV computes chord length instead of arc length. The ORIGINAL sets up the proper arc-length integral, while KV omits it and implicitly equates straight-line distance with curve length.

**Contrast summary.**
In the ORIGINAL, after identifying the target point via the slope condition, the solver explicitly parametrizes the curve and integrates the arc-length element to obtain the true length along the curve. The KV solution likewise finds the correct points where the tangents have the specified angles, but then switches to computing the Euclidean distance between those points, implicitly treating chord length as arc length. This omits the essential arc-length setup $1+(dy/dx)^2\,dx$ (or an equivalent parametrization) that the ORIGINAL employs. As a result, the KV produces a numerically smaller, incorrect value. The contrast highlights a classic failure: computing the wrong physical quantity despite correct intermediate calculus steps.

## 1939-B-1

### Original question

    8.\; From the vertex \((0,c)\) of the catenary

$$
y = c \!(xc)
$$

a line \(L\) is drawn perpendicular to the tangent to the catenary at a point \(P\).
Prove that the length of \(L\) intercepted by the axes is equal to the ordinate
\(y\) of the point \(P\).

### O3 solution on original

Let \(P\) be an arbitrary point of the catenary

$$
y = c \!(xc), c>0.
$$

Write \(P = (a,\, y_P)\) with

$$
y_P = c \!(ac). 1
$$

**1. Slope of the tangent at \(P\).**

Differentiate (1):

$$
dydx = \!(xc).
$$

Hence the slope of the tangent at \(x=a\) is

$$
m_t = \!(ac). 2
$$

**2. Equation of the tangent at \(P\).**

Using the point–slope form through \(P(a, y_P)\):

$$
y - y_P = m_t(x-a). 3
$$

**3. Slope and equation of the required line \(L\).**

Line \(L\) passes through the vertex \(V(0,c)\) and is perpendicular to the tangent, so its slope is

$$
m_L = -1m_t
       = -1\!(ac). 4
$$

Through \(V(0,c)\):

$$
y - c = m_L x
y = c - x\!(ac). 5
$$

**4. Intercepts of \(L\) with the coordinate axes.**

- *y–intercept:* put \(x=0\) in (5) \(y=c\).
      Thus \(V\) itself is the y–intercept.

- *x–intercept:* put \(y=0\) in (5):

$$
0 = c - x\!(ac)
x = c\,\!(ac).
$$

Call this point \(B\):

$$
B(c\,(ac),\,0).
$$

**5. Length of the segment \(AB\) intercepted by the axes.**

\(A V = (0,c)\),  and \(B\) is found above. The Euclidean distance is

$$

|AB|
&= (c (ac))^2 + (0-c)^2 \\[4pt]
&= c^2\!(ac) + 1.

$$

Using the hyperbolic identity \(^2u - ^2u = 1\),

$$
^2u + 1 = u.
$$

Therefore,

$$
|AB| = c\,\!(ac). 6
$$

**6. Comparison with the ordinate of \(P\).**

From (1) we have \(y_P = c (ac)\).
Equation (6) shows that

$$
|AB| = y_P.
$$

Hence, the length of the segment of the line \(L\) intercepted between the
coordinate axes equals precisely the ordinate of the point \(P\).

### Kernel variant

Fix \(> 0\) and any integer \(n 2\).
Write

$$
r(x_1,...,x_n-1)
=
x_1^2 + + x_\,n-1^2.
$$

Consider the \((n-1)\)-dimensional "radial catenary"

$$
x_n = \!(r)
(so the vertex is  V=(0,...,0,)).
$$

For a chosen radius \(0\), set

$$
Q = (u,\; (/)),
$$

where \(u\) is a unit vector in \(R^\,n-1\).

Let \(H\) be the hyperplane through \(V\) that is orthogonal to the tangent
hyperplane of the surface at \(Q\).

Prove that the segment of \(H\) cut off by the hyperplanes

$$
x_n=0
x_1==x_n-1=0
$$

has length

$$
(/).
$$

### O3 solution on KV

**Step 1. Reduction to a 2-dimensional problem**

Because the surface

$$
S :\ x_n = (r/),
r = x_1^2 + + x_\,n-1^2,
$$

is invariant under every rotation about the \(x_n\)-axis, we may, without loss
of generality, rotate the coordinate system so that the given unit vector \(u\)
equals the first basis vector \(e_1\).
After the rotation the point chosen on the surface is

$$
Q = (, 0, ..., 0,\ (/)).
$$

Let \(\) be the coordinate \(2\)-plane spanned by the axes \(x_1\) and
\(x_n\) (all the other coordinates equal \(0\)).
In that plane the surface \(S\) appears as the usual planar catenary

$$
y = (x/),
(y := x_n,\ x := x_1 0), 1
$$

with vertex \(V = (0,)\).

All the geometric objects involved (the tangent hyperplane at \(Q\), the required
hyperplane \(H\), the coordinate hyperplanes \(x_n = 0\) and
\(x_1 = = x_n-1 = 0\)) are rotationally symmetric; consequently the
problem reduces to showing, inside the plane \(\), that the line
\(L = H \) has the stated property.
Once that is done, the same length is obtained in the whole space \(R^n\).

**Step 2. Tangent line to the catenary in \(\)**

For the planar catenary (1) we have

$$
y'(x) = (x/).
$$

At the abscissa \(x=\) this gives the slope

$$
m := y'() = (/).
$$

Hence the tangent line at

$$
Q_ = (,\ (/)) 2
$$

reads

$$
y - (/)
  = m(x - ). 3
$$

Its direction vector is \((1,m)\).

**Step 3. The required line \(L = H \)**

Inside \(\) the hyperplane \(H\) intersects as a line \(L\) passing through the
vertex \(V\) and perpendicular to (3).
Two lines in the plane are perpendicular when the product of their slopes
equals \(-1\); therefore the slope of \(L\) is \(-1/m\).
Writing its equation through \(V=(0,)\) we get

$$
y - = -1m\, x,
.e.y = - x(/). 4
$$

**Step 4. The two intersection points of \(L\)**

(i) With the horizontal axis \(y=0\) (i.e.\ with the hyperplane \(x_n=0\)):

Setting \(y=0\) in (4) gives \(x = (/)\).
Thus

$$
A = ((/),\, 0)
,
$$

that is,

$$
A = ((/)\, e_1,\ 0,...,0)
R^n.
$$

(ii) With the vertical axis \(x=0\) (i.e.\ with \(x_1==x_n-1=0\)):

Putting \(x=0\) in (4) gives \(y=\); hence the point is exactly the vertex

$$
B = V = (0,...,0,).
$$

**Step 5. Length of the segment \(AB\)**

Inside \(\) the Euclidean distance between \(A\) and \(B\) is

$$
|AB|^2
= ((/))^2 + ^2
= ^2 (^2(/) + 1)
= ^2 ^2(/),
$$

because \(^2u - ^2u = 1\).

Therefore

$$
|AB| = (/).
$$

Because the coordinates of \(A\) and \(B\) in \(R^n\) differ only in the
first and the last component, the same distance is obtained in the full space.
Hence the segment of \(H\) cut off by the hyperplanes \(x_n=0\) and
\(x_1==x_n-1=0\) indeed has length \((/)\), as
was to be proved.

**Failure types:** logic\_hallucination, step\_omission.

**Breakdown location.**
In Step 1 the KV asserts that the tangent hyperplane at $Q$ and the perpendicular hyperplane $H$ are rotationally symmetric, wrongly justifying reduction to the $x_1$–$x_n$ plane; the correct rationale (that the normal lies in that plane, so $H$ is contained in it) is missing. From Step 2 onward it also relies on $m = (/)$ in denominators, breaking down at $= 0$.

**Caption / takeaway.**
Faulty symmetry reduction and edge-case omission in the higher-dimensional catenary: incorrect invariance claim and failure at $= 0$, versus a complete 2D argument.

**Contrast summary.**
The ORIGINAL solution works entirely in 2D, computing the perpendicular through the vertex and showing its intercept length equals the ordinate, with all steps justified. The KV attempts to generalize via a rotational-symmetry reduction to a 2D slice, but this symmetry claim is false because the tangent hyperplane depends on the chosen direction $u$ and is not rotation-invariant. The correct reason the problem reduces to the $x_1$–$x_n$ plane is that the normal $((/)u,-1)$ lies in that plane, which the KV omits. Moreover, the KV ignores the degenerate case $= 0$ where the slope vanishes, making its formulas ill-defined; a separate check is required. Thus the KV exhibits both a faulty geometric reduction and an unhandled edge case, despite correct computations when $> 0$.

## 1939-B-7

### Original question

    14. Take either (i) or (ii).

(i) If

$$

$$

prove that

$$
^3 + v^3 + w^3 - 3 u v w = 1.
$$

(ii) Consider the central conics

$$

$$

where \(\) is a given positive constant.

Show that if all radii from the origin to the first conic are changed in the
ratio \(\) to \(1\) the tips of these new radii generate the second conic.

Let \(P\) be the point with coordinates

$$
x = -pa\,21+,
y = -qb\,21+.
$$

Show that if all radii from \(P\) to the first conic are changed in the ratio
\(\) to \(1\) and then reversed about \(P\) the tips of these new radii
generate the second conic.

Comment on these results in case \(= 1\).

### O3 solution on original

**Problem (i).**

Let

$$
u(x)=1+x^33!+x^66!+=_k=0^x^3k(3k)!,
v(x)=x1!+x^44!+x^77!+=_k=0^x^3k+1(3k+1)!,
$$

$$
w(x)=x^22!+x^55!+x^88!+=_k=0^x^3k+2(3k+2)!.
$$

Denote

$$
f(x)=u^3+v^3+w^3-3uvw.
$$

We shall prove that \(f(x)1\).

**1. A useful cyclic-derivative property.**

Differentiate the three series term by term:

- For \(k1\),

$$
ddx\!(x^3k(3k)!)
=x^3k-1(3k-1)!.
$$

The exponent \(3k-123\), hence the term belongs to \(w(x)\).

- Similarly, \(ddx(v)=u\) and \(ddx(w)=v\).

Therefore,

$$
u'=w,v'=u,w'=v. 1
$$

**2. The derivative of \(f(x)\).**

Using (1) and the product rule,

$$

f'(x)
&=3u^2u' + 3v^2v' + 3w^2w'
 - 3(vw\,u' + uw\,v' + uv\,w')
\\[4pt]
&=3(u^2w + v^2u + w^2v - v w^2 - u^2 w - u v^2)
\\[4pt]
&=3(v^2u - u v^2 + w^2v - v w^2)
=0.

$$

Each bracketed pair cancels identically; hence \(f'(x)=0\) for all real \(x\).

**3. Evaluation at \(x=0\).**

$$
u(0)=1,v(0)=0,w(0)=0
f(0)=1^3+0+0-0=1.
$$

**4. Conclusion.**

Because \(f'(x)=0\) and \(f(0)=1\), the function \(f(x)\) is constant. Therefore

$$
u^3+v^3+w^3-3uvw = 1
all real x.
$$

*Remark.*
An alternative (though longer) proof uses the roots-of-unity filter

$$
u=13(e^x+e^x+e^^2x),
= e^2i/3,
$$

followed by standard symmetric-polynomial manipulations.
The differential proof above is the most economical.

### Kernel variant

Problem.

(i)\; Define three power series

$$

U(x) &= 2 + x^33! + x^66! + x^99! + , \\[4pt]
V(x) &= x1! + x^44! + x^77! + x^1010! + , \\[4pt]
W(x) &= x^22! + x^55! + x^88! + x^1111! + .

$$

Show that, for every real \(x\),

$$
U^3 + V^3 + W^3 - 3UVW = 8.
$$

(ii)\; Let \(>0\) be fixed and consider the two central conics

$$

C:\;& (x^2 + y^2) + 2(r x + s y) + d = 0,\\
D:\;& (x^2 + y^2) + 2(r x + s y) + ^2 d = 0,

$$

where \(,\ (0),\, r,\, s,\, d\) are real constants.

(a)\; Show that multiplying every radius vector from the origin to \(C\) by the
factor \(\) sends \(C\) onto \(D\).

(b)\; Let

$$
P(-\,21+\,r,
       -\,21+\,s).
$$

Prove that if each radius vector from \(P\) to \(C\) is first multiplied by
\(\) and then reversed (i.e.\ multiplied by \(-1\)), the resulting tips
trace exactly the conic \(D\).

(c)\; Discuss what happens in parts (a) and (b) when \(=1\).

### O3 solution on KV

0.4pt

**Problem (i)**

0.4pt

1.\; Let \(= e^2i/3\) (so \(^3 = 1\) and \(1++^2 = 0\)).
Split the exponential series

$$
e^x = _n0 x^nn!
$$

into its three residue classes modulo \(3\).

$$
A(x) := _k0 x^3k(3k)!,
B(x) := _k0 x^3k+1(3k+1)!,
C(x) := _k0 x^3k+2(3k+2)!.
$$

Then

$$
U(x) = 1 + A(x) + 1 = A(x)+1+1??\ (BUT in the problem \(U\) starts with \(2\)...)
$$

hence

$$
U = A+1,V = B,W = C. 1
$$

2.\; *Closed form of \(A,B,C\).*

The three linear equations

$$

A+   B+   C &= e^x,\\
A+ B+ ^2C &= e^x,\\
A+ ^2B+ C &= e^^2 x

$$

give, by Cramer,

$$

A &= e^x+e^x+e^^2x3,\\
B &= e^x+^2e^x+e^^2x3,\\
C &= e^x+e^x+^2e^^2x3.

$$

All three are real-valued functions of the real variable \(x\), and (2) is easily
seen to reproduce exactly the three power series of \(A,B,C\).

3.\; *Elementary symmetric functions of \(A,B,C\).*

$$

_1 &:= A+B+C = e^x, \\
_2 &:= AB+BC+CA = e^2x-e^-x3,\\
_3 &:= ABC.

$$

(3b) is obtained by multiplying the first two lines of (2) and using
\(^2+=-1\) together with \(e^xe^^2x=e^-x\).
A direct (but slightly longer) calculation gives

$$
A^3+B^3+C^3-3ABC = 1. 4
$$

4.\; *The required identity.*

With (1) write

$$

S(x)
&:= U^3+V^3+W^3-3UVW \\
&= (A+1)^3 + B^3 + C^3 - 3(A+1)BC \\
&= (A^3+B^3+C^3-3ABC) + (3A^2+3A+1) - 3BC.

$$

Insert (4):

$$
S(x)=1 + (3A^2+3A+1) - 3BC. 6
$$

Now express \(BC\) through \(_1,_2\):

$$
BC = _2 - A(_1-A)
= _2 - A e^x + A^2. 7
$$

Substitute (3b) and (7) in (6):

$$

S(x)
&=1 + 3A + 1 - 3[e^2x-e^-x3 - A e^x+A^2] \\
&= 2 + 3A + e^-x - e^2x + 3A e^x - 3A^2 + 3A^2 \\
&= 2 + e^-x - e^2x + 3A(1+e^x).

$$

Using (2) one directly checks that the right-hand side of (8) is identically
equal to \(8\) (a short verification is to note that both sides are entire
functions satisfying the same third-order ODE \(f"'=f\) and the same initial
data at \(x=0\)). Hence

$$
S(x) 8 every real x. 9
$$

In particular \(S(0)=2^3=8\); therefore (9) holds for all \(x\).

0.4pt

**Problem (ii)**

0.4pt

For convenience put \(X:=(x,y)^T\) in column-vector notation. The equations
of the two conics can be rewritten as

$$
X^TKX + 2p^TX + d = 0, (C)
$$

$$
X^TKX + 2\, p^TX + ^2 d = 0, (D)
$$

with the diagonal matrix \(K:=diag(,)\)
(\(0\)) and the vector \(p:=(r,s)^T\).

0.4pt

**(a) Radial homothety with centre \(O\).**

0.4pt

Multiply a point \(XC\) by the factor \(\), i.e.\ send it to

$$
X X.
$$

Then

$$
(X)^TK(X)+2p^T(X)+d
= ^2X^TKX+2p^TX+d = 0
$$

because \(X\) fulfils (C). Dividing by \(^2\) gives exactly (D). Hence
the mapping \(XX\) sends \(C\) onto \(D\).

0.4pt

**(b) Radial homothety with centre \(P\) followed by a half-turn.**

0.4pt

Let

$$
P=(
-2r(1+),
-2s(1+)
)^T
$$

and define the map

$$
F(X):=P - (X-P) = (1+)P - X. 10
$$

(10) reverses the vector \(PX\) and multiplies its length by \(\).

Write \(X' := F(X)\) and substitute in the equation (D):

$$
X'^TKX' + 2\, p^TX' + ^2 d.
$$

By (10) \(X' = (1+)P - X\), so

$$
X'^TKX' = ^2 X^TKX
- 2(1+) P^TKX
+ (1+)^2 P^TKP.
$$

A short calculation, using the explicit coordinates of \(P\), shows

$$
P^TK = -1+\, p^T, P^TKP = ^2(1+)^2\, d.
$$

Insert these three facts:

$$

X'^TKX' + 2p^TX' + ^2d
&= ^2 X^TKX
- 2(1+)P^TKX
+ (1+)^2P^TKP  \\
&+ 2p^T[(1+)P-X] + ^2d \\
&= ^2[ X^TKX + 2 p^TX + d ] = 0,

$$

because the bracket vanishes for every \(X\) on \(C\). Thus the image curve is
exactly \(D\).

0.4pt

**(c) The special case \(=1\).**

0.4pt

With \(=1\) the two conics coincide (their equations are identical).

(a) The mapping \(XX\) is the identity, so nothing changes.

(b) Formula (10) becomes \(F(X)=2P-X\), i.e.\ the half-turn (central symmetry)
about \(P\). When \(C=D\), a \(180^\) rotation about \(P\) leaves the
conic fixed (a usual symmetry of every central conic).

**Failure types:** step\_omission, logic\_hallucination, arithmetic.

**Breakdown location.**
In part (i) the KV solution asserts $A^3+B^3+C^3-3ABC=1$ without proof and then claims $S(x)=8$ via a wrong ODE argument ($f"' = f$), which a constant cannot satisfy. In part (ii) it mishandles the effect of the scaling $X X$ on the linear and constant terms and computes incorrect identities for $P$ (missing factors), so the reduction to $D$ is unfounded.

**Caption / takeaway.**
Clean cyclic-derivative cancellation vs.\ an overcomplicated roots-of-unity/ODE shortcut and mishandled scaling. The KV fails by omitting a key identity, using an invalid ODE argument, and mis-scaling conic coefficients.

**Contrast summary.**
The ORIGINAL solves part (i) by exploiting the cyclic derivative identities $u' = w$, $v' = u$, $w' = v$ to show $f'(x)=0$ and then fixes the constant by $f(0)=1$, a short and airtight argument. The KV instead uses a roots-of-unity decomposition, leaves a pivotal symmetric identity unproved, and finally appeals to an incorrect ODE invariance to conclude $S(x)8$. In the conic mapping, the ORIGINAL approach (analogous to the statement) respects how quadratic, linear, and constant terms scale, whereas the KV’s matrix computation drops necessary $$ factors and miscomputes properties of $P$, breaking the cancellation to $D$. The pair highlights how a clean structural identity beats an overengineered approach and how small coefficient errors derail geometric transformations.