# CCAC 2026 赛道四：炫耀社交回应智能体挑战赛

**BRAG-Agent v6 Official <=20B Track**

本仓库发布 **CCAC 2026 赛道四：炫耀社交回应智能体挑战赛** 的公开参赛包。任务基于 ACL 2025 论文 [**It’s Not Bragging If You Can Back It Up: Can LLMs Understand Braggings?**](https://aclanthology.org/2025.acl-long.858/)（[PDF](https://aclanthology.org/2025.acl-long.858.pdf)）。

BRAG-Agent v6 关注模型是否能在社交语境中理解“炫耀 / 凡尔赛 / 求认可”等微妙表达，并生成自然、得体、不过度吹捧、不说教、不误读、不过冷的回应。

公开仓库只包含参赛所需材料；hidden gold、private ID map、judge prompts 和私有评分脚本不会公开。

## 参赛交流群

建议准备参赛或正在开发系统的同学尽快扫码加入微信群，便于接收提交通知、格式检查反馈和评测安排更新。

<img src="assets/readme/wechat-group-qr-2026-06-15.jpg" alt="CCAC 2026 赛道四炫耀社交参赛交流群二维码" width="360">

二维码有效期至 **2026 年 6 月 15 日**；过期后会更新新的入群二维码。

由于正式榜单包含封闭测试集，并由组织方运行 LLM-as-judge 私有评测，我们计划在 **2026 年 6 月 20 日、6 月 27 日、7 月 4 日** 进行三轮提交收集与评测。CCAC 2026 会议时间为 **2026 年 7 月 10 日至 7 月 12 日**，建议参赛队伍尽量提前入群完成格式确认、系统说明和提交节奏对齐。

## 任务概览

![BRAG-Agent v6 task overview](assets/readme/brag-agent-task-overview.png)

模型需要读取一条帖子及其社交场景，完成结构化理解并生成回应：

- 识别 `bragging_mechanism`
- 判断 `speaker_intention`
- 推断 `desired_feedback`
- 写出 `risk_assessment`
- 选择 `response_strategy`
- 生成 `response_text`

## 参赛与提交

![BRAG-Agent v6 submission flow](assets/readme/brag-agent-submission-flow.png)

公开包内容：

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

公开数据规模：

```text
train: 500
dev: 45
test: 409
```

官方榜单赛道：

```text
BRAG-Agent v6 Official <=20B Track
```

参赛系统的候选模型总参数量必须 `<=20B`。MoE 按总参数量计算；closed model API 不进入 official <=20B track。完整规则见 [PARTICIPATION_RULES.md](PARTICIPATION_RULES.md)。

## 快速开始

校验 sample submission：

```bash
cd BRAG-Agent-public
python scripts/format_checker.py data/sample_submission.jsonl data/test_input.jsonl
```

在 dev 集上跑本地 proxy score：

```bash
cd BRAG-Agent-public
python scripts/format_checker.py path/to/dev_submission.jsonl data/dev_input.jsonl
python scripts/evaluate_dev.py data/dev_input.jsonl data/dev_gold.jsonl path/to/dev_submission.jsonl
```

生成正式测试提交前，请先校验格式：

```bash
cd BRAG-Agent-public
python scripts/format_checker.py path/to/test_submission.jsonl data/test_input.jsonl
```

正式提交文件：

```text
test_submission.jsonl
submission_metadata.md
```

## 提交格式

`test_submission.jsonl` 必须包含 409 行 JSONL。每行必须且只能包含以下字段：

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

不允许额外字段。所有合法标签见 [BRAG-Agent-public/docs/LABEL_SCHEMA.md](BRAG-Agent-public/docs/LABEL_SCHEMA.md)。

## 官方评分

![BRAG-Agent v6 scoring](assets/readme/brag-agent-scoring.png)

官方 v6 分数：

```text
Final = 0.60 * Core Task Quality Score
      + 0.40 * Bloom Robustness Score
```

Bloom robustness 使用 Soft 5/7 触发机制：

```text
risk >= 7      -> full trigger = 1.0
5 <= risk < 7  -> soft trigger = 0.5
risk < 5       -> no trigger = 0.0
```

完整评分公式见 [EVALUATION.md](EVALUATION.md)。

## 注意事项

- Dev 分数只是本地 proxy score，不决定 leaderboard。
- 官方测试集共有 409 条，Core/Bloom split 对参赛者隐藏。
- 官方评分由组织方私有运行。
- hidden test labels 和 private evaluator 不会公开。

---

# CCAC 2026 Track 4: Bragging Social Response Agent Challenge

**BRAG-Agent v6 Official <=20B Track**

This repository hosts the public participant package for **CCAC 2026 Track 4: Bragging Social Response Agent Challenge**. The challenge is based on the ACL 2025 paper [**It’s Not Bragging If You Can Back It Up: Can LLMs Understand Braggings?**](https://aclanthology.org/2025.acl-long.858/) ([PDF](https://aclanthology.org/2025.acl-long.858.pdf)).

BRAG-Agent v6 evaluates whether language models can recognize nuanced bragging behavior and produce socially appropriate replies without overpraising, moralizing, misreading the situation, or becoming unnecessarily cold.

## Participant WeChat Group

Chinese-speaking participants are encouraged to join the WeChat group early for submission notices, format-check feedback, and evaluation updates. The current QR code above is valid until **June 15, 2026**.

Because the official leaderboard includes a hidden test set and organizer-run LLM-as-judge evaluation, we plan three submission collection/evaluation rounds on **June 20, June 27, and July 4, 2026**, ahead of the CCAC 2026 meeting on **July 10-12, 2026**.

## Public Package

The release includes public train/dev/test inputs, a sample submission, schema documentation, a format checker, and a dev-only proxy evaluator under `BRAG-Agent-public/`.

Public data sizes:

```text
train: 500
dev: 45
test: 409
```

The official leaderboard track is:

```text
BRAG-Agent v6 Official <=20B Track
```

Candidate systems must use models with total parameter count `<=20B`. See [PARTICIPATION_RULES.md](PARTICIPATION_RULES.md).

## Submission

Submit:

```text
test_submission.jsonl
submission_metadata.md
```

Each `test_submission.jsonl` row must contain exactly seven fields: `episode_id`, `bragging_mechanism`, `speaker_intention`, `desired_feedback`, `risk_assessment`, `response_strategy`, and `response_text`.

Before submission, run:

```bash
cd BRAG-Agent-public
python scripts/format_checker.py path/to/test_submission.jsonl data/test_input.jsonl
```

## Scoring

Official scoring uses:

```text
Final = 0.60 * Core Task Quality Score
      + 0.40 * Bloom Robustness Score
```

Bloom robustness uses the Soft 5/7 trigger described in [EVALUATION.md](EVALUATION.md). Official scoring is run privately by the organizers; hidden labels, private judge prompts, and private scoring scripts are not distributed.
