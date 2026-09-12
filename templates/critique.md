# Critique: <slug>

Run: run-<YYYYMMDD-HHMM> - Sweep: screenshot --full, a11y, errors, console, vitals[, mobile 390x844]
Summary: <counts by severity> - a11y violations: <n> - console errors on load: <n> - LCP/CLS: <values or n/a>
Norms in force: <class: value (provenance)> | Clear: <categories inspected with no finding>

## Impression
<Three to six sentences: what a person feels in the first five seconds.>

## Design read
<Five to ten sentences with a measurement in each, walking the heuristics table in references/ui-state-model.md section 5: where the eye lands and whether that is the page's purpose; how many primary-styled actions compete; whether related things sit closer than unrelated things; what repeats per item that should appear once; which copy carries identifiers or codes; whether the same control class matches its siblings on this surface and on the entry surface; what the empty, loading, and error states teach. Every sentence that names a problem is also a finding below.>

## State matrix
Built from states.jsonl for this surface. One row per component class; cells read present / missing / broken / n/a.
| component | hover | focus-visible | active | disabled+reason | busy | loading | empty | error | open/expanded | invalid | dark | narrow |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| button.primary | present | present | missing | broken (no reason) | n/a | n/a | n/a | n/a | n/a | n/a | present | present |

## Transformations
| dynamic | result | evidence |
|---|---|---|
| narrow:900 | <overflow / collapse / clipped> | screenshots/<slug>--900.png, scrollWidth |
| dark | <parity / islands / contrast> | screenshots/<slug>--dark.png |
| reduced-motion | <loops stopped / entrances instant> | eval animation-name |
| overlay "<name>" | <trap / escape / return focus> | states rows st-... |
| form "<name>" | <invalid names field / submit guarded / success announced> | states rows st-... |
| keyboard-only | <completed / stuck at ...> | screenshots/<slug>--focus-<n>.png |

### dsg-<slug>-1: <short title>
- severity: critical | high | medium | low
- category: functional-affordance | layout | hierarchy | typography | color-contrast | states | transformation | consistency | navigation | content | hit-areas | accessibility | performance | motion | polish
- basis: floor | norm | expectation | human | structure
- element: <selector> - "<on-screen text>" - source: <path>
- observed: <measurement, quoted from the command output>
- principle: <WCAG criterion or named principle and source>
- fix: <file path> - <property or class change in the project's own styling system>
- check: <agent-browser command(s) and the output that proves the fix>
- screenshot: screenshots/dsg-<slug>-1.png  (an element or region capture in the state that shows the finding)
