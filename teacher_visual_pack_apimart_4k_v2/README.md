# BRAG-Agent v6 APIMart 4K Visual Pack v2

This folder contains APIMart-generated 4K images for the teacher briefing.

## Output

- 3 plates
- 3 candidates per plate
- 9 total images
- all images are `3840 x 2160`
- no SVG files are used

## Candidate Folders

- `images/01-figure/`
  - 发布包边界：公开开发，私有评测。
- `images/02-7-jsonl/`
  - 单条 BRAG-Agent 样本如何变成 7 字段 JSONL。
- `images/03-soft-bloom-final-score/`
  - Soft 5/7 + Final score 计算。

## Recommended Picks

Recommended copies are in `selected/`:

- `selected/01-release-boundary-selected.png`
- `selected/02-jsonl-example-selected.png`
- `selected/03-soft-bloom-selected.png`

## QA Note

The v2 prompts explicitly forbid unrelated test examples such as games, plants, generic QA, `T0001`, `T0409`, and `id/input/answer` style fake samples.

Manual visual check found the generated candidates stay on the BRAG-Agent topic. As usual with image-model text rendering, some tiny labels may have minor glyph drift; use the selected files for the cleanest briefing version.
