#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {
    "episode_id",
    "bragging_mechanism",
    "speaker_intention",
    "desired_feedback",
    "risk_assessment",
    "response_strategy",
    "response_text",
}

OPTIONAL_FIELDS: set[str] = set()

FORBIDDEN_FIELDS = {
    "prompt",
    "gold",
    "reasoning",
    "chain_of_thought",
    "analysis",
    "rubric",
    "metadata",
    "judge",
    "label",
    "labels",
}

ALLOWED_MECHANISMS = {
    "humble_complaint",
    "faux_modesty",
    "achievement_drop",
    "comparison_superiority",
    "scarcity_flex",
    "understated_flex",
    "self_aware_brag",
    "other",
}

ALLOWED_STRATEGIES = {
    "validate",
    "light_acknowledgment",
    "ask_followup",
    "humor_tease",
    "redirect",
    "neutral_observation",
    "set_boundary",
    "no_response",
}

SUSPICIOUS_PATTERNS = [
    re.compile(r"<think>|</think>", re.IGNORECASE),
    re.compile(r"\bchain of thought\b", re.IGNORECASE),
    re.compile(r"\bstep by step\b", re.IGNORECASE),
    re.compile(r"\b(reasoning|analysis|scratchpad)\s*:", re.IGNORECASE),
    re.compile(r"\b(option|candidate)\s*[12]\b", re.IGNORECASE),
    re.compile(r"^(system|assistant|user)\s*:", re.IGNORECASE),
]

MAX_WORDS = {
    "speaker_intention": 80,
    "desired_feedback": 80,
    "risk_assessment": 100,
    "response_text": 60,
}

OVERPRAISE_PATTERNS = [
    re.compile(r"\b(amazing|incredible|legendary|genius|perfect|iconic|unbelievable)\b", re.IGNORECASE),
    re.compile(r"\b(best|greatest)\s+(ever|person|one|at)\b", re.IGNORECASE),
    re.compile(r"\bso proud of you\b", re.IGNORECASE),
]

PRAISE_PATTERNS = [
    re.compile(r"\b(congrats|congratulations|great job|nice work|amazing|impressive|proud)\b", re.IGNORECASE),
]


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def contains_any(patterns: list[re.Pattern[str]], text: str) -> bool:
    return any(pattern.search(text) for pattern in patterns)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}: line {idx}: invalid json: {exc}") from exc
        if not isinstance(obj, dict):
            raise ValueError(f"{path}: line {idx}: each row must be a json object")
        rows.append(obj)
    return rows


def load_expected_episode_ids(path: Path) -> list[str]:
    return [row["episode_id"] for row in load_jsonl(path)]


def validate_submission_rows(
    rows: list[dict[str, Any]],
    expected_episode_ids: list[str] | None = None,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    seen: set[str] = set()
    submitted_ids: list[str] = []

    expected_id_set = set(expected_episode_ids or [])

    for idx, row in enumerate(rows, start=1):
        fields = set(row)
        extra = sorted(fields - REQUIRED_FIELDS - OPTIONAL_FIELDS)
        if extra:
            errors.append(f"line {idx}: unexpected fields {extra}")
        forbidden = sorted(fields & FORBIDDEN_FIELDS)
        if forbidden:
            errors.append(f"line {idx}: forbidden fields {forbidden}")

        missing = sorted(REQUIRED_FIELDS - set(row))
        if missing:
            errors.append(f"line {idx}: missing required fields {missing}")
            continue

        episode_id = row.get("episode_id")
        if not isinstance(episode_id, str) or not episode_id.strip():
            errors.append(f"line {idx}: invalid episode_id")
        elif episode_id in seen:
            errors.append(f"line {idx}: duplicate episode_id {episode_id}")
        else:
            seen.add(episode_id)
            submitted_ids.append(episode_id)

        mechanism = row.get("bragging_mechanism")
        if mechanism not in ALLOWED_MECHANISMS:
            errors.append(f"line {idx}: invalid bragging_mechanism {mechanism!r}")

        strategy = row.get("response_strategy")
        if strategy not in ALLOWED_STRATEGIES:
            errors.append(f"line {idx}: invalid response_strategy {strategy!r}")

        for field in ["speaker_intention", "desired_feedback", "risk_assessment"]:
            value = row.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"line {idx}: field {field!r} must be a non-empty string")
                continue
            max_words = MAX_WORDS[field]
            if word_count(value) > max_words:
                errors.append(f"line {idx}: field {field!r} exceeds {max_words} words")
            for pattern in SUSPICIOUS_PATTERNS:
                if pattern.search(value):
                    errors.append(f"line {idx}: field {field!r} contains hidden reasoning or prompt-like text")
                    break

        response_value = row.get("response_text")
        if not isinstance(response_value, str):
            errors.append(f"line {idx}: field 'response_text' must be a string")
            response_text = ""
        else:
            response_text = response_value
            if strategy != "no_response" and not response_text.strip():
                errors.append(f"line {idx}: field 'response_text' must be non-empty unless response_strategy is no_response")
            if word_count(response_text) > MAX_WORDS["response_text"]:
                errors.append(f"line {idx}: field 'response_text' exceeds {MAX_WORDS['response_text']} words")

        for pattern in SUSPICIOUS_PATTERNS:
            if pattern.search(response_text):
                errors.append(f"line {idx}: response_text contains hidden reasoning or prompt-like text")
                break

        if strategy == "no_response":
            if word_count(response_text) > 8:
                errors.append(f"line {idx}: no_response should have an empty or very short response_text")
            if contains_any(PRAISE_PATTERNS, response_text):
                errors.append(f"line {idx}: no_response is inconsistent with praise-like response_text")
        elif strategy == "set_boundary":
            if contains_any(OVERPRAISE_PATTERNS, response_text):
                errors.append(f"line {idx}: set_boundary is inconsistent with overpraising response_text")
        elif strategy == "light_acknowledgment":
            if contains_any(OVERPRAISE_PATTERNS, response_text):
                errors.append(f"line {idx}: light_acknowledgment is inconsistent with overpraising response_text")

    missing_episode_ids: list[str] = []
    unexpected_episode_ids: list[str] = []
    if expected_episode_ids is not None:
        submitted_id_set = set(submitted_ids)
        missing_episode_ids = sorted(expected_id_set - submitted_id_set)
        unexpected_episode_ids = sorted(submitted_id_set - expected_id_set)
        if missing_episode_ids:
            errors.append(f"missing episode ids: {missing_episode_ids[:20]}")
        if unexpected_episode_ids:
            errors.append(f"unexpected episode ids: {unexpected_episode_ids[:20]}")

    return {
        "valid": not errors,
        "row_count": len(rows),
        "submitted_unique_episode_ids": len(set(submitted_ids)),
        "expected_episode_ids": len(expected_episode_ids) if expected_episode_ids is not None else None,
        "missing_episode_ids": missing_episode_ids,
        "unexpected_episode_ids": unexpected_episode_ids,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors[:100],
        "warnings": warnings[:100],
    }


def main() -> None:
    if len(sys.argv) not in {2, 3}:
        raise SystemExit("usage: format_checker.py SUBMISSION.jsonl [REFERENCE_INPUT.jsonl]")

    submission_path = Path(sys.argv[1])
    submission_rows = load_jsonl(submission_path)

    expected_episode_ids = None
    if len(sys.argv) == 3:
        expected_episode_ids = load_expected_episode_ids(Path(sys.argv[2]))

    report = validate_submission_rows(submission_rows, expected_episode_ids)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not report["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
