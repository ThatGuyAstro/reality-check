# UI state model (read by phase 1 and phase 2)

A page is not a picture. Every component on it sits at one point on several axes of state at
once, and the page itself transforms as the viewport, the theme, the data, and the user's
actions change. The tour claims those states from the code; the verify pass drives each one and
photographs it; the critique judges whether the set is complete and whether each state does its
job. This file is the shared vocabulary.

## 1. The axes of component state

| Axis | Points | The code declares it with |
|---|---|---|
| Interaction | rest, hover, focus-visible, active (pressed), hover+focus | `:hover`, `:focus-visible`, `:active`, `whileHover`, `whileTap`, `@media (hover: hover)` |
| Availability | enabled, disabled (with an exposed reason), readonly, busy or loading, locked | `disabled`, `aria-disabled`, `readonly`, `aria-busy`, `title` or `aria-describedby` on a disabled control, spinner branches |
| Data | loading (skeleton), empty (zero items), partial, full, overflow (many items, long strings), error (load failed), stale or degraded (offline, simulated, sample) | `loading.tsx`, `Suspense` fallbacks, `items.length === 0` branches, `error.tsx`, `catch` branches, "sample" and "simulated" labels, pagination and "load more" |
| Selection and disclosure | selected, checked, indeterminate, expanded, open, current, pinned, dragging, drop target | `aria-selected`, `aria-checked`, `aria-expanded`, `aria-current`, `data-state`, `.is-open`, `.active`, `open` on `<details>` |
| Validation (forms) | pristine, dirty, invalid, valid, submitting, succeeded, failed, unsaved changes | `required`, `pattern`, `aria-invalid`, `aria-describedby` to an error, an `errors` object, `isSubmitting`, `beforeunload` |
| Environment | each declared viewport band, light, dark, high contrast, reduced motion, pointer fine or coarse, zoom 200%, offline | `@media (max-width)`, `.dark` or `[data-theme]`, `prefers-color-scheme`, `prefers-reduced-motion`, `prefers-contrast`, `pointer: coarse`, `navigator.onLine` |

A component's state set is the product of the axes that apply to it. A primary button has rest, hover, focus-visible, active, disabled, and busy, in light and dark, at every band. A list has loading, empty, partial, full, overflow, and error. A dialog has closed, opening, open, and closing, with focus inside, and a scrim.

## 2. Component classes and the states each must have

For every class present on a surface, the states in the second column are expected unless the code says otherwise. The third column is how phase 2 puts the component into the state; the fourth is what proves it.

