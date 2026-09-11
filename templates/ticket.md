---
id: TKT-<nnn>
title: <imperative, one line>
type: functional | visual | ux | a11y | copy | console-error | performance
severity: critical | high | medium | low
gap: model-belief | behavior | unnarrated | design | promise | environment
surface: [<slug>]
sources: [clm-<slug>-<n>]
suspected_source: [<path:line>]
status: open
created_run: run-<YYYYMMDD-HHMM>
file: tickets/TKT-<nnn>-<slug>.md
---

# TKT-<nnn>: <title>

## What the narrator believed
> <claim sentence verbatim> [clm-<slug>-<n>] (confidence: <tag>)
<or: No claim covered this; a person expects: ... [obs-<slug>-<n>]>
<or: <principle line> [dsg-<slug>-<n>]>

## What the browser showed
<observed verbatim>. URL: <url>. Screenshots: <paths>. Console/network: <excerpt or none>.

## Suspected source
- <path:line> - <function, handler, route, or style rule> (code-verified)
- <path> (from tour evidence)

## Proposed fix
<Concrete change in the project's language. For design tickets, the finding's fix verbatim.>

## Repro
```bash
agent-browser --session rc-repro set viewport 1920 1080
agent-browser --session rc-repro open <base url + path>
<the exact commands that reproduce the observation>
```

## Acceptance
```bash
<agent-browser commands>
```
Expected output: <the exact output that must result; for build-or-remove gaps, both accepted outputs joined by OR>

## Agent brief
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

## History
- run-<YYYYMMDD-HHMM> created open: <evidence path>
