# Critique rubric (phase 2, per surface)

A finding without a measurement is an opinion. A finding without a file and a property is a complaint. A finding without a check is a wish. Every finding has all three.

The critique is a design review, not an audit printout. It answers, in this order: does the page read (hierarchy, grouping, rhythm, signifiers, copy); is every component complete in its states and does each state do its job; does the page hold together when it transforms (bands, modes, motion, overlays, forms, keyboard); and only then, which floors are breached. Contrast ratios and target sizes are floors, they are measured on every surface, and they are reported as systemic clusters so they never crowd out the design read. `references/ui-state-model.md` is the vocabulary; its section 5 table supplies the principle name and the evidence for every finding here.

## Rubric (`docs/reality-check/rubric.md`)

Phase 0 writes it from the code; phase 2 adds measured norms. Precedence for any threshold: a `human` row a person edited (preserved verbatim on regeneration), then `evidenced (path)` from design tokens, theme config, or docs, then `measured` from phase 2 sampling, then the floor. There is no default size or spacing threshold: a lens with no human, evidenced, or measured value and no floor breach is `Clear`. Findings from the hidden-control sweep and other structural rules (a control in the markup but not visible, a dead end, a missing landmark) carry `basis: structure`.

Floors (never adapt; any breach is at least `medium`, `high` on a primary action or primary text):

| Floor | Standard |
|---|---|
| Text contrast 4.5:1 body, 3:1 large text (24px+, or 18.66px+ bold) and UI boundaries | WCAG 1.4.3, 1.4.11 |
| Interactive target at least 24x24 CSS px; exempt: a link inside a sentence of running text, and targets whose 24px circles do not overlap a neighbor's (WCAG 2.5.8 spacing exception). A native checkbox, radio, or switch wrapped in or associated with a clickable `<label>` is measured by the label's box (`get box` on the label), and the spacing exception applies to it like any other target. Standalone controls and icon buttons are never exempt. | WCAG 2.5.8 |
| Focus visible on every interactive element reached by Tab | WCAG 2.4.7 |
| No horizontal overflow at the configured viewport | layout |
| No console error or failed request on load | runtime |
| Any axe `serious` or `critical` violation | axe-core |

Norms (adapt): control height and width per class (`buttons`, `nav-links`), body font size and line height, sibling gap. A class's norm is the median of its samples when every sample lies within 2px of that median, at any sample count from 2 up, re-evaluated on every new sample; provenance `measured (<surfaces>, n=<count>)`. Samples that do not agree: no norm, the lens stays `Clear` unless a floor is breached. A deviation of more than 2px from a norm is `low` (`medium` when the deviating control is the surface's primary action); a difference of 2px or less is never a finding. A norm that breaches a floor keeps the floor in force, and the breach is one systemic finding listing every location.

Environment rows: phase 0 also records in `rubric.md` the declared `breakpoints` (every `max-width`/`min-width` value in the stylesheets and any breakpoint ladder in a design doc), the declared `modes` (light, dark, high contrast, from `.dark`, `[data-theme]`, `prefers-color-scheme`), and whether `prefers-reduced-motion` is handled. The page dynamics pass reads these rows.

Expectations: every checkable statement in README, docs, PRD, a11y or performance statements ("targets WCAG AA", "every table can be exported", "works on mobile") is an `exp-<n>` row with the quote, `applies_to` (all, or a surface pattern), an intent-level `check`, severity (default `high`), and `provenance: evidenced (path:line)`. Phase 2 verifies them per surface like claims.

## Sweep

Run after the surface's claims, in the same session:

```bash
$S screenshot --full surfaces/<slug>/screenshots/<slug>--full.png
$S a11y --json > surfaces/<slug>/a11y.json
$S errors
$S console
$S vitals                                   # LCP / CLS / INP where the page yields them
$S snapshot                                 # full tree: headings, landmarks, labels
```

Mobile pass (390x844): run it on every surface if `:mobile` or a second viewport is configured, or if the repo declares a breakpoint at or below 600px or uses responsive utility prefixes (`sm:`, `md:`); a repo whose only breakpoints sit above 600px is covered by the breakpoint ladder alone; `$S set viewport 390 844`, reload, `screenshot --full ... <slug>--mobile.png`, `eval document.documentElement.scrollWidth`, then restore the configured viewport and reload. A surface that overflows by a measured amount is its own `layout` finding. If none of those conditions holds, run no mobile pass and file one `low` finding "no responsive layout" on the entry surface, with the grep for `@media` as its measurement.

Feature surfaces (session, search, theme) get no sweep; their `critique.md` states `sweep: n/a - governed pages: <slugs>`. A surface whose destination never rendered an app page (a 404 or error document) gets no sweep either; its `critique.md` states `sweep: n/a - destination did not render` and names the ticket that covers it.

