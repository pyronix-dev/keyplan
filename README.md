# KEYPLAN: Legend-Keyed Relational Graph Recovery

A vision challenge. Each 512×512 image is a schematic that **carries its own
legend**. The legend binds abstract node **shapes** to component-type labels
(`A`–`G`) and connector **line-styles** to relation labels
(`feeds`, `blocks`, `syncs`, `gates`). The schematic then draws those shape-nodes
joined by directed, styled connectors.

**Task:** for each test image, recover the **typed relational graph** — the set of
`(source_type, relation, target_type)` triples obtained by decoding every connector
through *that image's* legend.

The catch: **the legend is different in every image.** Which shape means `A`, and
which line-style means `feeds`, is a fresh random assignment per image, so there is
no global mapping to memorize — the binding must be read from the legend and applied
to the schematic, image by image.

## Data

`keyplan_public.zip` (Git LFS) contains:

| Path | Description |
|------|-------------|
| `train/images/<id>.png` | 4,000 labeled training images. |
| `train.csv` | `id`, `triples` — the training labels. `triples` is `;`-joined `src\|relation\|tgt`, canonically sorted (order is not meaningful; it is a set). |
| `test/images/<id>.png` | 1,000 test images (no labels). |
| `test.csv` | `id` — the images to predict. |
| `sample_submission.csv` | `id`, `triples` with empty predictions. |

Each image has 4–6 nodes and up to ~2× that many directed connectors. Every
component type appears at most once per image. Self-loops do not occur.

See `PROBLEM.md` for the full task statement, evaluation, and submission format,
and `RUBRICS.md` for the evaluation rubrics.

## Evaluation

Mean **triple-level F1** over the test images (`grade.py`), in `[0, 1]`, higher is
better. Partial credit is smooth: more correct triples (and fewer spurious ones)
raise the score.

## Submission

`submission.csv` with header `id,triples` and exactly 1,000 rows — one per test
`id`; `triples` is `;`-joined `src|relation|tgt`. Example:
`e_00007,"A|feeds|C;C|blocks|D;D|syncs|A"`.

## License

MIT (code + data) — see `LICENSE`. The dataset is fully synthetic and contains no
personal or third-party material.
