# GREEN test of the merged skill (2026-09-11)

This is the internal evaluation log from the day this skill was built. It records a real
before/after comparison: two earlier, independently-built skills ("rc" and "d2r" below) were
each run cold against two planted-bug fixtures, graded by reading the output artifacts on disk
(never by trusting the agent's own report), and their failures became the pass bar for this
merged skill. The raw per-cell grade files this table summarizes aren't included in this repo
(they belonged to the throwaway comparison workspace); what's reproducible here is the fixtures,
the grader, and the runs described below. Failures the merged skill had to close:

| # | Baseline failure | Cell | Merged-skill rule that targets it |
|---|---|---|---|
| F1 | Hidden Create account link recorded in a confirmed row, never filed | d2r on Ledgerlite (L3) | hidden-control sweep before a surface's claims writes `obs-` + finding; claim is `contradicted / model-belief`; narrator claims hidden controls as visible (`guess`) |
| F2 | Export CSV narrated as "does nothing", confirmed, never ticketed | rc on Acme (R2) | user's-side rule (`guess`, expects a download) + confirmed-no-effect rule writes `obs-` |
| F3 | Settings link, Sign out, Save filed as blockers after pointer-click failures | rc on Acme (R4, A11) | pointer-click rule: dispatched click works -> `confirmed`, `note: pointer-click-flaky`, one low observation |
| F4 | 37-39px buttons ticketed against a 40px default | rc on Acme (TKT-009) | no default size threshold; norms from unanimous samples at any count; findings only at floor or norm deviation |
| F5 | curl status check before the tour | rc on Ledgerlite (L11) | phase 0 "Start nothing, probe nothing"; rationalization row; red flag names port probes |

Pass bar: on both fixtures every planted defect ticketed, every working path confirmed and unticketed, F1-F5 closed, cited screenshots on disk, acceptance blocks fenced. Grader: `python3 grade.py <docs/reality-check dir> --fixture ledgerlite|acme` plus a human read of the artifacts.

Each run below was a fresh, cold execution of a pinned snapshot of the skill text against a disposable copy of one fixture served on its own local port, run by an agent with no access to the answer key.

## Results, GREEN-1 (snapshot as first written)

| Cell | grade.py | F1 hidden control | F2 dead control | F3 click flake | F4 default norm | F5 probe before tour | Working paths | False-positive tickets | Wall time | Tool calls |
|---|---|---|---|---|---|---|---|---|---|---|
| v2 on Acme | 20/21 | closed: obs-dashboard-1, obs-settings-1, dsg-dashboard-1, TKT-004 | closed: clm-dashboard-8 (promise, guess) contradicted, TKT-002 | no flake occurred; Settings/Sign out/Save confirmed | residual: dsg-dashboard-3 (39px vs 37px "norm" from 2 of 3 samples, low, in polish rollup) | closed: tour at 14, first probe at 17 | all confirmed, none ticketed | 0 (1 debatable low finding) | 17m | 109 |
| v2 on Ledgerlite | 24/24 | closed: clm-login-8 contradicted/model-belief, obs-login-1, dsg-login-1, TKT-004 | closed: clm-dashboard-12 contradicted, TKT-002 | none occurred | closed: no .btn finding, norm measured 39px | closed: tour at 19, first probe at 27 | all confirmed, none ticketed | 0 (TKT-008 13x13 native checkbox is debatable: the wrapping label is the target) | 21m | 111 |

Versus the parents on the same fixtures: demo-to-reality 22/23 with one miss (F1); reality-check v1 19/23 with three misses (F2, F3 twice) and 6 false tickets. Merged: 44/45 on the new grader, both parents' misses closed, 0 false tickets.

Text fixes applied after GREEN-1 (each traced to a runner-cited ambiguity): norm = median with every sample within 2px, re-evaluated per sample, deviation > 2px only; mobile pass as a clean conditional; `basis: structure`; gap of a multi-source ticket; unrendered destination critique; cue placement; claim+obs+finding and claim+expectation share one ticket; nav item with no destination keeps primary tier as its own scene; scenes in reach order; environment startup log in phase 0 when a URL is given; native checkbox measured by its label; `report.md` renamed `results.md` (subagent harnesses block writes to that name).

## Results, GREEN-2 (edited snapshot)

| Cell | grade.py | Notable | False-positive tickets | Wall time | Tool calls |
|---|---|---|---|---|---|
| v2 on Acme (v2b__acme) | 22/22 | The pointer-click flake occurred live (Settings, Save, Sign out): all three verdicted `confirmed` with `note: pointer-click-flaky` and low observations, no blocker tickets (F3 closed under fire). Unplanted real defect found: saved display name discarded on re-login (auth.js:10 hardcodes the name), TKT-004 high. No norm finding on the 37-39px buttons (F4 closed). | 0 | 16m | 97 |
| v2 on Ledgerlite (v2b__ledgerlite) | 24/24 (after a grader keyword fix) | All six plants ticketed; Create account hidden link is TKT-003 with claim + obs + finding merged; 39px .btn norm measured, no finding. Debatable: TKT-005 (Sync now tooltip promises bank sync, no request observed) and TKT-010 (theme switch label under 24px). | 0 | 23m | 132 |

Both parents' baseline misses stay closed on the edited text. Wording fixes applied after GREEN-2 (all from runner-cited ambiguities): severity precedence (primary tier -> critical first), hidden-control finding exempt from the "already contradicted" rule, data-loss definition, `get value` for inputs, focus measured only by a Tab walk, `feature` claim tier, highest severity for multi-source tickets, post-claim work before the surface-leaving claim, contradictory README recorded as inferred.

## Results, GREEN-3 (final text) and :recheck micro-test

| Cell | grade.py | Notable | False-positive tickets | Wall time | Tool calls |
|---|---|---|---|---|---|
| v2 on Ledgerlite (v2c__ledgerlite) | 24/24 | 38 claims, sure 29/29 confirmed, guess 0/6 confirmed. All six plants ticketed (3 critical: Export, Reports, 2FA on the primary route). Runner self-corrected a claim-tier slip against the text. | 0 | 23m | 129 |
| :recheck TKT-003 on v2b__ledgerlite after removing `.register-link { display: none; }` | pass | new run id, one verdict row appended, obs and finding statuses flipped, TKT-003 `open -> fixed` with fixed_run and a History line, tickets.jsonl / index.md / manifest.json updated, TKT-004 (missing register page) untouched and still 404. | - | 5m | 46 |

Clarifications applied after GREEN-3 (wording only, from runner-cited ambiguities; not re-run): :recheck scope of the history move and where obs/finding pass-fail is recorded; ticket `type` tie-break; promise-with-missing-capability is functional; hidden-control rule outranks the pointer-click rule; revisited surfaces get `(continued)` scenes; switch label gets the spacing exception.

## Totals across the merged skill's five executions
5 runs (3 Ledgerlite full, 2 Acme full) + 1 recheck: every planted defect ticketed in every run (11/11 plants x runs), 0 tickets sourced from a confirmed claim, 0 blocker tickets from click flakes (3 flakes occurred and were absorbed), tour-before-browser held in 5/5, viewport-before-open held in 5/5.