Then walk the categories against the screenshot and the tree. Measure before you write: `get styles`, `get box`, `eval` for computed values, `hover` then `get styles` for hover states. Focus visibility is measured only by a real keyboard walk: `press Tab` repeatedly, `screenshot` and `get styles` on `document.activeElement` at each stop. The `focus` command alone never decides a focus finding; Chrome suppresses `:focus-visible` for programmatic focus.

## Contrast measurement

```bash
$S eval "$(cat <<'JS'
(() => { const sel = '<selector>'; const el = document.querySelector(sel); if (!el) return {error:'no element'};
  const p = c => c.match(/\d+(\.\d+)?/g).slice(0,3).map(Number);
  const lum = ([r,g,b]) => { const f = v => { v/=255; return v<=0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055,2.4); }; return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b); };
  let bg = null, n = el; while (n && (!bg || bg === 'rgba(0, 0, 0, 0)')) { bg = getComputedStyle(n).backgroundColor; n = n.parentElement; }
  if (!bg || bg === 'rgba(0, 0, 0, 0)') bg = 'rgb(255, 255, 255)';
  const cs = getComputedStyle(el); const L1 = lum(p(cs.color)), L2 = lum(p(bg));
  return { selector: sel, color: cs.color, background: bg, fontSize: cs.fontSize, fontWeight: cs.fontWeight, ratio: +(((Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05)).toFixed(2)) }; })()
JS
)"
```

## Impression paragraph

Every `critique.md` opens with `## Impression`: three to six sentences of what a person feels in the first five seconds on the surface (trust, clarity, density, where the eye lands, what a first-time user would do next). It may use feeling words; it is never ticketed on its own and orders the findings below it.

## The critique, in order

### A. Design read (five to ten measured sentences, then findings)

Walk `references/ui-state-model.md` section 5 against the overview screenshot, the full-page screenshot, and the tree, and write the `## Design read` paragraph: each sentence carries a measurement, and each problem it names becomes a finding with the principle from that table.

| Lens | Look for | Measure with |
|---|---|---|
| hierarchy | more than one primary-styled action; heading order skips; the largest or boldest element is not the page's purpose; the eye lands on chrome | count of primary-styled controls; heading levels from `snapshot`; `get styles` font-size and weight on the top three elements |
| grouping (proximity, common region, similarity) | related controls further apart than unrelated ones; labels far from fields; siblings of one kind styled differently; groups with no boundary | `get box` gaps between related vs unrelated siblings; `get styles` on siblings |
| rhythm and alignment | edges that do not line up; gaps off the project scale; uneven padding among siblings | `get box` left edges and gaps vs `rubric.md` norms |
| repetition and density | the same chrome repeated per item (feedback buttons under every message, a trash icon on every row, a label on every card); a list whose rows are indistinguishable | count of repeated controls per item; count of items sharing identical text |
| signifiers | a control that does not look clickable; a non-control that does; a link styled as a button or the reverse; an action available only on hover with no keyboard or persistent path; a disabled look on an enabled control; an icon with no label or tooltip | `cursor`, hover diff, `is visible` without hover, keyboard reachability, tooltip after `hover` |
| copy and honesty | raw identifiers, wire codes, enum names, provider paths, hex ids, camelCase, or `_` in user copy; "Something went wrong" errors; a zero standing in for "not measured"; "live" that is not live; unlabelled sample data; inconsistent casing among sibling labels; developer vocabulary | `get text` scans; provenance of figures |
| empty, loading, error quality | a bare "No results"; an empty state with no next action; a skeleton that does not mirror the layout or never resolves; an error with no retry; raw JSON or a stack on screen | the `states.jsonl` rows for `empty`, `loading`, `error` |
| consistency | the same control class with different heights, radii, casing, or icon style on this surface vs the entry surface; two ways to do one thing | `get box` and `get styles` on the class here and on the entry surface; a table of values |
| typography | more sizes on the surface than the ladder allows; body under the floor; line length over 90 characters; line height under 1.3; more than two families | `get styles` font-size set; measured line length |
| color semantics | a status color used for decoration; direction colored like status; more than one action color; a hover wash that is invisible | count of distinct accent colors on primary controls; status color on non-status elements |

### B. State completeness (from states.jsonl)

Build the `## State matrix` from this surface's `states.jsonl` rows. Every `missing` or `broken` cell is a finding with `category: states`, `basis: structure`, the class row's expected behaviour as the principle, and the state screenshot as evidence:

| State gap | Severity |
|---|---|
| no focus-visible ring on any control of a class; hover-only affordance with no keyboard or persistent path; a form that submits while invalid; an overlay that does not trap or return focus, or does not close on Escape; a skeleton that never resolves; raw error output on failure | high |
| no hover feedback on a control class; disabled with no exposed reason; no empty state or a bare one; no loading indicator over 1 s; no error state with a retry; a toast that cannot be read in time or covers a needed control; no busy state on a submit | medium |
| no active (pressed) feedback; a missing indeterminate or overflow state; a tooltip only on hover and not on focus | low |

