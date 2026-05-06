生成一张 16:9 横版 4K 中文高密度研究汇报图版，APIMart gpt-image-2。主题：BRAG-Agent v6 发布包边界。风格：ACL/NeurIPS/ICML survey figure，off-white 背景，细墨线，muted blue/teal/green/orange，专业信息图，不是海报。必须只围绕 BRAG-Agent v6，不要任何无关例子。标题：『发布包边界：公开开发，私有评测』。布局 5 区域：(1) 左侧文件树『BRAG-Agent-public/』，只写 train.jsonl 500、dev_input.jsonl 45、dev_gold.jsonl 45、test_input.jsonl 409、sample_submission.jsonl 409、docs/、scripts/format_checker.py；(2) 中央流程『参赛者流程』：LABEL_SCHEMA -> train/dev -> test_submission.jsonl -> format_checker；(3) 右侧锁定模块『private evaluation』：hidden gold withheld、private ID map withheld、judge prompts withheld、private evaluator withheld、API keys withheld、concrete judge names withheld；(4) 底部结构条：Core 206 + Bloom 203 = 409，标注 split private；(5) 小角标：Official <=20B Track，MoE 按总参数量，closed API non-eligible。强制禁止：不要出现游戏、植物、数学题、T0001、T0409、id/input/answer、RAG、假 difficulty distribution、假 baseline、具体 judge 模型名或 API key。

High-density plate contract:
- Render as a high-density visual plate, not a sparse social card.
- Density: paper-survey.
- Output language: zh.
- Language instruction: Use Chinese for human-readable titles, section labels, callouts, and takeaways. Keep equations, variable names, model names, dataset names, layer/head IDs, and standard method names in English when clearer.
- Mode: paper-survey
- Layout mold: method-pipeline
- Main thesis: BRAG-Agent v6 的发布设计是 public participant package 与 private hidden evaluation 严格分离。
- Why needed: 老师需要确认哪些文件可以发布、哪些必须保密，以及官方 <=20B track 的边界。
- Visible text: [
  "BRAG-Agent v6",
  "BRAG-Agent-public/",
  "train.jsonl 500",
  "dev_input.jsonl 45",
  "dev_gold.jsonl 45",
  "test_input.jsonl 409",
  "sample_submission.jsonl 409",
  "docs/",
  "scripts/format_checker.py",
  "private evaluation",
  "hidden gold withheld",
  "private ID map withheld",
  "judge prompts withheld",
  "private evaluator withheld",
  "API keys withheld",
  "Core 206 + Bloom 203 = 409",
  "Official <=20B Track"
]
- Panel plan: [
  "左侧：公开包文件树，只列出 BRAG-Agent-public 真实文件和数字",
  "中间：参赛者流程 LABEL_SCHEMA -> train/dev -> test_submission.jsonl -> format_checker",
  "右侧：私有评测保险箱，只写 withheld，不写具体 judge 模型名",
  "底部：409 hidden evaluation 被分成 Core 206 与 Bloom 203，标注 split private",
  "右下：official <=20B track 规则简表"
]
- Information slots: {
  "main_thesis": "public/private split protects usability and leaderboard validity",
  "mechanism": "participants see only public inputs and scripts; organizers run private scoring",
  "evidence": "500 train, 45 dev, 409 test input, 409 sample submission, format checker",
  "takeaway": "公开包可以发布，private eval 不能发布"
}
- Evidence anchor: TEACHER_BRIEF_ZH.md sections 1, 3, 9
- Text budget: 中文短标签；英文文件名和公式保留；不要段落；不要密密麻麻小字。
- Regenerate if: 出现游戏/植物/通用 QA 样本、T0001/T0409/id-input-answer、RAG、具体 judge model name、API key、假 baseline 或假分布。
- Concept mapping: 公开包是参赛者工作台，私有评测是封存评分器。
- Required labeled regions: main thesis, mechanism, evidence, takeaway.
- Use 4-6 labeled regions when density is paper-survey; story-hook plates should keep the metaphor compact and include a technical mapping inset.
- Include at least two of these technical supports when relevant: formula, variable legend, diagnostic plot, ablation, comparison, concrete example, limitation.
- Keep labels concise; no paragraph blocks; no decorative hero poster; no large empty metaphor scene.

Variant focus: evidence-dense. Emphasize diagnostics, ablations, examples, comparison panels, and a compact takeaway while preserving the same main thesis.
Keep the plate constrained to one main thesis. Supporting modules are expected, but do not add an unrelated second thesis.
Make the result look like a dense research-paper survey figure, not a title slide, poster, or decorative illustration.
Variant id: 03-evidence-dense.
