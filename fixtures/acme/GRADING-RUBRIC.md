# Grading rubric - planted-app (pre-committed 2026-09-11 before any run completed)

Grade only by reading the run's output files and checking the artifacts they cite exist on disk. Same rubric for RED and GREEN. One point each, 13 max (R1-R10 original; R11-R13 added 2026-09-11 after the board ratification, before GREEN-3 ran).

| # | Check | Evidence to look for |
|---|---|---|
| R1 | P1 registration link flagged as failing/missing | a verdict, finding, or ticket naming the register link / 404 |
| R2 | P2 Export CSV flagged as doing nothing | a verdict/finding/ticket naming Export CSV |
| R3 | P3 Reports nav flagged as hidden/absent | a verdict/finding/ticket naming Reports nav |
| R4 | P4 Save flagged as WORKING (not filed as bug) | a confirmed/pass verdict for settings save; no ticket about it |
| R5 | P5 contrast flagged in a design/UX critique | a finding naming the hint/helper text contrast |
| R6 | P5 fix is actionable: names `css/app.css` and the `.hint` color property | text of the finding or ticket |
| R7 | Interactive verdicts cite screenshots that exist on disk | pick every CONFIRMED/CONTRADICTED interactive claim; `ls` each cited screenshot |
| R8 | Tickets exist, one per real defect, each with an acceptance check phrased as browser steps/commands | tickets dir |
| R9 | Phase 1 (tour) produced before any browser command; browser not used to write the tour | agent's own instrumentation report ordering + tour file has code-evidence pointers |
| R10 | Viewport set to 1920x1080 before first navigation | instrumentation report / command log |
| R11 | P6 README promise appears as an `E-` expectation row and is CONTRADICTED on the dashboard with a ticket quoting the README | expectations.md, dashboard verification.md, tickets |
| R12 | P3 (hidden Reports) is filed as an F- or U- id in the SAME step as its verdict and ticketed, regardless of verdict | dashboard verification.md row for Reports has an F-/U- id beside it; tickets |
| R13 | After the fixture is patched (Reports link un-hidden, `.hint` color fixed), `:recheck --all` flips those tickets to `fixed`, reports them as fixes, and reports zero regressions | tickets.jsonl status, manifest run entry, agent report |
