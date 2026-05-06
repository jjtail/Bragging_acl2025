# Participation Rules

## Official Track Eligibility

The official leaderboard is limited to candidate models with:

```text
total parameter count <= 20B
```

For dense models, use the full model parameter count.

For MoE models, use total parameters, not active parameters.

For ensembles, cascades, generator-reranker systems, retrieval-augmented generation systems with neural rerankers, or multi-agent systems, every model that reads the input, writes candidate outputs, scores candidate outputs, selects among candidates, or edits the final answer must individually satisfy the <=20B rule. Any use of a >20B model in the inference path makes the submission non-eligible for the official track.

Closed model APIs are not eligible for the official <=20B track, even if the provider claims the model is <=20B. They may be submitted as reference systems only. Open-weight local or self-hosted models are eligible when their total parameter count is disclosed and <=20B.

## Allowed Development Data

Participants may use:

- `BRAG-Agent-public/data/train.jsonl`
- `BRAG-Agent-public/data/dev_input.jsonl`
- `BRAG-Agent-public/data/dev_gold.jsonl`
- public documentation in `BRAG-Agent-public/docs/`
- any generally available pretraining data already used by the base model

Participants may use the public training set for:

- zero-shot or few-shot prompting
- supervised fine-tuning
- LoRA or other parameter-efficient tuning
- rule-based systems
- reranking or calibration, if every model used for reranking or calibration also satisfies the <=20B rule

## Disallowed Data And Assistance

Participants must not use:

- hidden test labels
- the private evaluation package
- private ID maps
- judge prompts
- manual annotation of official test labels
- direct or indirect access to official hidden gold during development

For the official <=20B track, participants must not use >20B models or closed model APIs to generate, label, filter, select, rerank, calibrate, edit, or distill answers for `test_input.jsonl`.

If synthetic data is used, participants must disclose:

- generator model
- parameter count or API provider
- whether generated data was used for training, prompt construction, or selection

Task-specific synthetic data generated, labeled, filtered, selected, rewritten, or distilled by >20B models or closed model APIs makes a system non-eligible for the official <=20B track. Such systems may be reported only as non-eligible reference baselines unless the organizers explicitly create a separate assisted-data track.

## Required Submission Files

Each participant should submit:

```text
test_submission.jsonl
submission_metadata.md
```

The JSONL submission must contain 409 rows, one for every `episode_id` in `data/test_input.jsonl`.

The metadata file should follow [SUBMISSION_METADATA_TEMPLATE.md](SUBMISSION_METADATA_TEMPLATE.md).

## Submission Validation

Before submission, participants must run:

```bash
cd BRAG-Agent-public
python scripts/format_checker.py path/to/test_submission.jsonl data/test_input.jsonl
```

The checker rejects:

- missing IDs
- unexpected IDs
- duplicate IDs
- missing fields
- extra fields
- invalid labels
- overly long fields
- hidden reasoning or prompt-like text
- obvious response strategy / response text mismatches

Only submissions that pass the public format checker are eligible for official scoring.

## Reporting Requirements

Leaderboard entries should report:

- model name
- total parameter count
- base model source
- training method
- public data used
- external or synthetic data used
- decoding settings
- date of submission
- official Final, Core, and Bloom scores

Reference entries above 20B should be clearly marked:

```text
Non-eligible reference baseline
```
