---
name: reality-check
description: Use when someone needs to know whether a web app really works and looks the way its code suggests - checking a product experience end to end, verifying what a demo, how-to, or README would claim against the running UI, auditing functional and design/UX gaps a human would hit, turning those gaps into agent-dispatchable tickets, or re-verifying tickets after fixes. Triggers on "reality-check", "rc", "demo-to-reality", "does this actually work", "does the app do what the code says", "verify the experience", "tour the app", "claim verification", "is this demo safe to record", or the modes :tour, :verify, :tickets, :recheck, :surface, :persona, :viewport, :mobile, :mutate, :auth.
---

# Reality Check

**Mission: measure the gap between what the code leads a first-time user to expect and what a user actually experiences in the browser, then turn every gap into work an agent can finish without asking anyone.**

Three phases, strictly ordered. Phase 1 writes what a demo narrator would say after reading only the code. Phase 2 opens the real app and proves or refutes every sentence, records what a human notices that the narrator never said, and critiques what it sees with measurements. Phase 3 converts every gap into a ticket. The separation is the instrument: if the browser touches phase 1, or the code decides a phase 2 verdict, the measurement is gone.

Design rules:
- **Codebase-agnostic.** Framework, router, styling system, and auth model are discovered, never assumed.
- **Standardized.** Every repo gets the identical `docs/reality-check/` tree, templates, and id scheme.
- **Narrated from the user's side.** The narrator says what a user expects from what is on screen, not what the implementation will do. A button with no handler is claimed as working (`guess`); a link the stylesheet hides is claimed as visible (`guess`). That is how a dead button and a hidden link become measured gaps instead of confirmed facts.
- **Black and white.** `confirmed`, `contradicted`, or `blocked(<reason>)`. No partial verdicts, no "mostly works".
- **Evidence or nothing.** No verdict without a screenshot and a quoted observation. No finding without a measurement, a file, and a check that proves the fix.
- **Both directions of the gap.** What the narrator claimed and the browser refuted, and what the browser showed that the narrator never mentioned.
- **Graded against itself, with floors.** Universal floors (WCAG contrast, 24x24 targets, visible focus, no overflow, no console errors) never adapt. Everything else is graded against the project's own measured norms, never against a default number.

<modes>
| Mode | Behavior |
|------|----------|
| `/reality-check [url]` | Full pipeline: Prepare -> Tour -> Verify -> Tickets -> Report. On a repo that already has `docs/reality-check/`, re-tours fresh and reconciles ids (see `<living-docs>`). |
| `:tour` | Phases 0-1 only. Code reading; no browser, no server, no curl. |
| `:verify [url]` | Phase 2 against the existing tour. Fails fast if `docs/reality-check/tour.md` is absent. |
| `:tickets` | Phase 3 against existing verification, observation, and critique files. |
| `:recheck <TKT-nnn \| clm-... \| --all>` | Re-verify the listed items with their precondition chain and flip ticket status; `--all` replays every claim and reports regressions and fixes separately. |
| `:surface <slug>` | Scope any phase to one surface folder. |
| `:persona <name>` | Narrator profile from `docs/reality-check/personas/<name>.md`, then this skill's `personas/`. Default `howto`. |
| `:viewport WxH[,WxH]` | Phase 2 viewports. Default `1920x1080`. `:mobile` appends `390x844` as a second pass. |
| `:mutate` | Permit destructive triggers (delete, cancel, send, pay). Without it they are `blocked(destructive)`. |
| `:auth <user> <pass>` | Explicit credentials. Env vars `REALITY_CHECK_URL`, `REALITY_CHECK_USER`, `REALITY_CHECK_PASS` are honored. |

Modifiers compose (`:verify :viewport 1440x900 :mutate`). Intake: input is a thought-stream; resolve typos silently; on contradiction the last statement wins; open the reply with one `Heard:` line restating the request and the resolved modes. A `url` argument means the app is already running there; without one, phase 2 starts it per `environment.md`. Nothing is asked before running.
</modes>

<output-contract>
Everything lands in `<cwd>/docs/reality-check/`. Start every file from the matching template in this skill's `templates/`; the templates ARE the standard.

