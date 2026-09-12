# Verification: <slug>

Run: run-<YYYYMMDD-HHMM> - Base URL: <url> - Session: <name> - Viewport: 1920x1080

## Hidden-control sweep
<"none" or one line per markup-present, snapshot-absent control: obs id, text, selector, finding id>

## Claims
| id | kind | verdict | gap | observed | evidence | reached_via | note |
|---|---|---|---|---|---|---|---|
| clm-<slug>-1 | <kind> | confirmed \| contradicted \| blocked(<reason>) | model-belief \| behavior \| - | <what the browser returned, quoted, <= 25 words> | screenshots/clm-<slug>-1.png; <snapshot line \| get text \| url \| network line \| errors line> | narrated \| bypass | <pointer-click-flaky \| code_peek: path \| -> |

## States
One row per `states.jsonl` row for this surface (component state pass and page dynamics pass).
| id | component | state | trigger | verdict | observed | screenshot |
|---|---|---|---|---|---|---|
| st-<slug>-1 | button.primary | hover | hover "Save" | present \| missing \| broken | <style diff, quoted> | screenshots/<slug>--button--hover.png |

## Expectations
| id | verdict | observed | evidence |
|---|---|---|---|
| exp-<n> | confirmed \| contradicted \| blocked(<reason>) | <quoted> | <screenshot; excerpt> |

## Unnarrated
| id | severity | observed | expected_by_a_human | screenshot |
|---|---|---|---|---|
| obs-<slug>-1 | critical \| high \| medium \| low | <what was seen> | <what a person expects> | screenshots/obs-<slug>-1.png |
