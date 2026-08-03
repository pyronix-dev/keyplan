# KEYPLAN — Legend-Keyed Relational Graph Recovery

## Overview

Each image is a technical schematic that **carries its own legend**. The legend
binds abstract node **shapes** to component-type labels (`A`–`G`) and connector
**line-styles** to relation labels (`feeds`, `blocks`, `syncs`, `gates`). The
schematic then draws those shape-nodes joined by directed, styled connectors.

Your job: for each **test** image, recover the **typed relational graph** — the
complete set of `(source_type, relation, target_type)` triples you get by decoding
every connector through *that image's* legend.

The catch: **the legend is different in every image.** Which shape means `A`, and
which line-style means `feeds`, is a fresh random assignment per image. There is no
global mapping to memorize — the binding must be read off the legend and applied to
the schematic, image by image. You are given 4,000 labeled training images to learn
this skill and 1,000 unlabeled test images to solve.

Real-world analogue: reading any schematic, floor plan, or circuit whose symbol key
is defined locally on the sheet rather than by a universal standard.

## Evaluation

Mean **triple-level F1** over the test images, in `[0, 1]`, higher is better.

For one image, let `P` be your predicted set of triples and `T` the true set:

```python
def f1(P, T):
    if not P and not T: return 1.0
    if not P or not T:   return 0.0
    tp = len(P & T)
    if tp == 0: return 0.0
    prec, rec = tp / len(P), tp / len(T)
    return 2 * prec * rec / (prec + rec)
```

The final score is the mean of `f1` over all 1,000 test images. Partial credit is
smooth: getting more triples right (and fewer wrong) raises the score
proportionally. A missing test `id` scores 0 for that image.

**Why this is hard (measured):** a solver that ignores the per-image legend and
applies any fixed shape→type / style→relation mapping scores ≈ **0.05** triple-F1,
even with perfect geometry reading — no better than chance. The known-legend
ceiling is **1.0**. The gap between them is entirely the skill of reading each
image's legend and consistently applying it while exhaustively enumerating the
schematic's directed connectors.

## Dataset

Provided under `dataset/public/`:

| Path | Description |
|------|-------------|
| `train/images/<id>.png` | 4,000 labeled training images (512×512 RGB). |
| `train.csv` | Columns `id`, `triples`. `triples` is `;`-joined `src\|relation\|tgt`, canonically sorted (order is not meaningful — it is a set). |
| `test/images/<id>.png` | 1,000 unlabeled test images (512×512 RGB). |
| `test.csv` | Column `id`. The images you must predict. |
| `sample_submission.csv` | Columns `id`, `triples` with empty predictions. |

Each image has 4–6 nodes and up to ~2× that many directed connectors. Every
component type appears at most once per image, so each triple identifies a unique
connector. Self-loops do not occur.

## Submission

A CSV named `submission.csv` with a header and **exactly 1,000 rows** (one per test
`id`):

| Column | Type | Description |
|--------|------|-------------|
| `id` | string | Test image id, matching `test.csv`. |
| `triples` | string | Your predicted triples: `;`-joined `src\|relation\|tgt`. Use component-type labels (`A`–`G`) and relation names (`feeds`/`blocks`/`syncs`/`gates`). Order does not matter; duplicates are ignored. An empty string means "no edges". |

Example row: `e_00007,"A|feeds|C;C|blocks|D;D|syncs|A"`

## Rules

- **From-scratch method, standard libraries only.** Build your solution with the
  Kaggle Docker stack (numpy, pandas, torch, torchvision, timm, transformers,
  PIL, …). You may fine-tune an openly licensed pretrained vision or
  vision-language backbone on the provided training data.
- **No LLM outputs in the submission.** Predictions must come from your own model
  or algorithm run on the test images — not from prompting an external LLM/VLM
  service and not from any answer key.
- **Only `dataset/public/` is available.** Test answers and the per-image legend
  metadata are hidden. Do not attempt to reconstruct or scrape hidden files.
- **Determinism.** Your training and inference should be reproducible from a fixed
  seed.

## Allowed

- Training or fine-tuning any model (CNN, ViT, vision-language model, or a
  from-scratch pipeline) on the provided `train` images and labels.
- Using openly licensed pretrained vision / vision-language backbones and the
  standard Kaggle Docker libraries (numpy, pandas, torch, torchvision, timm,
  transformers, PIL, scikit-image, …).
- Any classical computer-vision approach (segmentation, template matching, line
  tracing, OCR of the legend, etc.) built by you.
- Holding out part of `train` for validation; test-time augmentation; ensembling
  your own models.
- Reading the legend and schematic straight from the pixels — that is the task.

## Not allowed

- **LLM/VLM API outputs in the submission.** Do not prompt an external hosted
  model (or any third-party service) to produce predictions; the submission must
  come from your own model or algorithm running on the test images.
- **Using hidden data.** Test labels and the per-image legend metadata
  (`scheme_json`) are not provided — do not scrape, reconstruct, or otherwise
  obtain them, and do not hard-code answers for specific test ids.
- **Leaking a fixed global mapping.** You may not assume any constant shape→type or
  style→relation mapping; the bindings are randomized per image and must be read
  from each image's legend. (Such an assumption is also provably capped near the
  chance floor.)
- **Non-reproducible submissions.** No dependence on network calls at inference,
  external services, or unseeded randomness that changes the output run to run.
- **Manual labeling.** Do not annotate the test images by hand or crowdsource their
  triples; predictions must be produced programmatically by your solution.