```
docs/reality-check/
  manifest.json            per templates/manifest.schema.json: runs, surfaces, counts, headline numbers
  environment.md           dev command, base URL, auth, seed users; each value tagged evidenced (path) | inferred | given
  rubric.md                floors, README/doc promises as expectations (exp-<n>), project norms measured in phase 2
  tour.md                  the whole narrated tour in scene order; every claim anchored inline as [clm-<slug>-<n>]
  tour.verified.md         phase 2 re-emission with [confirmed] | [contradicted] | [blocked] per line; safe-to-say running time in the header
  results.md                per templates/results.md
  claims.jsonl             per templates/claim.schema.json
  verdicts.jsonl           append-only, one row per claim per run, per templates/verdict.schema.json
  observations.jsonl       unnarrated observations, per templates/observation.schema.json
  findings.jsonl           design findings, per templates/finding.schema.json
  personas/<name>.md       repo-local personas (optional)
  surfaces/<slug>/
    claims.md              phase 1 ledger for this surface
    verification.md        phase 2 verdict rows, expectation rows, unnarrated observations
    critique.md            phase 2 impression paragraph plus measured findings
    screenshots/           <clm-id>.png (interactive claims add --before/--after), <dsg-id>.png, <slug>--overview.png
    console.txt, a11y.json
    history/<run-id>/      previous run's screenshots and per-run files
  tickets/
    index.md               severity then tour order
    tickets.jsonl          per templates/ticket.schema.json
    TKT-<nnn>-<slug>.md    one per ticket, per templates/ticket.md
```

Ids are stable forever, never renumbered; removed items get `status: retired`. `clm-<slug>-<n>` claims, `obs-<slug>-<n>` unnarrated observations, `dsg-<slug>-<n>` design findings, `exp-<n>` expectations, `TKT-<nnn>` tickets, `run-<YYYYMMDD-HHMM>` runs. A surface is a route, screen, modal, or drawer a user lands on; a feature spanning surfaces (session, search, theme) gets its own feature slug. A nav item whose destination has no code still gets a navigation claim on the origin surface; it never gets dropped because the code is missing.
</output-contract>

<phases>
**0. Prepare** (read-only). Detect the dev command and port from the package manifest or framework config (`scripts.dev` or `start`, `next dev`, `vite`, `artisan serve`, `manage.py runserver`, `rails s`, `python3 -m http.server`). Find seed accounts in README, `.env*`, seeders, fixtures, test helpers. Write `environment.md`; when the docs contradict the files (a documented directory or script that does not exist), record both under `Notes` and mark the value `inferred`. Then read `references/critique-rubric.md` "Rubric" and write `rubric.md`: the floors, every checkable promise in README and docs as an `exp-<n>` row with its quote and path, and any design tokens that fix a norm outright. Start nothing, probe nothing: no port check, no binary check, no curl. Those belong to phase 2 setup.

**1. Tour** (code only). Read `references/tour-persona.md` and the active persona. Read the app in the order that file gives, then write `tour.md` as a recordable first-person demo script, surface by surface, and split it into `surfaces/<slug>/claims.md` and `claims.jsonl`. Every sentence asserting something a user sees, or something that happens on an action, is exactly one claim with an inline anchor, a kind, a confidence tag, and code evidence. **No `agent-browser`, no server start, no curl, no reading of prior verdicts in this phase.**

**2. Verify** (browser only). Read `references/verification-protocol.md`, then `agent-browser skills get core`. Preflight the URL; if unreachable, start the dev command; if it cannot start, every claim is `blocked(no-runtime)` and the pipeline continues. Fresh named session, `set viewport 1920 1080` (or the configured viewport) before the first navigation. Walk surfaces in tour order honoring preconditions; run the sequence for each claim's kind; write the verdict row the moment it is decided. When a narrated navigation fails, mark it, navigate directly to the destination, and continue with `reached_via: bypass`. On every surface after its claims: verify applicable `exp-` rows exactly like claims, record unnarrated observations, sample the project's norms, then run the critique sweep from `references/critique-rubric.md` and write `critique.md`. Finish with `tour.verified.md`, then `manifest.json` last. Close only your own session.

**3. Tickets.** Read `references/ticket-rules.md`. One ticket per contradicted claim, per unnarrated observation a user would call a defect, per failed expectation, and per finding at `medium` or above; `low` findings roll into one polish ticket per surface. Phase 3 may open the source files named in the phase 1 evidence to sharpen the root cause; every such sentence is marked `code-verified`. Verdicts are never revisited here. Every ticket ends with a fenced `Agent brief` and an acceptance block written as agent-browser commands with the exact expected output.

**4. Report.** Write `results.md` and print the same block in chat: the functional gap (contradicted functional claims over decidable functional claims, split by confidence tier), findings by severity, unnarrated observation count, the three most consequential gaps in one line each, the safe-to-say running time, and the path to `tickets/index.md`. Update `manifest.json` last.
</phases>

