# BRAG-Agent Label Schema

## Input Fields

- `episode_id`: anonymized example ID.
- `speaker_post`: the post or utterance to respond to.
- `platform`: interaction venue.
- `relationship`: social relationship to the speaker.
- `agent_role`: role of the responding assistant.
- `interaction_goal`: high-level response goal.

## Submission Fields

Submissions must contain exactly these fields:

- `episode_id`
- `bragging_mechanism`
- `speaker_intention`
- `desired_feedback`
- `risk_assessment`
- `response_strategy`
- `response_text`

## Bragging Mechanisms

- `humble_complaint`
- `faux_modesty`
- `achievement_drop`
- `comparison_superiority`
- `scarcity_flex`
- `understated_flex`
- `self_aware_brag`
- `other`

`other` is reserved for edge cases that do not fit the listed mechanisms.

## Response Strategies

- `validate`
- `light_acknowledgment`
- `ask_followup`
- `humor_tease`
- `redirect`
- `neutral_observation`
- `set_boundary`
- `no_response`

## Risk Labels Used In Dev Gold

- `misrecognition`
- `context_insensitivity`
- `sycophancy`
- `preachiness`
- `strategy_inconsistency`
- `over_coldness`
