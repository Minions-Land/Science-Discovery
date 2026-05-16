# Round Notes — R-future-3 4-task expansion

**Round:** R-future-3
**Date:** 2026-05-17
**Tasks:** 4 (gallery expansion + manifold fixture + radar fixture + vision-loop design)

## Status

- ✓ Task 1 manifold fixture — built, tested through 3 candidate iterations
- ✓ Task 2 radar fixture — built, tested through 2 candidate iterations
- ✓ Task 3 vision-loop design — design + skeleton complete, R-future-4
  validation pending API access
- ✓ Task 4 gallery expansion — 4 forms generated, 3 accepted (ridgeline,
  beeswarm, parallel coords v3), 1 rejected (sankey)

## Per-task verdict

### Task 1: manifold form
- v1 (PCA scatter colour by cluster, no skill) — baseline default
- v2 (cluster identity only, drop trajectory + bifurcation) — too sparse
- v3 (bigger points + convex-hull shading + tight axes) — pending user grade

User R-future-3 v2 grade: "颜色 OK 但点太小+散". Surfaced new P3 sub-rule
(scatter-point size). Encoded in aesthetic-principles.md.

### Task 2: radar form
- v1 (legend overlap + saturation-gradient single hue) — fail
- v2 (legend off-plot + 5 distinct pastel hues) — better but still loses
  to comparison_radar reference

User R-future-3-final: "对于 Radar，你可以直接把 Reference 当成模板了."
Decision: comparison_radar is the LITERAL template (P9 anchor). Skill
now points to it as the canonical polar reference.

### Task 3: vision-iterative-loop design
Complete design document at `workflow/vision-iterative-loop.md`. Two
deployment options (Anthropic API direct OR Codex sandbox vision).
Implementation skeleton with judge / apply_deltas / loop_driver
functions. Not validated yet — requires API key OR Codex vision MCP
surface.

### Task 4: gallery expansion
- ridgeline ✓ accepted (still room for tail-trim improvement)
- beeswarm ✓ accepted, **beat reference bar exemplar** ("左边好看")
- sankey ✗ rejected ("节点很普通，flow 用来掩盖矩形丑")
- parallel coords v3 ✓ accepted ("Three Distinct Pastel 配色已经不错了")

## R-future-3-final aesthetic-principles updates

| Principle | Update | Source |
|---|---|---|
| P1 hue coherence | **CORRECTED**: ≥3 distinct hues within family OK; NOT saturation-gradient single-hue | parallel coords v1/v2 user feedback |
| P3 effective area | NEW sub-rule: scatter point size ~28+ for hero, with hull shading | manifold v2 user feedback |
| P7 (NEW) | Legend off-plot for polar / overlay-dense plots | radar v1 user feedback |
| P8 (NEW) | Manifold carries 1-2 info dimensions MAX | manifold v1 user feedback |
| P9 (NEW) | comparison_radar is the literal template; do NOT improve, just diff | radar v2 user feedback |

9 principles + 12 sub-rules. The skill is now mature for SkillTest port.

## Cross-skill anchor still holds (now 7 fixtures)

> **Substantively-bounded specificity, not vague good-faith promises.**

R-future-3 adds: each new principle is grounded in a SPECIFIC user
flagged failure (point size in pixels, legend position in matplotlib
syntax, hue distinguishability in HEX). No vague "make it pretty" rules.

7 fixtures cumulative now: R1.C overclaim + R2 rebuttal + R3.A data
avail + R3.B citation + R5.A end-to-end + R-future palette + R-future-3
manifold/radar/parallel-coords.

## What R-future-3 leaves open

1. **Manifold v3** still pending user grade. Could be R-future-4 follow-up.
2. **Vision-loop validation** awaits API access. R-future-4 should run
   it on R5.C 7-panel as starting point.
3. **3 exemplars without annotation cards**: manifold_holes,
   cellsplicenet_ablation, atlas-image-plates. Author when next fixture
   demands their archetype.

## Recommendation

`figure-aesthetic-exemplars` skill is now mature for the SkillTest port
plan. The 9-principle + 12-sub-rule + 13-exemplar combo, plus the
diff-and-revise workflow, plus the vision-loop design (skeleton),
covers the figure-aesthetic gap that R6.A surfaced.

Next user decision: land R1-R6 + R-future-1/2/3 ports together, or
run R-future-4 (vision-loop validation) first.