<claims>
| Kind | Functional | The claim says | Verified by |
|---|---|---|---|
| `exists` | no | an element, control, or page is present and visible | `snapshot -i`, `is visible`, screenshot |
| `shows` | no | specific text, values, or records are displayed | `get text`, screenshot |
| `looks` | no | a visual property holds (layout, order, style, state) | screenshot, `get box`, `get styles` |
| `does` | yes | a control produces an observable effect | perform it; URL, snapshot diff, `network requests`, `console`, screenshot after |
| `flows` | yes | an action moves the user from surface A to surface B | perform it, `wait --url` or wait for the landing element, screenshot |
| `state` | yes | something persists or changes across reload, navigation, or session | perform, reload or navigate, re-check, screenshot both |
| `promise` | yes | copy or docs promise a capability ("export anytime", "enable 2FA below") | quote the copy, attempt what it promises, screenshot |

A sentence that is both `exists` and `does` is two claims. Every claim carries: `id`, `surface`, `kind`, `functional`, `claim` (the sentence verbatim), `expected` (one observable), `trigger`, `preconditions`, `evidence` (`path:line`), `confidence`, `destructive`.

Confidence is set in phase 1 and never revised: `sure` (one code location states it plainly), `inferred` (assembled from several locations), `guess` (the persona filled a gap: a control with no handler, a hidden or conditional element, a target that cannot be found). Phase 2 treats all three identically; the manifest reports verdicts per tier so the reader sees how wrong confident code-reading was.
</claims>

<verdicts>
`confirmed`: the browser showed exactly what the claim states. `contradicted`: it did not (absent, hidden, no effect, wrong destination, wrong content, error). A half-true claim is `contradicted`; the row states `matched` and `unmatched`, and the next re-tour splits it. `blocked(<reason>)` with one of `no-runtime`, `credentials`, `needs-data`, `external-service`, `crash`, `destructive`, `precondition:<clm-id>`.

Every contradicted row carries one `gap`: `model-belief` (the code led the narrator to expect something a user cannot see or reach: a hidden control, a missing page, a dead link), `behavior` (present and reachable, but did something else), `environment` never applies to contradicted rows (blocked carries it).

Rules that decide the hard cases:
- Retry once before `contradicted`. Two identical outcomes decide.
- A pointer click (`click`, `find ... click`) that produces no effect while a dispatched `eval "el.click()"` on the same element succeeds is `confirmed` with `note: pointer-click-flaky` and one unnarrated observation; it is never a contradiction and never a blocker.
- A control present in the markup but absent from the interactive snapshot or `is visible` false is a gap the moment it is seen, whatever the claim said: the claim row (if any) is `contradicted / model-belief`, and an `obs-` row plus a `navigation` finding are written in the same step (see `references/verification-protocol.md`). A narrator who correctly predicted the hiding does not make it acceptable.
- A `confirmed` claim whose expected observable is "nothing happens" on an interactive control, or that confirms copy which promises a capability the app lacks, writes an `obs-` row in the same step. Phase 3 tickets it. The narrator being right about a dead button does not make the button less dead.
- Every row cites `url`, `screenshot`, and one of: snapshot excerpt, `get text` result, console or errors excerpt, network excerpt. `confirmed` is never inferred from a similar claim, a static snapshot for a functional kind, or the code. Source may be opened only to locate an element when the snapshot is ambiguous, logged as `code_peek`; a peek never changes a verdict.
</verdicts>

<critique>
Phase 2 deliverable with the same evidence standard as verdicts. Each `critique.md` opens with one `Impression` paragraph (what a person feels in the first five seconds; context, never ticketed on its own), then findings, each with severity, category, `basis` (floor | norm | expectation | human | structure), element, measurement, principle by name, fix as a file-level change in the project's own styling system, and the agent-browser check that proves it. Floors never adapt and any floor breach is at least `medium`. Norms come from the project's own sampled controls: when every sample of a class lies within 2px of the class median, that median is the norm, at any sample count from 2 up, re-evaluated every time a sample is added; a deviation of more than 2px from a norm is `low`; there is no default size threshold and no finding for "under 40px" or "under 44px", and no finding for a 2px difference. Details, categories, and the contrast snippet are in `references/critique-rubric.md`.
</critique>

