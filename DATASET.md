# Dataset Description — KEYPLAN

## Overview

KEYPLAN is a procedurally generated corpus of **legend-keyed schematic images**.
Each 512×512 RGB image contains two parts:

1. a **legend panel** (left) that, *for that image only*, binds a set of abstract
   node **shapes** to **component-type** labels (`A`–`G`) and a set of connector
   **line-styles** to **relation** labels (`feeds`, `blocks`, `syncs`, `gates`);
2. a **schematic** (right) of shape-nodes joined by directed, styled connectors.

The label for an image is the **typed relational graph**: the set of
`(source_type, relation, target_type)` triples obtained by decoding every
connector through that image's legend. The shape→type and style→relation bindings
are a **fresh random assignment in every image**, so no fixed mapping transfers
between images — the legend must be read and applied per image.

- **Size:** 5,000 images — 4,000 `train` (with labels) and 1,000 `test`
  (without labels).
- **Source:** fully synthetic (procedurally generated). No external source dataset;
  the data contains no personal or third-party material.
- **License:** MIT (see `LICENSE`).

## File Structure

Distributed as `keyplan_public.zip` (Git LFS):

- `train/images/<id>.png` — 4,000 training images, named `t_00000`–`t_03999`.
- `train.csv` — training labels: `id`, `triples`.
- `test/images/<id>.png` — 1,000 test images, named `e_00000`–`e_00999`.
- `test.csv` — the test index: `id` only.
- `sample_submission.csv` — a valid submission template: `id`, `triples`.

## Features

### `train.csv`

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Image identifier; matches `train/images/<id>.png`. |
| `triples` | string | Label: `;`-joined `src\|relation\|tgt` triples, canonically sorted. Order carries no meaning (it is a set). |

### `test.csv`

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Test image identifier; matches `test/images/<id>.png`. Predict the triples for each. |

### `sample_submission.csv`

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Test image identifier. |
| `triples` | string | Predicted triples, `;`-joined `src\|relation\|tgt` (empty in the template). |

### `<id>.png`

| Field | Type | Description |
|-------|------|-------------|
| (pixels) | 512×512×3 uint8 PNG | The rendered legend + schematic. All information needed to produce the triples is present in the pixels. |

## Notes

- **Vocabulary is per-image.** `A`–`G` and the four relation names are a shared
  alphabet, but which shape/style maps to which label is randomized every image, so
  the legend must be consulted per image.
- **Graph facts.** Each type appears exactly once per image, so a triple
  `(src, rel, tgt)` uniquely identifies one directed connector. Self-loops never
  occur; a given ordered pair appears at most once. Opposite-direction pairs
  (`a→b` and `b→a`) are drawn with a small perpendicular offset to remain
  distinguishable.
- There is no separate validation file — hold out from `train` as needed.
