# Planted answer key - fixtures/orbit

Never copy this file into a run's fixture directory. The served root is `site/`. Serve with `cd site && python3 -m http.server 4180`. Account in `site/README.md` (demo@orbit.test / orbit-pass).

Orbit plants state, transformation, and design defects that a static audit (axe, contrast, target size) cannot find. A correct run drives every component through its states, walks the declared breakpoint and theme, and reads the page as a designer would.

| # | Plant | Where | What a correct run produces |
|---|---|---|---|
| P1 | Card actions (Archive, Edit) appear only on pointer hover; keyboard focus never reveals them | `css/app.css` `.card .actions` opacity 0, `.card:hover .actions` | state row card/hover `present` and card/focus-visible `broken` (actions still hidden), or a `signifiers`/`states` finding "hover-only affordance with no keyboard path", severity high, ticket |
| P2 | New task dialog: focus does not move in, Tab escapes to the page, Escape does nothing (scrim click and Cancel close it) | `js/board.js` openDlg, `board.html` #new-dialog | overlay rows: focus-in `missing`, trap `broken`, escape `missing`; finding `transformation`/`states`; ticket high |
| P3 | Filter menu never closes on outside click or Escape | `js/board.js` menu handlers | menu rows: escape `missing`, outside-click `missing`; ticket |
| P4 | Calendar view is a bare "No results" | `js/board.js` render() calendar branch | empty state `broken`, finding `content`/`states` "bare empty state, no next action", ticket medium; the README promises "Every list has a helpful empty state" so exp- row contradicted on board |
| P5 | Activity page "Recent comments" skeleton never resolves | `activity.html` #comments, `js/activity.js` (no code touches #comments) | loading `broken` "skeleton never resolves", ticket high |
| P6 | Profile form: empty name shows "Something went wrong." not naming the field; Save stays enabled while invalid; valid save gives no success feedback | `settings.html` inline script | form rows: invalid `broken` (message names nothing), submitting/success `missing`; two findings; tickets (high + medium) |
| P7 | Export button disabled with no reason exposed | `board.html` #export-btn | disabled `broken` (no title/describedby), finding medium, ticket |
| P8 | Dark mode: `.card` ground hard-coded white (light islands); filter menu hard-coded white text on white in dark | `css/app.css` `.card { background:#ffffff }`, `.menu { background:#ffffff; color:#ffffff }` | dark row `broken` for card and menu; findings `transformation`/`color-contrast` in dark; tickets; README promise "Dark mode is supported" exp- contradicted |
| P9 | At <=900px the sidebar becomes a fixed overlay while `.main` never shifts (sidebar covers the first column), and `.columns` keeps min-width 932px (horizontal overflow) | `css/app.css` `@media (max-width: 900px)`, `.columns` | narrow:900 `broken`: scrollWidth > innerWidth and sidebar box overlaps main; finding `layout`/`transformation` high; README "Works down to 900px" exp- contradicted |
| P10 | Signifiers: "Delete all done" is an `<a>` styled as a primary button, destructive, no confirm; "View archive" is a `<button>` styled as a link; two primary-styled actions compete in the toolbar | `board.html` toolbar, `css/app.css` `.btn-like`, `.link-like` | design-read findings: hierarchy (two primary actions), signifiers (link as button, button as link), error prevention (destructive without confirm); severity medium+; tickets |
| P11 | Raw identifiers in copy: assignee `usr_8f3a`, status chip `TODO`/`IN_PROGRESS` enum casing, task ids `tsk_*` | `js/board.js` card(), `data/tasks.json` | content/honesty finding "raw identifiers in user copy"; ticket medium |
| P12 | Repetition: every card carries "Sample data · Learn more" | `js/board.js` card() | design-read finding repetition per item; low or medium |
| P13 | Motion: card hover scales 1.04 over `transition: all .6s` (layout motion, slow); header dot pulses forever meaning nothing; reduced motion stops only the shimmer | `css/app.css` `.card:hover`, `.live-dot`, `@media (prefers-reduced-motion)` | reduced-motion row `broken` (pulse still animating); motion finding on hover scale/duration; honesty finding on the dot; README "Respects the reduced-motion preference" exp- contradicted |
| P14 | Sticky toolbar covers the anchor target: the sidebar "Archived" link to `#archived` (a section 640px below the board, so it requires scrolling) lands the heading under the sticky toolbar | `css/app.css` `.toolbar` sticky, `board.html` nav and #archived | scroll row `broken` (anchor target box top < toolbar bottom); finding `transformation` medium |
| P15 | Toast "Theme updated" dismisses after 700 ms, no hover pause | `settings.html` orbitToast(…, 700) | time row `broken`; finding medium |
| P16 | `button:focus` and `button:focus-visible` set `outline:none` with no replacement: no focus ring on any button | `css/app.css` | keyboard-only / focus-visible rows `broken` for every button class; ONE systemic finding (cluster), high; README "Fully keyboard accessible" exp- contradicted |

Working states that must be `present` or `confirmed` and never ticketed:
- Sign in button: hover, active (scale .97), primary styling; wrong password shows an inline error naming the mismatch.
- Search input: focus ring, filters cards as you type.
- Tabs Board/List: `aria-selected` switches, arrow keys move selection, the List view renders a table.
- Sidebar collapse toggle: `aria-expanded` flips, labels hide, preference persists across reload.
- Done column: a helpful empty state ("Nothing is done yet… Add a task"); List view with a filter that matches nothing: a helpful empty state with "Clear the filter".
- Activity list loads and renders three rows; its own error branch (with `network route --abort`) shows "We could not load activity" with Try again.
- Theme preference persists across reload; the sidebar, toolbar, panels, and inputs do have dark partners.
- Nav items mark the current page (`aria-current`) and show hover and focus-visible rings (nav links keep their ring; only buttons lost theirs).
