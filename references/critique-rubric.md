# Critique rubric (phase 2, per surface)

A finding without a measurement is an opinion. A finding without a file and a property is a complaint. A finding without a check is a wish. Every finding has all three.

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

Mobile pass: run it on every surface if `:mobile` or a second viewport is configured, or if the repo has media queries or responsive utility prefixes (`sm:`, `md:`); `$S set viewport 390 844`, reload, `screenshot --full ... <slug>--mobile.png`, `eval document.documentElement.scrollWidth`, then restore the configured viewport and reload. A surface that overflows by a measured amount is its own `layout` finding. If none of those conditions holds, run no mobile pass and file one `low` finding "no responsive layout" on the entry surface, with the grep for `@media` as its measurement.

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

## Categories and what counts as a finding

| Category | Look for | Measure with |
|---|---|---|
| functional-affordance | a control with no visible hover, focus, or press feedback; an action with no confirmation, loading state, or result; a destructive action with no confirm | `hover`/`focus` + `get styles`; `does` verdicts |
| layout | overflow, horizontal scroll, overlap, clipped text, misaligned siblings off by more than 2px | `get box`, `eval document.documentElement.scrollWidth`, screenshot |
| hierarchy | more than one primary-styled action; heading order skips; the focal point is not the page's purpose | snapshot headings, `get styles` on primary and secondary controls |
| typography | body text under the project's norm or under 14px when no norm exists and the text is primary content; line length over 90 characters; truncation without a title | `get styles` font-size / line-height |
| color-contrast | text or UI boundaries below the floor; state colors that do not differ from neutrals | the contrast snippet, `a11y --json` |
| states | missing empty, loading, error, or success states; success not announced; errors that do not name the field | drive the state, screenshot it |
| navigation | dead ends, no way back, active item not marked, a control in the markup but not visible or reachable with no revealing condition (from the hidden-control sweep), links styled as buttons or the reverse | `snapshot -i`, `is visible`, `get html` |
| content | typos, placeholder text, inconsistent terminology or casing among sibling labels, developer vocabulary in user copy | `get text` |
| hit-areas | any target under the 24x24 floor; a control off its class's measured norm by more than 2px | `get box` |
| accessibility | axe violations, unlabeled inputs, no focus ring, focus order, missing landmarks, images without alt | `a11y --json`, `focus` + screenshot, `press Tab` walk |
| performance | LCP over 2.5 s, CLS over 0.1, console errors or failed requests on load | `vitals`, `errors`, `network requests` |
| polish | non-concentric radii, mixed shadow and border depth cues, icon and text baseline misalignment, `transition: all`, motion as the only feedback | `get styles`, screenshot |

Severity: `critical` blocks a core flow or discards a record the user created or edited; `high` a feature is unusable, a floor breach on primary text or the primary action, horizontal overflow at the configured viewport, a hidden primary-path control; `medium` any other floor breach, a hidden secondary control with no revealing condition, a missing landmark or unlabeled input (axe serious/critical), a console error or failed request on load, works with noticeable friction; `low` a norm deviation, cosmetic, polish, axe minor/moderate, overflow at 390 in a repo with no responsive CSS. Phase 3 tickets everything `medium` and above individually and rolls `low` into one polish ticket per surface.

Systemic issues: a floor breach that is a project-wide rule (the same caption color everywhere, every icon button 20px) is ONE finding with a `cluster` value and every location listed, written in the critique of the surface where it was first seen and referenced by id from the others.

## Impression paragraph

Every `critique.md` opens with `## Impression`: three to six sentences of what a person feels in the first five seconds on the surface (trust, clarity, density, where the eye lands, what a first-time user would do next). It may use feeling words; it is never ticketed on its own and orders the findings below it.

## Finding format (critique.md)

```
### dsg-<slug>-<n>: <short title>
- severity: critical | high | medium | low
- category: <one of the table above>
- basis: floor | norm | expectation | human | structure
- element: <selector> - "<on-screen text>" - source: <path from phase 1 evidence or a logged code_peek>
- observed: <the measurement, quoted from the command that produced it>
- principle: <WCAG criterion number, or the named design principle and its source>
- fix: <file path> - <property or class change in the project's own styling system>
- check: <agent-browser command(s) whose output proves the fix>
- screenshot: surfaces/<slug>/screenshots/dsg-<slug>-<n>.png
```

Every finding gets a line in `findings.jsonl`. Record `Clear` for a category with no finding; never imply a category was inspected when it was not.

## Never

- "Consider improving spacing", "feels cramped", "could be more modern". No measurement, no finding.
- A finding for a control under 40px or 44px that is at or above the 24x24 floor and at its class's norm.
- A fix that introduces a second styling system into the repo.
- A finding on an element a verdict already contradicted for the same reason, except the hidden-control sweep's `navigation` finding, which is always written and links the claim id.
- Skipping the sweep on a surface because it "looks fine". The a11y audit and the console find what eyes miss.
