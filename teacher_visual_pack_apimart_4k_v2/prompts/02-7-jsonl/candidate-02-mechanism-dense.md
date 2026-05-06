生成一张 16:9 横版 4K 中文高密度研究汇报图版，APIMart gpt-image-2。主题：BRAG-Agent 单条真实样本如何变成 7 字段 JSONL。风格：ACL/NeurIPS/ICML survey figure，off-white 背景，细线框，muted teal/blue/orange，机制图，不是海报。只能使用这个真实 BRAG-Agent 公开训练样本：episode_id = train_seed_000001_a；speaker_post = “Covid really brought these antique contacts out of the woodwork! I forgot how vast my network is..”；platform = direct_message；relationship = close_friend；agent_role = friend；interaction_goal = be_supportive_without_overpraising。布局 5-6 区域：(1) 左侧输入卡，显示上述真实字段；(2) 中央放大镜 bragging_mechanism = understated_flex，标注『表面：旧联系人出现』『隐含：network 很大』；(3) 小模块 speaker_intention、desired_feedback、risk_assessment；(4) 风险镜头：avoid sycophancy、preachiness、misrecognition、over_coldness；(5) 底部代码样式 schema，只列七字段：episode_id、bragging_mechanism、speaker_intention、desired_feedback、risk_assessment、response_strategy、response_text；(6) 右下 good reply：response_strategy = light_acknowledgment；response_text = “Haha, Covid definitely had people resurfacing out of nowhere.” 强制禁止：不要出现 id/input/answer 通用格式，不要 T0001/T0409，不要游戏、植物、数学题、地理题或任何非 BRAG-Agent 例子，不要 acknowledge_context，不要编造字段。

High-density plate contract:
- Render as a high-density visual plate, not a sparse social card.
- Density: paper-survey.
- Output language: zh.
- Language instruction: Use Chinese for human-readable titles, section labels, callouts, and takeaways. Keep equations, variable names, model names, dataset names, layer/head IDs, and standard method names in English when clearer.
- Mode: paper-survey
- Layout mold: mechanism-map
- Main thesis: 参赛模型必须把真实社交发言解析成结构化判断，并生成不过度吹捧的回应。
- Why needed: 用一个真实公开训练样本说明任务，不让读者误以为这是普通 QA 或普通聊天。
- Visible text: [
  "train_seed_000001_a",
  "Covid really brought these antique contacts out of the woodwork!",
  "I forgot how vast my network is..",
  "direct_message",
  "close_friend",
  "be_supportive_without_overpraising",
  "understated_flex",
  "speaker_intention",
  "desired_feedback",
  "risk_assessment",
  "avoid sycophancy",
  "light_acknowledgment",
  "response_text",
  "Haha, Covid definitely had people resurfacing out of nowhere."
]
- Panel plan: [
  "左上：真实输入卡，episode_id=train_seed_000001_a，speaker_post 是 Covid/vast network 例子",
  "中上：机制放大镜，表面旧联系人出现，隐含 network 很大，标签 understated_flex",
  "右上：风险镜头，avoid sycophancy/preachiness/misrecognition/over_coldness",
  "下方：7 字段 JSONL schema，只列七个字段",
  "右下：合格回复气泡，策略 light_acknowledgment，示例回复为 Covid resurfacing"
]
- Information slots: {
  "main_thesis": "social meaning must be recognized before choosing the reply",
  "mechanism": "input context -> bragging mechanism -> intention/feedback/risk -> response strategy -> JSONL",
  "evidence": "public train example train_seed_000001_a",
  "takeaway": "好回复识别炫耀，但不放大炫耀"
}
- Evidence anchor: TEACHER_BRIEF_ZH.md section 7
- Text budget: 只使用简短中文标签和必要英文 schema 字段；不要长段落。
- Regenerate if: 出现 id/input/answer、T0001/T0409、游戏/植物/数学题、acknowledge_context、非真实样本或非七字段 schema。
- Concept mapping: 一句社交帖子映射成机制、意图、期望反馈、风险和回应策略。
- Required labeled regions: main thesis, mechanism, evidence, takeaway.
- Use 4-6 labeled regions when density is paper-survey; story-hook plates should keep the metaphor compact and include a technical mapping inset.
- Include at least two of these technical supports when relevant: formula, variable legend, diagnostic plot, ablation, comparison, concrete example, limitation.
- Keep labels concise; no paragraph blocks; no decorative hero poster; no large empty metaphor scene.

Variant focus: mechanism-dense. Emphasize causal arrows, intermediate representations, equations, variable legends, and the exact computational pathway behind the main thesis.
Keep the plate constrained to one main thesis. Supporting modules are expected, but do not add an unrelated second thesis.
Make the result look like a dense research-paper survey figure, not a title slide, poster, or decorative illustration.
Variant id: 02-mechanism-dense.