### C. Transformations (from the page dynamics rows)

Fill `## Transformations` from the `component: page` rows. Findings use `category: transformation` (or `layout` for overflow, `motion` for animation, `color-contrast` for a dark-mode contrast breach):

| Dynamic | Finding when |
|---|---|
| breakpoints | horizontal overflow, overlap, clipped labels, a collapsed rail with no way to open it, a table unreadable at a band, a control that disappears with no replacement, layout that changes between bands without a plan (widths that shrink instead of re-flow) |
| theme modes | a component with no dark partner (light island), text that vanishes, a contrast floor breached only in one mode, a preference that does not persist |
| reduced motion | a loop that keeps running, an entrance that still animates, content that never appears because its entrance was skipped |
| overlays | focus not moved in or not returned, Tab escapes, Escape ignored, scrim click inert without a visible close, two overlays open at once, page scrolls behind a modal |
| forms | error not naming the field or the fix, submit enabled while invalid, double submit possible, no success feedback, data lost on server error, no unsaved-changes guard on a dirty form |
| navigation | full reload where soft navigation is promised, active item not marked, back lands elsewhere or loses scroll, deep link fails without the list |
| scroll | sticky chrome covering the first row or an anchor target, an inner scroll region that traps the wheel or is unreachable by keyboard, layout shift on load (CLS over 0.1) |
| keyboard | a stop with no visible ring, a control unreachable by Tab, order that does not match the visual order, a trap |
| time | a toast under 4 s with no hover pause, auto-refresh that steals focus or scroll, an action with no feedback within 300 ms |

### D. Floors and norms (measured everywhere, reported once)

Contrast, target size, focus visibility, overflow, console errors, and axe serious/critical are measured on every surface with the sweep commands below. They are reported as one systemic finding per rule or token across the whole run (the cluster is keyed by the CSS rule, the token, or the component class, not the surface), written in the critique of the surface where first seen and referenced by id from every other surface. A surface's critique therefore leads with its design read and state matrix; the floor rows sit last. Reported once does not mean ticketed never: every floor finding at `medium` or above becomes a ticket in phase 3, one per cluster, listing every location.

Severity for every finding: `critical` blocks a core flow or discards a record the user created or edited; `high` a feature is unusable, a floor breach on primary text or the primary action, horizontal overflow at the configured viewport, a hidden primary-path control, or a state gap from the high row above; `medium` any other floor breach, a hidden secondary control with no revealing condition, a missing landmark or unlabelled input (axe serious/critical), a console error or failed request on load, a design-read finding that misleads or costs a workaround (raw identifiers, codes, or enum names in user copy are always at least `medium`), a state gap from the medium row; `low` a norm deviation, cosmetic, polish, axe minor/moderate, overflow at 390 in a repo with no responsive CSS, a state gap from the low row. Phase 3 tickets everything `medium` and above individually and rolls `low` into one polish ticket per surface.

Systemic issues: a floor breach that is a project-wide rule (the same caption color everywhere, every icon button 20px, no focus ring on any `.btn`) is ONE finding with a `cluster` value and every location listed, written in the critique of the surface where it was first seen and referenced by id from the others. The same applies to a state gap shared by a component class across surfaces.

## Finding format (critique.md)

```
### dsg-<slug>-<n>: <short title>
- severity: critical | high | medium | low
- category: functional-affordance | layout | hierarchy | typography | color-contrast | states | transformation | consistency | navigation | content | hit-areas | accessibility | performance | motion | polish
- basis: floor | norm | expectation | human | structure
- element: <selector> - "<on-screen text>" - source: <path from phase 1 evidence or a logged code_peek>
- observed: <the measurement, quoted from the command that produced it>
- principle: <WCAG criterion number, or the named design principle and its source>
- fix: <file path> - <property or class change in the project's own styling system>
- check: <agent-browser command(s) whose output proves the fix>
- screenshot: surfaces/<slug>/screenshots/dsg-<slug>-<n>.png  (element or region capture in the state that shows the finding; never a reused page capture)
```

Every finding gets a line in `findings.jsonl`. Record `Clear` for a category with no finding; never imply a category was inspected when it was not.

## Never

- "Consider improving spacing", "feels cramped", "could be more modern". No measurement, no finding.
- A finding for a control under 40px or 44px that is at or above the 24x24 floor and at its class's norm.
- A fix that introduces a second styling system into the repo.
- A finding on an element a verdict already contradicted for the same reason, except the hidden-control sweep's `navigation` finding, which is always written and links the claim id.
- Skipping the sweep on a surface because it "looks fine". The a11y audit and the console find what eyes miss.
- A critique with no design read, no state matrix, or no transformations table. A surface whose critique is only contrast and target-size rows was not critiqued.
- A finding whose screenshot is the page overview or a claim capture that does not show the measured thing.
- One contrast or hit-area finding per element per surface. Cluster by rule or token; list the locations.
