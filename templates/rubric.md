# Rubric: <app name>

Run: run-<YYYYMMDD-HHMM> | Written by phase 0 from the code; norms added by phase 2 sampling
Sources read: <path>, <path> | Human rows preserved: <n>

## Floors (never adapt)
| floor | standard | severity |
|---|---|---|
| contrast 4.5:1 body, 3:1 large and UI | WCAG 1.4.3, 1.4.11 | medium (high on primary text or action) |
| target >= 24x24 | WCAG 2.5.8 | medium (high on primary action) |
| focus visible | WCAG 2.4.7 | medium |
| no horizontal overflow at the configured viewport | layout | high |
| no console error or failed request on load | runtime | medium |
| no axe serious or critical | axe-core | medium |

## Norms
| class | value | provenance | samples |
|---|---|---|---|
| buttons | <h>px | evidenced (<path:line>) \| measured (<surfaces>, n=<count>) \| none | <values> |
| nav-links | <h>px | ... | ... |
| body-text | <size>px / <line-height> | ... | ... |
| sibling-gap | <n>px | ... | ... |

## Expectations
| id | statement | applies_to | check | severity | provenance |
|---|---|---|---|---|---|
| exp-1 | "<quoted statement>" | all \| <surface pattern> | <intent-level steps> | high | evidenced (<path:line>) |

## Samples (phase 2 appends)
<class>: <surface> <element> <value>
