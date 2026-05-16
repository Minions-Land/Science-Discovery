# Round Notes — R-future-2 aesthetic-principles refinement

**Round:** R-future-2
**Date:** 2026-05-17
**Method:** User visual grading of 6 novel-form exemplars + extraction of
the 3 named principles into specific sub-rules.

## Headline

User explicitly named the missing aesthetic axis: 形式新颖 + 信息密度 +
色调一致 + 饱和度淡 + 排版有效面积. R-future-2 graded 6 novel-form
exemplars to validate where each principle bites and surface 6 new
sub-rules.

## User grades by exemplar (from feedback)

| Exemplar | Form | Grade | What worked / what didn't |
|---|---|---|---|
| diffusion_swiss_roll | manifold | **非常好看** | pure cyan-teal hue family; geometric structure IS the message |
| manifold_holes | manifold + topology | 不错 | mint+cyan low-saturation; 整个流形系列挺不错 |
| cellsplicenet_ablation | hybrid (heatmap+bar+scatter) | 挺好看 | configure issue: legend should be ncol=2 to remove upper-left whitespace |
| atlas-network-matrix | network + matrix | **非常漂亮** (network half) + 配色不行 (matrix half) | network section is teal-coherent; matrix uses red+teal complementary which user flagged as ugly |
| comparison_radar | polar / radar | **非常漂亮! 真的太漂亮了** | 77% grey + soft pastel polygons; 唯一缺点 polygon stroke 太细需要加粗 |
| atlas-image-plates | microscopy plate | 没什么大问题 | A-P 排列可以再紧凑一点 (gutter ≤2%) |

## 6 new sub-rules added

| Sub-rule | Source feedback | Where it lives now |
|---|---|---|
| P1: red-vs-teal complementary > 40% sat is bad | atlas-network-matrix matrix half | aesthetic-principles.md Principle 1 sub-rule |
| P2: pastel fills need 2x stroke weight to compensate | comparison_radar 边可以再粗 | aesthetic-principles.md Principle 2 sub-rule |
| P3: legend packing ncol≥2 for hybrid composites | cellsplicenet_ablation legend | aesthetic-principles.md Principle 3 sub-rule |
| P4: image plate gutter ≤ 2% canvas | atlas-image-plates 紧凑 | aesthetic-principles.md Principle 4 sub-rule |
| P5: manifold > flat chart when geometry IS the message | diffusion_swiss_roll + manifold_holes | aesthetic-principles.md Principle 5 sub-rule |
| P6 (NEW): polar/radar > bar for N×M cross-comparison with M≥3 | comparison_radar 非常正规、正经 | aesthetic-principles.md Principle 6 (new) |

## 3 new exemplar annotation cards written

- diffusion_swiss_roll.annotation.md — manifold archetype, pure cyan-teal
  family, "geometric structure IS the message" framing
- atlas-network-matrix.annotation.md — network archetype with matrix
  matrix-half-fix recommendation; demonstrates Principle 1 violation
  (red+teal) being explicitly flagged
- comparison_radar.annotation.md — polar archetype, 77% grey foreground,
  documented stroke-weight compensation rule

Total annotation cards now: 8 of 11 exemplars (3 still pending:
manifold_holes, cellsplicenet_ablation, atlas-image-plates).

## What R-future-2 confirmed

The "rules can't produce beauty" hypothesis from R-future continues to
hold partially:
- Some aesthetic axes (色调一致 hue coherence, 饱和度淡 reduced
  saturation, 有效显示面积 effective area) ARE rule-encodable now that
  user has named them concretely.
- Form novelty (manifold, polar, network, plate) IS exemplar-based
  not rule-based — the gallery has to grow.
- Specific deltas (legend ncol, stroke weight for pastels, image plate
  gutter ≤2%) are micro-rules that catch failure modes amateur figures
  hit.

## Open questions for R-future-3

1. **Build a SkillTest fixture that demands manifold form.** Currently
   our 14 figure cases are all bar/line/heatmap/scatter. A fixture
   demanding "visualise this 2D embedding's manifold structure" would
   force the candidate to use diffusion_swiss_roll-style and let us
   validate whether candidate-with-skill makes the form choice that
   amateur-no-skill misses.

2. **Build a SkillTest fixture that demands radar.** Similar — a multi-
   metric cross-method comparison fixture.

3. **Vision-capable iterative loop.** R-future-2 worked because user
   was the visual judge. Future R-rounds should test whether a vision-
   capable model (Sonnet 4.6 / Opus 4.7 with images) can JUDGE the
   aesthetic compliance, not just generate the figure. If yes, the
   exemplar paradigm becomes self-validating.

4. **Add more exemplar diversity.** Current gallery: 11 exemplars across
   bar / heatmap / multi-panel / manifold / network / plate / polar.
   Missing: ridgeline plots, beeswarm / strip plots, alluvial /
   sankey, parallel coordinates. Each is a distinct form-novelty
   class.

## Recommendation

`figure-aesthetic-exemplars` skill is now mature enough for the
SkillTest port plan with the R-future-2 sub-rules included. The skill
covers:
- 6 named aesthetic principles
- 11 exemplars (8 with annotation cards)
- diff-and-revise workflow
- typography reference
- palette extraction script

The remaining work for R-future-3+ is gallery diversity + vision-
capable validation, not core skill architecture.

## Status of the figure-aesthetic-exemplars proposed skill

- SKILL.md ✓
- aesthetic-principles.md ✓ (6 principles + 6 sub-rules)
- workflow/diff-and-revise.md ✓ (with current-rules audit patch)
- typography/reference.md ✓ (4-step ladder)
- palettes/extract.py ✓ (no-sklearn binning extractor)
- palettes/extracted-palettes.json ✓ (11 exemplars)
- gallery/ 11 exemplar PNGs ✓
- gallery/ 8 annotation cards ✓ / 3 pending
- gallery/index.md ✓
