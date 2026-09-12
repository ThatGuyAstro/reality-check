# Reality Check results: <app name>

Run: run-<YYYYMMDD-HHMM> | Persona: <persona> | Viewport(s): <list> | Base URL: <url>

**Functional gap: <contradicted functional> / <decidable functional> (<pct>%)** - by confidence: sure <a>/<b>, inferred <c>/<d>, guess <e>/<f>
**Design findings:** critical <n>, high <n>, medium <n>, low <n>
State coverage: <components> components, <states> states exercised, <missing> missing, <broken> broken, <synthesized> synthesized | Transformations: breakpoints <n>/<declared>, modes <n>/<declared>, reduced-motion <yes/no>
Unnarrated observations: <n> | Non-functional verdicts: exists <c>/<t>, shows <c>/<t>, looks <c>/<t> | Expectations: <c>/<t> confirmed | Blocked: <n> (<reasons>)

Most consequential gaps:
1. <TKT-nnn> <one line>
2. <TKT-nnn> <one line>
3. <TKT-nnn> <one line>

Cross-surface consistency (written once, from every surface's state matrix and findings):
- <the same control class measured on N surfaces: values, and the surfaces that deviate>
- <the same state missing on N surfaces (e.g. no focus-visible on any icon button)>
- <copy patterns repeated across surfaces (raw ids, codes, duplicated chrome)>

Safe-to-say running time: <m>m<s>s of <m>m<s>s narrated.
Tickets: <n> open -> `docs/reality-check/tickets/index.md`
<:recheck --all only: Regressions: <ids> | Fixes: <ids>>
