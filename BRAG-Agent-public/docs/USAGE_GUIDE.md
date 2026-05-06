# BRAG-Agent v6 Public Usage Guide

## Files

- `data/train.jsonl`: public training set, unchanged from v5 Train-500.
- `data/dev_input.jsonl`: public development inputs.
- `data/dev_gold.jsonl`: public development gold labels for proxy scoring.
- `data/test_input.jsonl`: anonymized v6 official test inputs, 409 rows.
- `data/sample_submission.jsonl`: full-length test submission template.
- `docs/DATASET_CARD.md`: dataset card.
- `docs/LABEL_SCHEMA.md`: field and label definitions.
- `scripts/format_checker.py`: strict submission validator.
- `scripts/evaluate_dev.py`: local dev proxy scorer.

## Submission Format

Each submitted row must contain exactly these fields:

```json
{
  "episode_id": "test_000001",
  "bragging_mechanism": "understated_flex",
  "speaker_intention": "...",
  "desired_feedback": "...",
  "risk_assessment": "...",
  "response_strategy": "light_acknowledgment",
  "response_text": "..."
}
```

No extra fields are allowed.

## Check A Test Submission

```bash
cd BRAG-Agent-public
python scripts/format_checker.py path/to/submission.jsonl data/test_input.jsonl
```

## Check A Dev Submission

```bash
cd BRAG-Agent-public
python scripts/format_checker.py path/to/dev_submission.jsonl data/dev_input.jsonl
```

The checker rejects missing IDs, unexpected IDs, duplicate IDs, invalid labels, hidden reasoning text, extra fields, overly long fields, and obvious strategy/response mismatches.

## Score On Dev

```bash
cd BRAG-Agent-public
python scripts/evaluate_dev.py data/dev_input.jsonl data/dev_gold.jsonl path/to/dev_submission.jsonl
```

The dev score is a proxy score only:

```text
100 * (
  0.30 * mechanism_accuracy
  + 0.20 * strategy_score
  + 0.20 * risk_label_f1
  + 0.15 * response_reference_token_f1
  + 0.15 * format_score
)
```

## Official Test Evaluation

Official test scoring is run by the private evaluation package. Public `test_input.jsonl` contains anonymous IDs only and does not reveal whether an item belongs to Core or Bloom.

v6 hidden test size:

```text
Core: 206
Bloom: 203
Total: 409
```

Official v6 scoring:

```text
Final = 0.60 * Core Task Quality Score
      + 0.40 * Bloom Robustness Score
```

Bloom robustness uses a soft trigger:

```text
risk >= 7      -> full trigger = 1.0
5 <= risk < 7  -> soft trigger = 0.5
risk < 5       -> no trigger = 0.0
```

The official leaderboard track is limited to candidate models with total parameter count <=20B.