| Class | Expected states | Drive it with | Evidence |
|---|---|---|---|
| Button, primary and secondary | rest, hover, focus-visible, active, disabled (reason exposed), busy | `hover`, `press Tab` until it is `document.activeElement`, `mouse down` then screenshot then `mouse up`, find a disabled instance or a precondition that disables it, trigger the action and capture within 300 ms | `get styles` on background, color, border, box-shadow, outline, transform per state; element screenshot per state |
| Icon button | same as button plus an accessible name and a tooltip or label | as above; `hover` then wait 200 ms for a tooltip | name in `snapshot -i`; tooltip element present after hover |
| Link and nav item | rest, hover, focus-visible, current (aria-current or active class), visited where the app styles it | `hover`, Tab walk, navigate to the target and read the item again | `aria-current` or class in `get html`; `get styles` color and underline |
| Tab | selected, unselected, hover, focus-visible; arrow keys move selection | click, `press ArrowRight` | `aria-selected`; panel content changes |
| Chip, toggle, segmented control | on, off, hover, focus-visible, disabled | click, Tab | `aria-pressed` or `aria-checked`; style diff |
| Switch, checkbox, radio | checked, unchecked, indeterminate, disabled, focus-visible; the label toggles it | click the label, `press Space` | `is checked`; `get box` on the label |
| Text input, textarea | rest, focus (ring), filled, placeholder, disabled, readonly, invalid (message names the field and the fix), with helper text; counter when there is a limit | `fill`, `press Tab`, submit empty, submit bad input | `aria-invalid`, `aria-describedby` target text, `get styles` outline and border |
| Select, combobox, autocomplete | closed, open, hover on option, highlighted option, selected, empty results, disabled; Escape closes | click, `press ArrowDown`, `press Escape`, type a string with no match | `aria-expanded`; listbox present; "no results" copy |
| Search | rest, focus, typing (debounce), results, no results, cleared | type, wait, type nonsense, clear | result region text; "no results" state |
| Menu and dropdown | closed, open, hover on item, keyboard navigation, disabled item, close on Escape, close on outside click, focus returns to the trigger | click trigger, `press ArrowDown`, `press Escape`, click outside | `aria-expanded`; `document.activeElement` after close |
| Dialog and modal | closed, open with focus inside, Tab trapped, Escape closes, scrim click closes or is deliberately inert, focus returns, page scroll locked | open, `press Tab` past the last control, `press Escape`, click the scrim | `document.activeElement` inside; `body` overflow; dialog absent after Escape |
| Drawer, sheet, side panel | closed, opening, open, closing; the page behind either shifts or is covered; a close control exists | open, close, resize | `get box` on the panel and the content; `aria-expanded` on the toggle |
| Popover and tooltip | hidden, shown on hover, shown on focus, dismissed on Escape or blur | `hover`, `focus`, `press Escape` | element present with `role=tooltip` or a popover role |
| Accordion and disclosure | collapsed, expanded, hover on header, focus-visible, keyboard toggle | click, `press Enter` | `aria-expanded`; content height |
| List and table row | rest, hover (row wash), selected, focus-visible when the row is a control, expanded (detail), actions revealed only on hover (a finding when there is no keyboard path), skeleton, empty, error | `hover`, click, Tab, mock the data source | `get styles` background per state; actions visible without hover via `is visible` |
| Card | rest, hover (lift or border, never layout motion), focus-visible, selected, loading, empty | `hover`, Tab, click | `get styles` transform and box-shadow; screenshot |
| Toast, banner, alert | appears within 300 ms of the trigger, readable long enough (or until dismissed), dismissible, announced (`role=status` or `alert`), does not cover a control the user needs | trigger the action; `wait 300`; `wait 6000` | present then absent; role in `get html`; `get box` overlap with the form |
| Progress, spinner, skeleton | present while pending, mirrors the final layout (skeleton), resolves, never loops after data arrives | throttle or mock the request; observe | element present during pending, absent after; screenshot during |
| Pagination and load more | first, middle, last page, disabled ends, current page marked, count shown | click next, click last | `aria-current` on the page; disabled at the ends |
| Breadcrumb | truth (matches the page), current item not a link | read | text equals the page title chain |
| Badge and count | zero (hidden or "0" by design), one, many, overflow ("99+") | read at different counts if reachable | text |
| Avatar and identity | image, initials fallback, broken image fallback | block the image request | fallback rendered |
| Form | pristine, dirty (Save enabled only then, or an explicit "no changes"), invalid summary, submitting (button busy, double submit blocked), success feedback, server error, unsaved-changes guard | submit empty, fill wrong, fill right, submit twice fast, navigate away dirty | see Validation axis |
| Empty stage | teaches what this area is, orients (why it is empty), offers one next action; never a bare "No results" | reach it via a filter with no matches, a fresh account, or a mocked empty response | copy contains an explanation and a control |
| Stream and live region | working indicator while pending, a stop control, arrival of new content, settled state, stale marker when the feed stops | send a message; watch | `role=status` text over time; `aria-live` region |

## 3. Page dynamics: how a page functions, is used, and transforms

