"""
KEYPLAN grader — mean triple-level F1 in [0, 1], higher is better.

A prediction and an answer are each a SET of "src|relation|tgt" triples,
separated by ';'. Per image we compute the F1 between predicted and true triple
sets; the score is the mean over all test images. Missing ids score 0.

    submission.csv : id, triples
    answers.csv    : id, triples
"""
import pandas as pd


def parse_triples(text) -> set:
    if not isinstance(text, str):
        return set()
    out = set()
    for chunk in text.strip().split(";"):
        chunk = chunk.strip()
        if not chunk:
            continue
        parts = [p.strip() for p in chunk.split("|")]
        if len(parts) == 3 and all(parts):
            out.add((parts[0], parts[1], parts[2]))
    return out


def _f1(pred: set, truth: set) -> float:
    if not truth and not pred:
        return 1.0
    if not pred or not truth:
        return 0.0
    tp = len(pred & truth)
    if tp == 0:
        return 0.0
    prec, rec = tp / len(pred), tp / len(truth)
    return 2 * prec * rec / (prec + rec)


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    if "id" not in submission.columns or "triples" not in submission.columns:
        raise ValueError("submission must have columns: id, triples")
    sub = dict(zip(submission["id"].astype(str), submission["triples"]))
    scores = []
    for _, row in answers.iterrows():
        img_id = str(row["id"])
        truth = parse_triples(row["triples"])
        pred = parse_triples(sub.get(img_id, ""))    # missing id -> empty -> worst
        scores.append(_f1(pred, truth))
    return float(sum(scores) / len(scores)) if scores else 0.0


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("submission")
    ap.add_argument("answers")
    a = ap.parse_args()
    s = grade(pd.read_csv(a.submission), pd.read_csv(a.answers))
    print(f"score: {s:.4f}")
