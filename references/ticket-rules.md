# Ticket rules (phase 3)

A ticket is a unit of work an agent can finish with no other context. It states what was believed, what was seen, where to look, what to change, and how to prove it. Input: every `verification.md` and `critique.md` under `surfaces/`, plus `observations.jsonl` and `findings.jsonl`. Output: `tickets/TKT-<nnn>-<slug>.md`, `tickets/tickets.jsonl`, `tickets/index.md`.

## What becomes a ticket

- One ticket per `contradicted` claim. Two claims contradicted by the same root observation on different surfaces (the same hidden nav link on two pages) share one ticket listing both ids. A contradicted claim, the `obs-` row, and the `dsg-` finding that all describe the same element share one ticket listing all of them. A `promise` claim and the `exp-` row about the same capability share one ticket.
- One ticket per unnarrated observation a user would call a defect: every `obs-` row written by the hidden-control sweep or the confirmed-no-effect rule, and any other observation at `medium` or above. `low` observations join the surface's polish ticket.
- One ticket per failed `exp-` expectation per surface; an expectation failing on 3+ surfaces is one ticket listing them all.
- One ticket per finding at `medium` or above. Findings with the same root cause (the same rule, component, or markup duplicated across files) share one ticket listing every finding id and every file.
- One polish ticket per surface collecting that surface's `low` findings and observations, titled `Polish: <surface>`.
- `blocked(no-runtime)` across the run: one ticket "Make the app runnable for verification" with the captured stdout. `blocked(credentials)`: one ticket "Provide verification credentials". Other blocked reasons produce no ticket and are listed in `index.md` under "Not verifiable this run".
- `confirmed` claims never produce tickets; their `obs-` rows do.
- Never bundle unrelated contradictions. Traceability beats tidiness.

## Type and severity

`type`: `functional | visual | ux | a11y | copy | console-error | performance`. A ticket with several sources takes the type of its first-listed source. A `promise` claim whose capability is missing is `functional` even when the copy is therefore also wrong. Claims of kind `does`, `flows`, `state` -> `functional`; `promise` -> `functional` when the capability is missing, `copy` when the statement is wrong; `exists` contradicted -> `functional` when the element is a control, `visual` when decorative; `shows` -> `copy`; `looks` -> `visual`. Observations and findings keep the category they were given: navigation, states, functional-affordance -> `ux` or `functional`; contrast, hit-areas, accessibility -> `a11y`.

`severity` (`critical | high | medium | low`), first matching row wins: a contradicted `flows`, `does`, `state`, or `promise` claim with `tier: primary` (the continuous first-run route, including every primary-navigation item) -> `critical`; any other contradicted functional claim, including a dead link, a no-op control, or a hidden control off the primary route -> `high`; contradicted `exists`, `shows`, `looks` -> `medium`; observations and findings keep their own severity, and an observation that discards a record the user created or edited is `critical`, one that reverts a preference or profile field is `high`. Expectations take the rubric row's severity. A ticket with several sources takes the highest severity among them.

`gap`: `model-belief` for hidden, missing, and unreachable elements; `behavior` for present-but-wrong; `unnarrated` for observations; `design` for findings; `promise` for failed expectations; `environment` for blocked clusters. A ticket with several sources takes the gap of its first-listed source; list a contradicted claim first, then observations, expectations, findings.

## Numbering

Read the highest `TKT-<nnn>` in `tickets/tickets.jsonl` and continue; with no file, start at `TKT-001`. Assign numbers in index order: severity (`critical`, `high`, `medium`, `low`), then tour order of the first source. A re-run that finds the same `sources` updates the existing ticket's status and observed fields; it never opens a duplicate.

## Ticket body (templates/ticket.md)

YAML frontmatter with every key in `templates/ticket.schema.json`, then, in order:

1. `What the narrator believed`: the claim sentence verbatim with its id and confidence, or for an observation "No claim covered this; a person expects: ...", or for a finding the principle line.
2. `What the browser showed`: the `observed` text verbatim, the URL, screenshot paths, console or network excerpt.
3. `Suspected source`: the phase 1 evidence paths. Phase 3 may open those files to name the function, handler, route, or style rule; every such sentence ends with `(code-verified)`. Unopened paths stay `(from tour evidence)`. This is the first time source is consulted since phase 1.
4. `Proposed fix`: concrete and minimal, in the repo's own idioms. For a design ticket, the finding's `fix` verbatim.
5. `Repro`: the exact agent-browser commands that reproduce the observation, starting from `set viewport` and `open`.
6. `Acceptance`: a fenced block of agent-browser commands followed by `Expected output:` stating the exact result. Prose is not acceptance. Acceptance asserts the user-visible outcome, never one implementation: when a gap can be closed by building the missing piece or by removing the dead affordance, list both accepted outputs inside the single final item ("`get title` is not `Error response`" OR "`is visible` on the link is `false`").
7. `Agent brief`: a fenced block, dispatchable verbatim:

```
Fix TKT-<nnn>: <title>
Open: <path>, <path>
Observed: <one sentence>
Expected: <one sentence>
Must pass (agent-browser, viewport <WxH>, session of your own):
  1. <step>
  2. <step>
Then run: /reality-check:recheck TKT-<nnn>
Do not touch: <files or behaviors the fix must leave alone, when known>
```

8. `History`: one line per status change, `<run-id> <from> -> <to>: <evidence path>`.

Paths in `tickets.jsonl` (`file`, `screenshot`) are relative to `docs/reality-check/`.

## index.md

One table ordered by severity then tour order, columns `id | severity | type | gap | surface | title | status | sources`, then a "Not verifiable this run" list.

## Lifecycle

`status: open | fixed | reopened | wontfix | superseded`.

- Created `open`.
- `:recheck`: when every source claim is `confirmed` (and, for a hidden-control or no-effect observation, the acceptance commands produce the expected output), every source finding `check` passes, and every source expectation confirms -> `fixed`, with `fixed_run` set; a source class the ticket does not have is trivially satisfied. A `fixed` ticket whose source regresses -> `reopened`.
- Only a human writes `wontfix`, with a `wontfix_reason`.
- `superseded` when every source was retired by a re-tour; superseded tickets stay in `index.md` at the bottom.
- Every status change appends a History line.

## Never

- A ticket whose acceptance is "works correctly" or "looks better".
- A ticket for a confirmed claim (ticket its `obs-` row instead), or for a blocked claim other than no-runtime and credentials.
- A ticket from a contradiction whose only evidence is a failed pointer click.