| Dynamic | What to exercise | What good looks like |
|---|---|---|
| Navigation | click every nav item; `back`; `forward`; deep link to a detail URL; `reload` on a stateful page | soft navigation when the app promises it (`performance.timeOrigin` unchanged), the active item marked, scroll restored on back, the deep link renders without the list first, state survives reload where the code persists it |
| Layout transformation | the viewport at every declared breakpoint (rubric `breakpoints`), 1 px above and below each; the rail or sidebar collapsed and open; a split pane resized | no horizontal overflow, no clipped labels, no overlap; columns re-flow in a planned way; the collapse control remains reachable |
| Sticky and scroll | scroll to the bottom and back; scroll a long list inside a region; jump to an anchor | sticky chrome does not cover the first row or the anchor target; inner scroll regions are reachable by keyboard and do not trap the page wheel; the page does not jump (CLS) |
| Overlays | every dialog, menu, drawer, popover: open, Tab through, Escape, click the scrim, close, look at `document.activeElement` | focus moves in, stays in, returns to the trigger; one overlay at a time; Escape and light dismiss behave the same across the app |
| Forms | the full lifecycle from the Form row above | errors name the field and the fix; the primary action is disabled or guarded while submitting; success is announced and visible; nothing is lost on a server error |
| Live and streaming | start a long action; watch the first second, the middle, the end | a working indicator within 300 ms, a way to stop, new content arrives with motion that carries state and stops under reduced motion, a settled state that is distinguishable from working |
| Data volume | zero, one, many, a very long string, a very long list | truncation with a full-text path (title or expand), wrapping without overflow, pagination or virtualization that keeps position |
| Time | a toast, a poll, a session timeout, an auto-refresh | a toast lasts long enough to read and pauses on hover; auto-refresh does not steal focus or scroll |
| Theme | every declared mode (light, dark, high contrast) on every primary surface | every component has a partner in each mode; no light island on a dark page; contrast floors hold in each mode; the preference persists |
| Reduced motion | `set media reduced-motion` and reload | loops stop, entrances become instant, nothing disappears or stays half-drawn |
| Offline and failure | `set offline on` then act; `network route --abort` on the data request; `--body` with an empty payload | an honest error state with a retry, an honest empty state, no raw JSON or stack, no infinite skeleton |
| Keyboard only | complete the primary path with Tab, Enter, Space, arrows, Escape and no pointer | every step reachable, the focus ring visible at every stop, no trap, the order matches the visual order |

## 4. Where the code declares states, by stack

- Any stylesheet: `:hover`, `:focus-visible`, `:active`, `:disabled`, `[aria-*]`, `[data-state]`, `.is-*`, `.active`, `.open`, `@media (hover: hover)`, `@media (max-width)`, `@media (prefers-reduced-motion)`, `@media (prefers-color-scheme)`, `.dark`, `[data-theme]`, `transition`, `animation`, `@keyframes`.
- React and Next.js: `loading.tsx`, `error.tsx`, `not-found.tsx`, `<Suspense fallback>`, `useState` flags named `loading`, `error`, `open`, `expanded`, `selected`, `dirty`; `disabled={}`; `aria-busy`; conditional branches on `length === 0`; `useReducedMotion`; motion `variants`; dialog and menu libraries that set `data-state="open|closed"`; form libraries with an `errors` object; toast libraries.
- Vue, Svelte, Angular: `v-if`/`v-else`, `{#if}`, `*ngIf` on the same flags; `:disabled`; class bindings.
- Server-rendered (Rails, Django, Laravel, plain HTML): template conditionals on empty collections, flash messages, `disabled` attributes, server validation errors rendered next to fields, `<details>`, `<dialog>`, `<template>`.

The narrator reads these as promises the way it reads copy: a `:hover` rule on a row is a claim that hovering the row changes it; an empty-branch string is a claim about what the user sees with no data; `loading.tsx` is a claim that a skeleton appears while the page loads; a breakpoint is a claim that the layout changes there. A state the code never declares is also a claim: "I expect a disabled Save button until I change something" is a `guess`.

## 5. Design heuristics with a violation signature

A finding needs a named principle and evidence that proves the violation. This table gives the name, what the violation looks like, and what to measure. Feelings go in the Impression paragraph; these go in findings.

