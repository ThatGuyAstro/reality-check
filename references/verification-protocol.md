# Verification protocol (phase 2)

Phase 2 is a human-experience instrument. The browser decides every verdict; you record. Code is never consulted to decide, and a failure is never explained here.

## Setup

```bash
agent-browser skills get core                 # version-matched command guidance; read before the first command
RUN=run-$(date -u +%Y%m%d-%H%M)
S="agent-browser --session rc-<app-slug>"     # a caller-supplied session name overrides this
OUT=docs/reality-check
$S set viewport 1920 1080                     # before the first navigation, always (or each configured viewport in turn)
$S open "$BASE_URL"
$S wait --load networkidle
```

- Read `rubric.md` before the first browser command; if absent, write it from phase 0's rules first.
- Always the direct `agent-browser` binary, never `npx agent-browser`.
- Fresh profile: a new named session has no cookies or storage. Never load a saved state at the start of a run.
- Preflight: if the base URL is unreachable, start the dev command from `environment.md` in the background, poll with `curl -s -o /dev/null -w '%{http_code}'` every 3 s for up to 90 s, record the pid. Still down: every claim is `blocked(no-runtime)` with the startup output in `environment.md`; continue to phase 3.
- Prior run present: move `surfaces/*/screenshots/*`, `verification.md`, and `critique.md` to `surfaces/<slug>/history/<previous-run-id>/` first.
- Credentials ladder: seed account from `environment.md` (evidenced), then `REALITY_CHECK_USER`/`REALITY_CHECK_PASS`, then `:auth`. None: every claim with an auth precondition is `blocked(credentials)`; public surfaces are still verified. After a successful login, `$S state save $OUT/.auth-state.json` for `:recheck`; never commit it.
- Refs (`@eN`) go stale on every navigation, submit, modal, or re-render. Re-snapshot before every interaction. `is visible`, `get styles`, `get box` take a CSS selector or a ref, not a role/text string; a role/text string silently returns false.

## Walk order

Surfaces in tour order; within a surface, claims in id order. Before each claim check its `preconditions`: if one is `contradicted`, the claim is `blocked(precondition:<clm-id>)` unless the surface is reachable by direct URL, in which case navigate there, set `reached_via: bypass`, and verify normally. Only a surface unreachable by any means blocks its claims.

On arrival at a surface, before any claim:

```bash
$S wait --load networkidle
$S screenshot $OUT/surfaces/$SLUG/screenshots/$SLUG--overview.png
$S snapshot -i > /tmp/rc-snap-$SLUG.txt
$S errors  >  $OUT/surfaces/$SLUG/console.txt
$S console >> $OUT/surfaces/$SLUG/console.txt
$S a11y --json > $OUT/surfaces/$SLUG/a11y.json      # violations at .data.violations[]; failureSummary carries the measured value
```

Then the hidden-control sweep, before the claims: compare `$S get html nav` (and the header, footer, and main action regions) against the interactive snapshot. Every link or button present in the markup but absent from the snapshot, or `is visible` false, is written immediately as an `obs-<slug>-<n>` row ("in markup, not visible: <text>, <selector>") and a `navigation` finding (severity `medium`, or `high` when the tour names it as a primary path item), unless the tour names the user-visible condition that reveals it. When a claim covers the element, its verdict is `contradicted / gap: model-belief` when it is reached, whatever the narrator predicted. This sweep is not optional and not deferred to the critique.

## Component state pass (every surface, after the hidden-control sweep, before or between the claims)

Read `surfaces/<slug>/components.md`. For every component class listed, drive each state in its row of `references/ui-state-model.md` section 2 on one representative instance (the first primary one; a second instance when the first is disabled), and for each state write one row to `states.jsonl` (`templates/state.schema.json`) and one element screenshot `surfaces/<slug>/screenshots/<slug>--<component>--<state>.png` taken while the state holds:

```bash
# style probe: nine properties, one line of JSON (`get styles` dumps every computed property and takes no property list)
PROBE='(s=>{const c=getComputedStyle(s);return JSON.stringify({bg:c.backgroundColor,color:c.color,border:c.borderColor,shadow:c.boxShadow,outline:c.outlineStyle+" "+c.outlineWidth,transform:c.transform,opacity:c.opacity,cursor:c.cursor,anim:c.animationName})})(document.querySelector("<sel>"))'
$S eval "$PROBE"                                            # rest baseline
$S hover "<sel>"; $S wait 250; $S eval "$PROBE"; $S screenshot "<sel>" $OUT/surfaces/$SLUG/screenshots/$SLUG--button--hover.png
$S press Tab   # repeat until eval "document.activeElement.matches('<sel>')" is true; then $PROBE + screenshot as --focus-visible
$S mouse move <cx> <cy>; $S mouse down; $S eval "$PROBE"; $S screenshot "<sel>" ...--active.png; $S mouse up
```

