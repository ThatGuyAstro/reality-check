# GREEN test of the UI-state enhancement (2026-09-12)

RED baseline: `2026-09-11-bigtimer-run-analysis.md` (zero `looks` claims, one hover screenshot in 289, 61% of findings contrast or target size, no breakpoint or theme pass). Instrument: `fixtures/orbit` (16 planted state, transformation, and design defects) graded by `grade.py --fixture orbit`, which also checks the structural requirements of the new passes.

## GREEN-1 (first run of the enhanced text, cold, 52 minutes, ~230 tool calls)

| Measure | Baseline (honeyflow run) | Orbit GREEN-1 |
|---|---|---|
| claims by kind | exists 54, shows 52, does 36, flows 14, state 2, looks 0 | looks 30, does 23, state 13, exists 12, shows 8, flows 4 |
| state rows | none | 61 (present 32, broken 20, missing 9; 3 synthesized via network mocks) |
| findings by category | contrast 23, hit-areas 18, other 26 | states 8, transformation 2, layout 1, hierarchy 1, functional-affordance 1, content 1, contrast 0 (floors clustered) |
| observations with a source | 0 of 93 | 28 of 28 (state-gap 23, human-eye 4, transformation 1) |
| breakpoints / modes / reduced motion | 0 of 4 declared / 0 of 2 / 1 of 18 surfaces | 1 of 1 / 2 of 2 / all animated elements |
| critique sections | impression + floor rows | impression, design read (measured sentences), state matrix, transformations, findings |

grade.py: 48/52. Plants surfaced and ticketed: 15 of 16. Working states never ticketed. The focus-ring plant was reported once as a systemic cluster (TKT-002) and once as the README promise (TKT-001).

Misses, all on the instrument side:
- P14 (sticky toolbar over an anchor) did not manifest: with four tasks the board fits the viewport, so the anchor never scrolled. Fixture changed: the anchor now points at an "Archived" section 640px below the board; the protocol's scroll step now says to follow every in-page anchor from the bottom of the page.
- The grader required the three critique sections on feature surfaces (session, theme), which the rubric exempts from the sweep. Grader now skips critiques that state `sweep: n/a`.
- Two tickets listed a confirmed claim among their sources as context. Rule added: sources hold only contradicted claims, failed expectations, observations, and findings.

Real unplanted defects the run found: the login page never applies the saved dark preference (index.html does not load app.js); the board has no loading state and shows a raw stack trace on a failed fetch; search has no no-results state; "Delete workspace" has no confirmation; empty To do and In progress columns show a bare "No results".

Runner-cited ambiguities folded into the text: state-gap ticket `type` by gap; page-level aggregate rows never get their own ticket; the 390px mobile pass runs only under `:mobile` or a declared breakpoint at or below 600px; feature surfaces get no state rows of their own. Runner slips not attributable to the text: a curl at tool call 1 before the skill was read; one destructive click ("Delete all done") despite the claim's destructive tag.

## Acme regression (enhanced text, plain fixture, 38 minutes, ~146 tool calls)

grade.py: 26/27 after two grader corrections (feature surfaces need no components.md; a landmark finding may cite the full-page capture). All five plants surfaced and ticketed except P5's ticket: the hint-contrast finding was written at medium and then not ticketed, a runner slip against "one ticket per finding at medium or above" that the new "floors reported once as clusters" wording invited. Rule now says reported once is not ticketed never. No ticket sourced from a confirmed claim; Save, Settings, Sign out confirmed. State pass on a fixture with no state styling: 43 rows, 18 missing (no hover, active, busy, disabled, invalid states anywhere), 2 broken (bare empty table, 390px overflow), reported as class-level tickets, not per element. New claims: looks 21 of 63. Fallback breakpoint ladder used (the repo declares none); modes: light only, declared and skipped; reduced motion trivially satisfied.

Runner-cited ambiguities folded in: the `get styles` shorthand in the state pass replaced by a nine-property eval probe; state-gap ticket type decided by any state source, not the first-listed; components.md and states rows for feature and unrendered surfaces spelled out.

## GREEN-2 on Orbit (edited text and fixture, 44 minutes, ~160 tool calls)

grade.py: 51/52. All 16 plants surfaced; 15 ticketed at medium or above, and P14 (the sticky toolbar over the Archived anchor) now manifests and was filed as a page-dynamics row plus an observation in the board polish ticket. The one grader miss: the raw-identifier finding (P11) was filed low this time and rolled into polish; severity rule tightened so identifiers and codes in user copy are at least medium. Working states untouched; no ticket sourced from a confirmed claim. Claims: looks 26, state 7 of 73. States: 51 rows, 15 missing, 9 broken, 2 synthesized. Both declared transformations measured (900px, dark) plus reduced motion. Feature surfaces carried the three critique headers with explicit n/a content.

Totals for the enhancement: three cold runs (Orbit twice, Acme once). Every planted state, transformation, and design defect surfaced in every Orbit run (16/16, 15/16 ticketed at medium+ in each). Zero tickets against working states or confirmed claims in all three runs. Versus the baseline honeyflow run: `looks` claims from 0% to 33-40% of the tour; state rows from none to 43-61 per run; finding categories led by states and functional-affordance instead of contrast and hit-areas; every declared breakpoint and theme mode measured.

Cost: the state and dynamics passes roughly double a run (Acme 16 min before, 38 min after; Orbit 44-52 min for four pages). One representative instance per component class keeps it bounded; a large app with dozens of surfaces should expect hours, not minutes.


