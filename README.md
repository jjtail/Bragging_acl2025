# CCAC 2026 Track 4: 炫耀社交回应智能体挑战赛

**BRAG-Agent v6 Official <=20B Track**

BRAG-Agent v6 evaluates whether language models can recognize nuanced bragging behavior and produce socially appropriate replies without overpraising, moralizing, misreading the situation, or becoming unnecessarily cold.

This repository hosts **CCAC 2026 赛道四：炫耀社交回应智能体挑战赛**. The challenge is based on the ACL 2025 paper [**It’s Not Bragging If You Can Back It Up: Can LLMs Understand Braggings?**](https://aclanthology.org/2025.acl-long.858/) ([PDF](https://aclanthology.org/2025.acl-long.858.pdf)).

The release contains the public participant package. The hidden gold labels, private ID map, judge prompts, and private scoring scripts are withheld for official evaluation.

## What Is Included

```text
BRAG-Agent-public/
  data/train.jsonl
  data/dev_input.jsonl
  data/dev_gold.jsonl
  data/test_input.jsonl
  data/sample_submission.jsonl
  docs/DATASET_CARD.md
  docs/LABEL_SCHEMA.md
  docs/USAGE_GUIDE.md
  scripts/format_checker.py
  scripts/evaluate_dev.py
```

Public data sizes:

```text
train: 500
dev: 45
test: 409
```

The official hidden evaluation contains 409 test examples:

```text
Core: 206
Bloom robustness: 203
Total: 409
```

Participants only see anonymized public test IDs such as `test_000001`; the Core/Bloom split is private.

## Official Track

The official leaderboard track is:

```text
BRAG-Agent v6 Official <=20B Track
```

Eligible systems must use a candidate model with total parameter count <=20B. See [PARTICIPATION_RULES.md](PARTICIPATION_RULES.md).

## Quick Start

Validate the sample submission:

```bash
cd BRAG-Agent-public
python scripts/format_checker.py data/sample_submission.jsonl data/test_input.jsonl
```

Score a development submission:

```bash
cd BRAG-Agent-public
python scripts/format_checker.py path/to/dev_submission.jsonl data/dev_input.jsonl
python scripts/evaluate_dev.py data/dev_input.jsonl data/dev_gold.jsonl path/to/dev_submission.jsonl
```

Create a final test submission:

```bash
cd BRAG-Agent-public
python scripts/format_checker.py path/to/test_submission.jsonl data/test_input.jsonl
```

Submit:

```text
test_submission.jsonl
submission_metadata.md
```

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

No extra fields are allowed. Valid labels are listed in `BRAG-Agent-public/docs/LABEL_SCHEMA.md`.

## Official Scoring

The official v6 score uses:

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

See [EVALUATION.md](EVALUATION.md) for the complete scoring formula.

## Important Notes

- Dev scores are proxy scores only and do not determine the leaderboard.
- Official scoring is run privately by the organizers.
- The hidden test labels and private evaluator must not be distributed.