Rules for the pass:
- A state row's `verdict` is `present` when the computed style or the DOM differs from rest in the way the class expects (hover changes colour, background, border, shadow, or lifts at most 2px; focus-visible shows a ring; active scales or darkens; disabled dims and exposes a reason; busy shows an indicator), `missing` when nothing differs, `broken` when the state is present but wrong (hover moves layout, focus ring invisible, disabled with no reason, a skeleton that never resolves). `missing` and `broken` each write an `obs-` row with `source: state-gap` and `severity` from the class row, and the critique files the finding.
- Data states are reached honestly first (a filter with no matches, a fresh record, a long list). When the app cannot be put into a state without server data, synthesize it: `$S network route "<data url>" --body '[]'` for empty, `--abort` for error, `$S set offline on` for offline, `--body` with a large payload for overflow; screenshot; then `network unroute` and `set offline off`. A synthesized state is recorded with `synthesized: true` and the mock named; it is still evidence that the component has or lacks the state.
- Loading: `$S network route "<data url>" --body '<real body>'` cannot delay, so capture loading by screenshotting within the first 300 ms of `open` or `reload` (`$S open <url>; $S screenshot ...--loading.png` before `wait --load networkidle`), or by `set offline on` before the navigation to hold the skeleton. Record whether the skeleton mirrors the final layout (`get box` on skeleton blocks vs the loaded content).
- Overlays: for every dialog, menu, drawer, popover on the surface, run the lifecycle from `references/ui-state-model.md` section 3 (open, focus inside, Tab past the end, Escape, scrim click, focus back on the trigger, body scroll locked) and write one `states.jsonl` row per step.
- Forms: run the full lifecycle (empty submit, invalid input, correction, submitting, success, server error via `network route --abort`, dirty-state guard) and write one row per step.
- Never skip a class because it "obviously works". The pass is the measurement; its rows are what the state matrix in `critique.md` is built from.

## Page dynamics pass (every primary surface, after its claims)

1. Breakpoints: for every band in `rubric.md` `breakpoints` (fallback: 1280, 1024, 768, 390), `$S set viewport <w> 900`, `reload`, `wait --load networkidle`, `screenshot --full ...--<w>.png`, `eval document.documentElement.scrollWidth`, `snapshot -i` diffed against the desktop snapshot (which controls vanished, which appeared), `get box` on the primary navigation and the main column. One `states.jsonl` row per band with `component: page`, `state: narrow:<w>`. Then restore the configured viewport and reload.
2. Theme modes: for every mode the app declares (`rubric.md` `modes`; fallback: light and dark when `.dark`, `[data-theme]`, or `prefers-color-scheme` appears in the stylesheet), switch with the app's own control when one exists, else `$S set media dark`, then `screenshot --full`, `a11y --json` again, the contrast snippet on the same elements measured in light, and `get styles` on cards, inputs, and the primary button. One row per mode; every light finding is re-measured in dark.
3. Reduced motion: `$S set media reduced-motion`, reload, `eval` the computed `animation-name` and `transition-duration` on every element that animated in the normal pass; screenshot. One row.
4. Navigation: click each primary nav item and `back`; `eval performance.timeOrigin` before and after when the app promises soft navigation; deep-link the surface's detail URL in a fresh tab; `reload` on a stateful view. One row per check.
5. Scroll: `scroll down 100000`, screenshot, `get box` on sticky chrome and the first and last rows; then, from the bottom, follow every in-page anchor link the navigation offers (`href="#..."`) and compare `get box` top of the target against the bottom of the sticky chrome (a target under the chrome is `broken`); scroll inside every inner scroll region with `scroll down 2000 --selector "<region>"`; `eval window.scrollY` after a wheel over the region to detect a trap. One row per check.
6. Keyboard-only: complete the surface's primary claims with Tab, Enter, Space, arrows, Escape and no pointer; screenshot the focused element at every stop where the ring is faint. One row; a stop with no visible ring is a `broken` state on that component.
7. Time: for every toast or auto-dismissing message seen, record appearance time, dismissal time, and whether hover pauses it. For every poll or refresh, whether focus and scroll survive it.

