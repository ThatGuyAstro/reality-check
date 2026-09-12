# Baseline: the honeyflow-web run (2026-09-11), read-only analysis

A full `/reality-check` run of the merged skill against a large production Next.js app
(18 surfaces, live account, 68 minutes, 25 parallel browser lanes). The owner's verdict:
"did a very poor job at actually using the UI and providing actual UI bugs and design
flaws." This document records what the artifacts show, so the fix can be graded against it.
Nothing in the target repo was modified.

## What the numbers say

| Measure | Value | Reading |
|---|---|---|
| Claims by kind | exists 54, shows 52, does 36, flows 14, state 2, looks 0, promise 0 | 67% of the tour asserts that things are present or read a string. Nothing predicts how a component looks in any state. Two claims in 158 concern persistence. |
| Findings by category | color-contrast 23, hit-areas 18, accessibility 7, content 4, states 3, typography 3, layout 3, navigation 2, functional-affordance 2, hierarchy 2, motion 0, polish 0 | 61% of design findings are two numbers axe could produce. Three findings in 67 concern a component state. |
| Screenshots | 289 total: 158 claim, 38 observation, 24 before-shots, 4 finding shots, 1 hover, 1 dialog, 1 picker, 3 focus walks | The verify pass photographed pages, not states. 67 findings share 4 finding screenshots; the rest reuse claim captures that do not show the finding. |
| Verification vocabulary | "hover" appears 14 times in 18 verification files, "loading" 2, "empty state" 3, "error state" 1, "animation" 2 | The browser pass never drove components through their states on purpose. |
| Design-system promises checked | dark mode: 0 surfaces (design.md declares light and dark); reduced motion: 1 surface of 18; breakpoints: one 960x540 pass, none of the four declared bands (560, 900, 1160, 1220) | The rubric read the design system correctly and then the pass ignored most of it. |
| Observations `source` | 93 rows, 0 with a source value | Schema field never filled; nothing distinguishes a sweep hit from a human-eye note. |

## What a design-literate reviewer sees in the same screenshots

Two captures the run took, re-read by a person:

- Chat overview: a one-row table whose only column header is a raw uppercase "LABEL" with a
  sort caret; an inline code block carrying a machine team id in the middle of a sentence; a
  pin glyph floating under every answer with no label; the same four feedback buttons repeated
  under every turn so the transcript reads as chrome; chips at the bottom of the thread
  ("Team Not Found x2", "Agent (2)") whose meaning is not recoverable from the screen. The run
  filed the raw provider path in the model stamp and nothing else on this screen.
- Inbox overview: five identical rows reading "Short Squeeze Finder's confer closed as failed
  (orchestrator_error)", a raw error code in user copy, repeated five times with no grouping;
  an "Unread 27,558" count with a five-row window under it; mark-as-read controls that exist
  only on pointer hover. The run filed the hover-only control and the count. It did not file
  the raw code, the duplication, or the grouping.

The gap is not measurement precision. It is that the critique had no vocabulary for hierarchy,
grouping, repetition, signifiers, or state completeness, and the verify pass had no procedure
that would put a component into a state and photograph it.

## Five failure classes, each with the rule that must close it

| # | Failure | Where it came from | Rule needed |
|---|---|---|---|
| B1 | No state claims. The tour never said "when I hover a row a check appears", "while the answer streams the send button becomes Stop", "with no connections the page shows ...". | Phase 1 reads handlers and copy; it never reads `:hover`, `:focus-visible`, `[aria-expanded]`, `loading.tsx`, empty branches, media queries as claims. | A state inventory per surface (components.md) and at least one `looks`/`state` claim per declared state. |
| B2 | No state exercise. The verify pass confirmed existence and text, then swept a11y and contrast. | The per-kind sequences only cover the claim's own trigger; nothing drives hover, focus, pressed, disabled, loading, empty, error, open/closed, dark, narrow. | A component state pass per surface with a screenshot and a computed-style diff per state, and a page dynamics pass (breakpoint ladder, theme modes, reduced motion, overlays, forms, data volume, offline). |
| B3 | Mechanical findings drown design. 41 contrast and hit-area rows across 14 surfaces, most from the same five grey tokens and three control rules. | The critique files one finding per element per surface and only clusters when it remembers to. | One systemic finding per rule or token, cross-surface, with locations listed; the per-surface critique leads with the design read. |
| B4 | No design vocabulary. Hierarchy, grouping, repetition, signifier confusion, raw identifiers, empty-state quality, consistency across surfaces are not lenses the rubric names with a measurable signature. | critique-rubric.md's category table is an a11y and layout table with a "polish" row. | Named heuristics (Nielsen, Gestalt, Norman, Fitts) each with a violation signature and the evidence that proves it; a cross-surface consistency section. |
| B5 | Finding evidence is not evidence. 63 of 67 findings point at a page or claim screenshot that does not show the finding. | The rule "every finding gets a screenshot" was satisfied by reuse. | A finding's screenshot is an element capture or an annotated crop showing the measured thing, in the state that shows it. |

## Things the run did well, to keep

The rubric derivation read design.md, accessibility.md, motion.md, and the component catalog
and produced twelve expectations with citations; the hidden-control sweep fired; the
Impression paragraphs are honest; 45 contradictions and 93 observations are real product
issues (dead-end run pages, disabled backtests with no inline reason, a share panel that does
not trap focus, wire event names as user copy); the pointer-click rule absorbed a flaky
scroll-container click without a false ticket; no ticket was filed against a working path.

## The fix, and how it is graded

Rules added (skill text as of this commit): `references/ui-state-model.md` (state axes, component
state sets, page dynamics, code signals, named heuristics with violation signatures); a state
inventory per surface (`components.md`) and `looks`/`state` claims per declared state in the tour; a
component state pass and a page dynamics pass in verification writing `states.jsonl` with one element
screenshot per state; a critique that leads with a design read, a state matrix, and a transformations
table, and reports floors as systemic clusters; findings whose screenshot must show the finding.

GREEN instrument: `fixtures/orbit` (a task board with 16 planted state, transformation, and design
defects that no static audit finds: hover-only actions, an untrapped dialog, a menu that never closes,
a bare empty state, a skeleton that never resolves, a form that names no field, a disabled control with
no reason, dark-mode white islands, a breakpoint that overlaps and overflows, link-as-button and
button-as-link, raw identifiers, per-card repetition, layout motion on hover and a meaningless pulse
that ignores reduced motion, a sticky toolbar covering an anchor, a 700 ms toast, and a global
`outline: none` on buttons), with working states that must not be ticketed. `grade.py --fixture orbit`
checks every plant surfaced and ticketed, the systemic focus-ring cluster, the working paths, and the
structural requirements (states.jsonl, components.md, the three critique sections, finding screenshots
that are not page captures, breakpoint and dark and reduced-motion rows).