<living-docs>
- A plain `/reality-check` on a repo with an existing `docs/reality-check/` re-tours fresh (the narrator never opens old verdicts), then reconciles ids by `surface + kind + trigger + expected`: matches keep their id, vanished claims get `status: retired`, new claims take the next `n`.
- `verdicts.jsonl` is append-only with `run_id`; the latest row per claim is current. `:recheck --all` diffs against the previous run and reports `regressions` (confirmed -> contradicted) and `fixes` (contradicted -> confirmed) separately.
- Before a re-verify, move the previous run's screenshots and per-run files to `surfaces/<slug>/history/<run-id>/`.
- Ticket status: `open | fixed | reopened | wontfix | superseded`. `:recheck` flips `open` to `fixed` when every source confirms, and `fixed` to `reopened` on regression. Only a human writes `wontfix`. `superseded` when every source was retired by a re-tour.
- Every mode that writes verdicts, findings, or tickets updates `manifest.json` last; `:recheck` mints its own run id. Human edits to prose sections are preserved.
</living-docs>

<rationalizations>
| Excuse | Reality |
|---|---|
| "I'll open the app to write a better tour" | The tour's value is that it is wrong exactly where the code misleads. A peeked tour measures nothing. |
| "Just a liveness check: is the port free, is agent-browser installed" | Nothing about the runtime is needed to write the tour. Probes belong to phase 2 setup, after `claims.jsonl` exists. |
| "The stylesheet hides it, so I do not claim it" | Claim what the label promises the user, tag `guess`. The hidden link is the gap; a narrator who quietly agrees with the CSS erases it. |
| "There is no handler, so the honest claim is that nothing happens" | Narrate the user's expectation (`guess`). A dead button confirmed as dead still gets an `obs-` row and a ticket. |
| "The snapshot shows the button, so clicking works" | `exists` and `does` are different claims. A button that renders and does nothing is the most common gap. |
| "Four click methods failed, so the link is broken" | If a dispatched click works, the handler works. `confirmed`, `note: pointer-click-flaky`, one observation. Never a blocker from a tool quirk. |
| "Mostly works, I'll mark it confirmed with a note" | A note is invisible to phase 3. `contradicted` with matched and unmatched; split at the next re-tour. |
| "The code clearly handles this, so confirmed" | Code is not evidence in phase 2. Only the browser is. |
| "40px is the rule, so the 39px buttons are findings" | The only rule is the project's own measured norm and the 24x24 floor. A 39px control in a 39px system is Clear. |
| "The layout feels off" | Feels is not a measurement. Get the ratio, the box, the computed style, or put the feeling in the Impression paragraph. |
| "Login failed, so everything else is blocked" | Bypass by direct URL, tag `reached_via: bypass`, keep verifying. Blocked is for the truly unreachable. |
| "Screenshots for every claim is overkill" | The screenshot is what a human uses to trust the verdict. No screenshot, no verdict. |
| "The app will not start, skip phase 2" | `blocked(no-runtime)` on every claim still produces the ticket that unblocks the next run. Finish the pipeline. |
| "I'll batch the rows at the end" | An interrupted session then loses everything. Write each row as it is decided. |
| "This delete is obviously safe" | Destructive is destructive. `blocked(destructive)` unless `:mutate`. |
</rationalizations>

<red-flags>
Stop if you notice: an `agent-browser`, server-start, port-probe, or `curl` command before `claims.jsonl` exists; a verdict row with no screenshot path; a `does`, `flows`, `state`, or `promise` verdict decided from a static snapshot; a `code_peek` that changed a verdict; a markup-present, snapshot-absent control with no `obs-` row; a `confirmed` no-effect claim with no `obs-` row; a contradiction whose only evidence is a failed pointer click; a finding whose fix names no file or whose check is prose; a hit-area finding below no floor and off no measured norm; a ticket without an `Agent brief` or with prose acceptance; a viewport other than the configured one; `agent-browser close --all`; `npx agent-browser`; a re-tour that read `verdicts.jsonl`.
</red-flags>

<quality-bar>
- Narration is concrete and first-person in the persona's voice: "I press Sign in and land on the dashboard, where the greeting reads 'Welcome back, Demo User.'" Never "the user can log in".
- One claim per sentence, one sentence per claim. Long sentences hide claims.
- Verdicts are decided by what the browser returned, quoted.
- Fixes speak the repo's styling language: Tailwind classes in a Tailwind repo, CSS properties in a CSS repo, tokens where tokens exist.
- Tickets are dispatchable verbatim to an agent with no other context.
- Plain imperatives; no em dashes; `-` bullets; no emojis.
</quality-bar>
