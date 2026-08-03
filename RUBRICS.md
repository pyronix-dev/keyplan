# KEYPLAN — Evaluation Rubrics

Approach-neutral criteria for judging a KEYPLAN solution's engineering quality.
Each is grounded in this task's measured numbers (fixed-mapping floor ≈ 0.05
triple-F1; known-legend ceiling = 1.0; 4–6 nodes and up to ~2× directed edges per
image; per-image randomized legend).

---

### R1 — Conditions predictions on the per-image legend (MODELING, REQUIRED)
The solution must produce type/relation labels **from the legend present in each
image**, not from a mapping fixed across images. Evidence: performance stays high
when the legend bindings are permuted; the model attends to or ingests the legend
region. **Fail:** learns or hard-codes a single global shape→type or
style→relation mapping — this is provably capped at ≈0.05 triple-F1 regardless of
how well geometry is read.

### R2 — Beats the fixed-mapping floor and moves toward the ceiling (MODELING, REQUIRED)
A credible solution scores **well above the 0.05 fixed-mapping / chance floor** on
a held-out split — a competent fine-tune should clear **≥0.40** triple-F1, and
strong solutions push toward the 1.0 ceiling. A score near 0.05 indicates the
legend is being ignored; a score near 0 indicates a format or decoding bug.

### R3 — Exhaustive, direction-aware edge extraction (FEATURE_ENGINEERING / MODELING, REQUIRED)
Because the metric is set-F1 over directed triples, the method must **enumerate all
connectors** (recall) while **not inventing edges** (precision), and must respect
**arrow direction** — `A|feeds|B` and `B|feeds|A` are different triples. Evidence
of handling both precision and recall (e.g. reported per-image counts vs truth on a
val split). **Fail:** systematically drops edges in denser (10–12 edge) images, or
ignores direction and collapses `a→b` / `b→a`.

### R4 — Sound held-out validation that mirrors the metric (TRAINING, REQUIRED)
The solution holds out images from `train` and reports **mean triple-F1 with the
official parsing** (`;` triple sep, `|` field sep; order-independent set compare).
Because every image has a novel legend, a random split is representative — but the
validation must score triples the same way `grade.py` does, not a proxy like token
accuracy. **Fail:** tunes only on training loss, or reports a metric that doesn't
match the grader.

### R5 — Robust legend/geometry reading, not brittle templating (DATA_HANDLING, RECOMMENDED)
Rendering carries controlled nuisance variation (node jitter, slight shape
rotation, fill-tint noise, anti-aliasing, offset parallel edges). A good solution
is **robust to this variation** rather than relying on exact pixel templates or a
brittle classical detector that breaks on dashed/dotted/double style confusions.
Evidence: stable val score across the `n_types`/`n_edges` range.

### R6 — Exact submission format and complete coverage (CODE_QUALITY, REQUIRED)
Output is `submission.csv` with header `id,triples`, exactly **1,000 rows**, every
test `id` present, triples serialized as `src|relation|tgt` joined by `;` using the
canonical label sets (`A`–`G`; `feeds`/`blocks`/`syncs`/`gates`). **Fail:** missing
ids (each scores 0), malformed triples, wrong delimiters, or emitting labels
outside the alphabet.

### R7 — Reproducible and self-contained (CODE_QUALITY, UNIVERSAL)
Fixed seeds; runs end-to-end from `dataset/public/` to `submission.csv` within the
competition runtime using only allowed libraries and openly licensed pretrained
weights (or from scratch). No dependence on hidden files, external services, or LLM
API calls. **Fail:** non-deterministic results, or reliance on network/LLM outputs.

### R8 — Clear reasoning about the legend trap (COMMUNICATION, RECOMMENDED)
The write-up articulates *why* a fixed mapping fails and how the design forces
per-image legend use, and reports the achieved val triple-F1 against the 0.05 floor
/ 1.0 ceiling reference points. **Fail:** presents a score with no comparison to
the floor/ceiling or no account of the legend-conditioning insight.