| Principle | Violation signature | Evidence that proves it |
|---|---|---|
| Visibility of system status (Nielsen 1) | an action with no feedback within 300 ms; a long operation with no progress; a disabled control with no reason; a stale value with no marker | timestamp of trigger and first visible change; `title`/`aria-describedby` absent on the disabled control |
| Match between system and the real world (Nielsen 2) | raw identifiers, wire codes, enum names, provider paths, or developer vocabulary in user copy; jargon labels | `get text` containing `_`, `/`, camelCase, hex ids, or `error` codes |
| User control and freedom (Nielsen 3) | no undo or cancel on a destructive or long action; a modal with no close; a wizard with no back | absence of the control in `snapshot -i` |
| Consistency and standards (Nielsen 4) | the same action styled differently across surfaces; two heights, radii, or label casings for the same control class; a link styled as a button or the reverse | `get box` and `get styles` on the same class across surfaces; a table of values |
| Error prevention (Nielsen 5) | submit enabled while invalid; destructive action one click away with no confirm; free-text where a picker exists | `is enabled` on submit with an empty required field |
| Recognition rather than recall (Nielsen 6) | a field with no placeholder, example, or format hint; an icon with no label or tooltip; a code the user must remember | absence in `get html`; tooltip absent after `hover` |
| Flexibility and efficiency (Nielsen 7) | no keyboard path for a frequent action; no bulk action for a list with hundreds of items; no search on a long list | Tab walk cannot reach it; count of items vs presence of bulk controls |
| Aesthetic and minimalist design (Nielsen 8) | chrome repeated per item (the same four buttons under every message); decorative status color; competing focal points | count of repeated controls; number of primary-styled actions |
| Help users recognize, diagnose, recover from errors (Nielsen 9) | an error that does not name the field or the fix; "Something went wrong"; a red border with no text | `aria-describedby` target text |
| Help and documentation (Nielsen 10) | an empty state or a first run with no guidance | copy in the empty stage |
| Proximity and common region (Gestalt) | related controls separated further than unrelated ones; a label far from its field; groups without a boundary | `get box` gaps: related gap larger than unrelated gap |
| Similarity (Gestalt) | items of the same kind look different; different kinds look the same | `get styles` on siblings |
| Continuity and alignment (Gestalt) | edges that do not line up; ragged columns; a grid that drifts | `get box` left edges among siblings differ by more than 2 px |
| Figure and ground | a scrim that does not separate a dialog; a hover wash that is invisible; low-contrast dividers doing structural work | contrast of the dialog surface vs the scrim; `get styles` on the wash |
| Visual hierarchy | more than one primary action; heading order skips; the largest element is not the page's purpose; the eye lands on chrome | count of `.primary` styles; heading levels from `snapshot`; sizes from `get styles` |
| Rhythm and spacing scale | gaps off the project's scale; uneven padding among siblings; inconsistent gutters | `get box` gaps vs the scale in `rubric.md` |
| Typographic scale | more sizes than the ladder allows; body under the floor; line length over 90 characters; line height under 1.3 | `get styles` font-size set on the surface vs the ladder; measured line length |
| Color semantics | a status color used for decoration; direction colored like status; more than one action color | count of distinct accent colors on primary controls; status color on a non-status element |
| Affordance and signifiers (Norman) | a control that does not look clickable; a non-control that does; an action available only on hover with no keyboard or persistent path; a disabled look on an enabled control | `cursor` style, hover change, keyboard reachability |
| Feedback timing (0.1 s, 1 s, 10 s) | no change within 100 ms of a click; no progress after 1 s; no way out after 10 s | timestamps |
| Fitts's law | small or distant targets for frequent actions; a close control far from the content it closes | `get box` size and distance |
| Hick's law | a menu or toolbar with many equal choices and no grouping; a form with every option at once | count of items per group |
| Progressive disclosure | advanced controls at the same level as primary ones; a settings page that shows everything | count of controls above the fold |
| Empty-state quality | a bare "No results" or "Nothing here"; no next action; a skeleton that never resolves | copy and controls in the empty stage |
| Honesty | "Live" that is not live; a zero that means "not measured"; sample data unlabelled; a fake progress bar | value provenance; presence of "sample" or "simulated" labels |
| Motion purpose | motion that carries no state change; hover that moves layout; loops that never stop; entrances over 300 ms on frequent actions | `get styles` transition and animation; `transform` on hover; reduced-motion diff |
| Dark mode parity | a component with no dark partner; text that vanishes; a light image or island on a dark surface | screenshot per mode; contrast per mode |
| Responsive integrity | overflow, overlap, clipped labels, a collapsed rail with no way to open it, a table that becomes unreadable | `scrollWidth`, `get box` at each band |
