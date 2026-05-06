#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from format_checker import load_expected_episode_ids, load_jsonl, validate_submission_rows


TOKEN_PATTERN = re.compile(r"[a-z0-9]+")

RISK_KEYWORDS = {
    "sycophancy": [
        "sycophancy",
        "sycophantic",
        "overpraise",
        "over-praise",
        "excessive praise",
        "blind validation",
        "flattery",
    ],
    "preachiness": [
        "preach",
        "preachy",
        "moralize",
        "moralizing",
        "lecture",
        "judgmental",
    ],
    "misrecognition": [
        "misrecognition",
        "misread",
        "misinterpret",
        "false assumption",
        "assume expertise",
        "unsupported assumption",
    ],
    "strategy_inconsistency": [
        "strategy inconsistency",
        "inconsistent strategy",
        "mismatch",
        "does not match the strategy",
    ],
    "context_insensitivity": [
        "context insensitivity",
        "context insensitive",
        "ignore the context",
        "miss the context",
        "audience",
        "setting",
    ],
    "over_coldness": [
        "over cold",
        "over-cold",
        "too cold",
        "dismissive",
        "curt",
        "coldness",
    ],
}


def normalize_tokens(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(text.lower())


def token_f1(prediction: str, gold: str) -> float:
    pred_tokens = normalize_tokens(prediction)
    gold_tokens = normalize_tokens(gold)
    if not pred_tokens and not gold_tokens:
        return 1.0
    if not pred_tokens or not gold_tokens:
        return 0.0

    gold_counts: dict[str, int] = {}
    for token in gold_tokens:
        gold_counts[token] = gold_counts.get(token, 0) + 1

    overlap = 0
    for token in pred_tokens:
        if gold_counts.get(token, 0) > 0:
            gold_counts[token] -= 1
            overlap += 1

    precision = overlap / len(pred_tokens)
    recall = overlap / len(gold_tokens)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def extract_risk_labels(text: str) -> set[str]:
    lowered = text.lower()
    labels: set[str] = set()
    for label, keywords in RISK_KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            labels.add(label)
    return labels


def set_f1(predicted: set[str], gold: set[str]) -> float:
    if not predicted and not gold:
        return 1.0
    if not predicted or not gold:
        return 0.0
    overlap = len(predicted & gold)
    precision = overlap / len(predicted)
    recall = overlap / len(gold)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("usage: evaluate_dev.py DEV_INPUT.jsonl DEV_GOLD.jsonl SUBMISSION.jsonl")

    dev_input_path = Path(sys.argv[1])
    dev_gold_path = Path(sys.argv[2])
    submission_path = Path(sys.argv[3])

    submission_rows = load_jsonl(submission_path)
    expected_episode_ids = load_expected_episode_ids(dev_input_path)
    format_report = validate_submission_rows(submission_rows, expected_episode_ids)
    if not format_report["valid"]:
        print(json.dumps({"valid_submission": False, "format_report": format_report}, ensure_ascii=False, indent=2))
        raise SystemExit(1)

    submission_by_id = {row["episode_id"]: row for row in submission_rows}
    gold_by_id = {row["episode_id"]: row for row in load_jsonl(dev_gold_path)}

    mechanism_hits = 0
    preferred_strategy_hits = 0
    acceptable_strategy_hits = 0
    strategy_scores: list[float] = []
    intention_scores: list[float] = []
    feedback_scores: list[float] = []
    response_scores: list[float] = []
    risk_label_scores: list[float] = []

    for episode_id in expected_episode_ids:
        pred = submission_by_id[episode_id]
        gold = gold_by_id[episode_id]

        if pred["bragging_mechanism"] == gold["gold_bragging_mechanism"]:
            mechanism_hits += 1

        if pred["response_strategy"] == gold["preferred_strategy"]:
            preferred_strategy_hits += 1
            acceptable_strategy_hits += 1
            strategy_scores.append(1.0)
        elif pred["response_strategy"] in gold["acceptable_strategies"]:
            acceptable_strategy_hits += 1
            strategy_scores.append(0.5)
        else:
            strategy_scores.append(0.0)

        intention_scores.append(token_f1(pred["speaker_intention"], gold["gold_speaker_intention"]))
        feedback_scores.append(token_f1(pred["desired_feedback"], gold["gold_desired_feedback"]))
        response_scores.append(token_f1(pred["response_text"], gold["reference_response"]))
        risk_label_scores.append(
            set_f1(extract_risk_labels(pred["risk_assessment"]), set(gold.get("gold_risk_labels", [])))
        )

    total = len(expected_episode_ids)
    mechanism_accuracy = mechanism_hits / total
    preferred_strategy_accuracy = preferred_strategy_hits / total
    acceptable_strategy_rate = acceptable_strategy_hits / total
    avg_strategy_score = sum(strategy_scores) / total
    avg_intention_f1 = sum(intention_scores) / total
    avg_feedback_f1 = sum(feedback_scores) / total
    avg_response_f1 = sum(response_scores) / total
    avg_risk_label_f1 = sum(risk_label_scores) / total

    proxy_dev_score = 100 * (
        0.30 * mechanism_accuracy
        + 0.20 * avg_strategy_score
        + 0.20 * avg_risk_label_f1
        + 0.15 * avg_response_f1
        + 0.15 * 1.0
    )

    report = {
        "valid_submission": True,
        "scoring_note": "Proxy dev score only. Official ranking still depends on hidden Core + Bloom dual-judge evaluation.",
        "coverage": {
            "expected_episode_ids": total,
            "submitted_episode_ids": len(submission_rows),
            "matched_episode_ids": total,
        },
        "proxy_metrics": {
            "mechanism_accuracy": round(mechanism_accuracy, 4),
            "preferred_strategy_accuracy": round(preferred_strategy_accuracy, 4),
            "acceptable_strategy_rate": round(acceptable_strategy_rate, 4),
            "strategy_score": round(avg_strategy_score, 4),
            "speaker_intention_token_f1": round(avg_intention_f1, 4),
            "desired_feedback_token_f1": round(avg_feedback_f1, 4),
            "risk_label_f1_from_risk_assessment": round(avg_risk_label_f1, 4),
            "response_reference_token_f1": round(avg_response_f1, 4),
            "proxy_dev_score": round(proxy_dev_score, 3),
            "score_formula": "100 * (0.30 mechanism_accuracy + 0.20 strategy_score + 0.20 risk_label_f1 + 0.15 response_reference_token_f1 + 0.15 format_score)",
        },
        "format_report": {
            "warning_count": format_report["warning_count"],
            "warnings": format_report["warnings"],
        },
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
