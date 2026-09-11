# Planted answer key (never shown to the agent under test)

Fixture: `site/` (Ledgerlite). Serve with `cd site && python3 -m http.server 4173`. Account documented in `site/README.md`.

| # | Planted defect | Where | Expected reality-check outcome |
|---|---|---|---|
| 1 | Export CSV button fetches `/api/export.csv` which does not exist; the error is swallowed, nothing visible happens | `js/app.js` export handler, `dashboard.html#export-btn` | interaction claim `not-confirmed / failed` (no download, no status text; console shows 404); ticket type functional, gap behavior |
| 2 | Nav link "Reports" points to `reports.html`, which does not exist (404 page from http.server) | `dashboard.html` and `settings.html` nav | navigation claim `not-confirmed / failed` (or not-found for the Reports surface render claim); ticket type functional, blocker or major |
| 3 | "Create account" link exists in the markup but `.register-link { display: none }` hides it | `index.html`, `css/app.css` | render claim `not-confirmed / not-found`, tagged `gap: model-belief`; ticket gap model-belief |
| 4 | "Last synced" caption color #b5b5b5 on #ffffff (about 2.0:1) | `css/app.css .last-synced` | design finding lens contrast, severity minor or major, measured ratio under 4.5:1; check via a11y color-contrast |
| 5 | Refresh icon button is 20x20px | `css/app.css .icon-btn`, `dashboard.html#refresh-btn` | design finding lens hit-areas, measured 20x20, After names .icon-btn and 40x40 |
| 6 | Security panel hint says "you can enable two-factor authentication below" but no control exists | `settings.html` Security panel | promise claim `not-confirmed / failed` (copy present, capability absent); ticket type functional or copy |

Adaptive rubric (added 2026-09-11): the site's own control norm is 39px (`.btn` padding 10px + 15px text), so the 39px buttons must NOT be findings; the 20px icon button stays a finding with `basis: floor` (WCAG 2.5.8, 24x24); the caption contrast stays a finding with `basis: floor`. README promises: "Every table can be exported as CSV" must appear as an `exp-` row and be `not-confirmed` on the dashboard (defect 1); "targets WCAG AA contrast" must appear as an `exp-` row and be `not-confirmed` on the dashboard (defect 4). `rubric.md` must exist with a provenance on every lens row and at least one `measured` row.

Routing (added 2026-09-11): an all-`here` run creates no `docs/reality-check/.handoff/`. A routed run (`:parallel` or `:route <phase>=handoff` + `:merge`) must leave `.handoff/<run-id>/<phase>/` with `tasks.jsonl` passing the Cursor `ownership.sh` check, one `units/<srf>/prompt.md` per non-entry surface, `done.json` per unit whose counts match its part files, `merge.json` with every unit `valid`, and `manifest.json` recording `route`, `units[]` with executors, and `verified_by`/`narrated_by` per surface. Grade with `python3 grade.py <docs> --routed`. The verdict set per claim must equal the sequential run's.

Working paths that must be `confirmed`: login with the documented account lands on dashboard.html (auth-gate / navigation); wrong password shows "Email or password is incorrect." (feedback); dashboard renders three cards with the quoted amounts (render / data); Save display name shows "Saved" and the greeting updates (interaction / feedback); theme toggle persists across reload (state); Log out returns to index.html (navigation); opening dashboard.html without a session redirects to index.html (auth-gate).

Pass bar for the skill build: at least 5 of 6 planted defects surface as tickets; defect 3 yields `not-found` with `gap: model-belief`; defect 6 yields a failed `promise` claim; the working paths above are confirmed; every ticket has all fields and an Agent brief; after fixing defect 3 (remove the `display: none` rule) `:recheck` flips its ticket to `fixed`.