Restore the viewport, media, offline, and routes before the next surface. Rows from this pass carry `component: page`. Feature surfaces (session, search, theme) get no state pass and no dynamics pass of their own: their behaviour is exercised as claims on the page surfaces, and their `verification.md` says `states: n/a - exercised on <slugs>`. The same holds for a destination that never rendered (a 404): `components.md` reads `n/a - destination did not render`, and it has no `states.jsonl` rows.

## Sequences by kind

Every sequence ends with a screenshot taken after the observation, saved as `surfaces/<slug>/screenshots/<clm-id>.png`; interactive kinds add `<clm-id>--before.png`. Meet preconditions first and record them in the row.

- `exists`: `$S snapshot -i`; locate by role, label, or text; `$S is visible <selector or ref>` must be true; screenshot. Absent after `wait <selector>` up to 5 s, or present in `get html` but not visible: `contradicted / model-belief`, observed "present in DOM, not visible" or "not found".
- `shows`: `$S get text <selector>` (for a form field, `$S get value <selector>` or `$S eval "document.querySelector('<selector>').value"`; inputs carry no text node); compare to `expected` in substance (not whitespace or case); screenshot. Different: `contradicted / behavior` with both strings in the row.
- `looks`: put the component into the claimed state first (the `component state pass` row for it, or the claim's own `trigger`), then screenshot the element in that state; `$S get styles <selector>` or `$S get box <selector>` for the stated property; keep the measured values and the rest-state values in the row. A `looks` claim about a state is `contradicted / behavior` when the state does not appear or appears differently, `contradicted / model-belief` when the component itself is absent.
- `does`: `$S snapshot -i` to a scratch file; `$S get url`; `$S network requests --clear`; perform the trigger (`click @ref`, `fill`, `select`, `press`); `$S wait --load networkidle` or `wait <ms>` for pure client effects; `$S get url`; `$S snapshot -i` to a second scratch file and diff the two; `$S network requests`; `$S errors`; `$S console`; screenshot. `confirmed` only when the effect the claim names is observed (new element, new URL, new text, request sent, download started, toast shown). No observable change at all: `contradicted / behavior`, observed "no-op: url unchanged, snapshot diff empty, no requests, console empty", quoting the network status when a request fired and failed. Swallowed fetch failures leave console empty; `network requests` still shows the status code, so always quote it.
- `flows`: `$S snapshot -i`; `click @ref`; `$S wait --url "**/<expected-path>*"` up to 10 s or wait for the landing element; `$S get url`; `$S get title`; screenshot. Lands elsewhere, times out, or shows an error document ("Error response", "404", "Not Found") with none of the app's chrome: `contradicted` (`model-belief` when the destination does not exist, `behavior` otherwise). A URL match alone never confirms a navigation.
- `state`: perform the trigger, then `$S reload` (or navigate away and back) and re-check with `get text`, `eval`, or `is visible`; screenshot both states.
- `promise`: `get text` to confirm the copy is present, then attempt what it promises with the `does`/`flows` sequence; screenshot the outcome. Copy present but capability absent: `contradicted / behavior`.

Retry once before `contradicted`: re-snapshot, wait 2 s, repeat the sequence. Two identical outcomes decide.

Pointer-click rule: when a `does` or `flows` trigger via `click @ref` and `find role <role> click --name "<text>"` produces no effect twice, run `$S eval "document.querySelector('<selector>').click()"` once. If the effect then appears, the verdict is `confirmed` with `note: pointer-click-flaky` and one `obs-` row (severity `low`) recording the pointer failure. If the dispatched click also produces nothing, the verdict is `contradicted`. A tool quirk is never a blocker ticket. This rule applies only to elements that are visible in the interactive snapshot; an element the hidden-control sweep marked not visible stays `contradicted / model-belief` even if a dispatched click on it would navigate.

Confirmed no-effect rule: when a `does` claim's `expected` is that nothing happens, or a `shows` claim confirms copy that promises a capability, write the verdict `confirmed` and, in the same step, an `obs-` row (severity `high` for a primary action, `medium` otherwise) stating what a user would expect. Phase 3 tickets the observation.

Mutations: create and edit freely; name created records in the row. Destructive triggers are `blocked(destructive)` unless `:mutate`.

Code access: the verifier may open a source file only to locate an element or route when the snapshot is ambiguous, logged in the row as `code_peek: <path>`. A peek never changes a verdict.

## Finding evidence

A finding's screenshot shows the finding. Capture the element (`$S screenshot "<sel>" <path>`) or the region around it, in the state that exhibits the problem (the hover state for a hover-only affordance, the dark mode for a dark-mode gap, the narrow band for an overflow, the invalid state for an unlabelled error). Reusing a page or claim screenshot that does not show the measured thing is a red flag. When the problem is only visible with context (alignment, grouping, repetition), use `screenshot --full` and name the region in `element`.

## Writing rows

Write each row to `surfaces/<slug>/verification.md` and append one line to `verdicts.jsonl` the moment the verdict is decided. Never batch. Row columns: `id | kind | verdict | gap | observed | evidence | reached_via | note`. `observed` is what the browser returned, quoted, at most 25 words; `evidence` is the screenshot path plus one of a snapshot line, a `get text` result, a URL, a network line, or a console line.

## After the claims of a surface

Ordering: when a surface's last claim is the action that leaves it (a login, a navigation, a sign-out), do the four steps below before performing that claim, so the surface is still open; then perform the leaving claim last. If a claim mid-surface leaves it, return by direct URL (`reached_via: bypass` is not needed for returning) and continue.

1. Expectations: verify every `rubric.md` `exp-` row whose `applies_to` matches this surface exactly like a claim; append a verdict row with `claim: exp-<n>` and `surface`, under `## Expectations` in `verification.md`.
2. Unnarrated observations: look at the surface as a person who never read the code, with the heuristics table in `references/ui-state-model.md` section 5 open: dead ends, controls with no visible effect that no claim covered, missing feedback after an action, confusing labels, raw identifiers or codes in copy, repeated chrome per item, groups without boundaries, competing focal points, surfaces reachable from here that the tour never mentioned. Each becomes `obs-<slug>-<n>` with `observed`, `expected_by_a_human`, `screenshot` (showing the thing), `severity`, `source` (`human-eye`, `state-gap`, `transformation`, `hidden-control`, `confirmed-no-effect`, `pointer-click-flaky`), `gap: unnarrated`, under `## Unnarrated` in `verification.md` and in `observations.jsonl`.
3. Norm sampling: `get box` every button and every nav link on the surface, `get styles` body text; append to `rubric.md` "Samples"; when every sample of a class lies within 2px of the class median, that median is the class's norm with provenance `measured (<surfaces>, n=<count>)`; the check is repeated every time a sample is added, and a norm whose samples no longer agree is withdrawn. Norms are read by the critique sweep; a norm landing or withdrawn after an earlier surface was critiqued re-evaluates that surface's findings on that lens (findings now within the norm, or resting on a withdrawn norm, get `status: retired`).
4. Critique sweep per `references/critique-rubric.md`, with the `states.jsonl` rows for this surface as its input; write `critique.md` (design read, state matrix, transformation results, findings) and `findings.jsonl`.

## tour.verified.md

After the last surface, copy `tour.md` to `tour.verified.md` and append to every anchored sentence its mark: `[confirmed]`, `[contradicted]`, or `[blocked]`. In the header, state the safe-to-say running time: 4 seconds per confirmed claim sentence plus 3 seconds per `[cue]` whose next claim is confirmed.

## :recheck

`:recheck <ids | --all>`: resolve ticket ids to their source claim, observation, expectation, or finding ids. Mint a new run id. Move only the touched ids' screenshots to `surfaces/<slug>/history/<previous-run-id>/` (the whole-surface move in Setup applies to `:verify` and the full pipeline, never to `:recheck`). For each claim, verify its precondition chain first (loading `.auth-state.json` when valid), then the claim, appending a new verdict row and rewriting that claim's row in `verification.md` in place with a `recheck: <run-id>` note. For an observation, re-run the check its ticket's acceptance block states and set its `status` in `observations.jsonl` to `resolved` on pass. For a finding, run its `check` command and set its `status` in `findings.jsonl` to `fixed` on pass or `regressed` when a previously fixed finding fails again. Then update ticket status per `references/ticket-rules.md`. `--all` replays every non-retired claim in tour order and lists `regressions` and `fixes` separately in `results.md`.

## Teardown

`$S close` for your own session only. Stop the dev server only if you started it. Never `close --all`.
