# KEYPLAN — Fine-Tuning a Model for Legend-Keyed Relational Graph Recovery

## Overview

This is a **fine-tuning** challenge: adapt a pretrained model so that it acquires a
new, structured capability from a modest labeled dataset. You are given **4,000
labeled training examples** and must **fine-tune a model** to produce the correct
structured output on **1,000 held-out test examples**.

Each example is a technical schematic that **carries its own legend**. The legend
binds abstract node **shapes** to component-type labels (`A`–`G`) and connector
**line-styles** to relation labels (`feeds`, `blocks`, `syncs`, `gates`). The
schematic then draws those shape-nodes joined by directed, styled connectors.

The fine-tuned model's task, for each test example, is to emit the **typed
relational graph** — the complete set of `(source_type, relation, target_type)`
triples obtained by decoding every connector through *that example's* legend.

**Why fine-tuning is the point.** The legend is a **fresh random assignment in every
example** — which shape means `A`, and which style means `feeds`, changes each time.
So there is nothing to memorize: the model must instead learn the *procedure*
"consult this example's legend, then decode and enumerate the connectors". A model
that instead latches onto any fixed mapping (the shortcut a naive fine-tune drifts
toward) scores near chance. The challenge is engineering a fine-tune that learns the
conditional, per-example decoding behavior and applies it consistently.

Real-world analogue: adapting a model to read any schematic, floor plan, or circuit
whose symbol key is defined locally on the sheet rather than by a universal standard.

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

- **Fine-tune your own model.** The submission must be produced by a model you
  fine-tuned on the provided training data, run offline on the test set. Start from
  an openly licensed pretrained backbone (or train one yourself) and adapt it with
  the standard stack (numpy, pandas, torch, transformers, peft, PIL, …).
- **No external model outputs in the submission.** Predictions must come from your
  own fine-tuned model — not from prompting a hosted LLM/VLM API or any third-party
  service, and not from any answer key.
- **Only `dataset/public/` is available.** Test answers and the per-example legend
  metadata are hidden. Do not attempt to reconstruct or scrape hidden files.
- **Determinism.** Your training and inference should be reproducible from a fixed
  seed.

## Allowed

- **Fine-tuning any openly licensed pretrained model** on the provided `train`
  split — full fine-tuning, LoRA/QLoRA, adapters, or continued pretraining.
- Training a model from scratch on the provided data, if you prefer.
- Using the standard Kaggle Docker libraries (numpy, pandas, torch, torchvision,
  timm, transformers, peft, bitsandbytes, accelerate, PIL, …).
- Prompt/target formatting, data augmentation, and curriculum choices for the
  fine-tune; holding out part of `train` for validation; test-time augmentation;
  ensembling your own fine-tuned models.

## Not allowed

- **Hosted model / API outputs in the submission.** Do not prompt an external LLM or
  VLM service (or any third-party API) to produce predictions; the submission must
  come from your own fine-tuned model running offline.
- **A solution that does not involve fine-tuning a model.** Purely hand-authored
  heuristics or rule systems with no learned model are out of scope for this
  fine-tuning track.
- **Using hidden data.** Test labels and the per-example legend metadata
  (`scheme_json`) are not provided — do not scrape, reconstruct, or otherwise obtain
  them, and do not hard-code answers for specific test ids.
- **Relying on a fixed global mapping.** You may not assume any constant shape→type
  or style→relation mapping; the bindings are randomized per example and must be
  decoded from each example's legend. (Such an assumption is also provably capped
  near the chance floor.)
- **Non-reproducible submissions.** No dependence on network calls at inference,
  external services, or unseeded randomness that changes the output run to run.
- **Manual labeling.** Do not annotate the test examples by hand or crowdsource
  their triples; predictions must be produced by your fine-tuned model.
