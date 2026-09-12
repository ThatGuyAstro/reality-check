# The tour persona and claim extraction (phase 1)

You are recording a how-to video of this app for someone who has never seen it. You have the source code open on a second monitor and nothing else: no running app, no browser, no screenshots, no prior verdicts. Everything you say, you say because the code makes a user expect it.

## Reading order

Read in this order and keep `path:line` notes per surface. The order is what makes the narration a path rather than a list.

1. Entry and routing: router config, `app/` or `pages/` tree, `routes.rb`, `web.php`, `urls.py`, plain HTML files and their links; redirects on first visit; guards and middleware; 404 handling.
2. Layout and navigation: shells, sidebars, headers, nav arrays, menus, breadcrumbs, links inside pages, buttons that route.
3. Each surface in the order a first-time user reaches it: the page component, its children, its data source, forms and handlers, API calls, conditional rendering, empty and error states, copy strings, styles.
4. Handlers and effects: click and submit handlers, API calls, redirects, local storage, toasts, downloads.
5. Cross-surface features: session and auth, search, notifications, theme, settings persistence, exports.
6. Copy that promises something: README and docs claims, marketing lines, tooltips, empty-state hints, help text.
7. State signals, per surface, with `references/ui-state-model.md` open: every `:hover`, `:focus-visible`, `:active`, `:disabled`, `[aria-expanded]`, `[aria-selected]`, `[data-state]`, `.is-*` rule that touches this surface's components; every `loading.tsx`, `Suspense` fallback, skeleton component, empty branch, error branch, `disabled=` expression, toast or dialog or menu library call, `transition` and `animation`; every breakpoint, `.dark` or `[data-theme]`, and `prefers-*` media query. These are promises about how the page looks and transforms, and they become claims.

Do not run it, start it, curl it, probe its port, or open `docs/reality-check/verdicts.jsonl` or any prior verification file. On a re-tour, read only `claims.jsonl` to reuse ids after the new transcript is written.

## State inventory (components.md)

Before narrating a surface, write `surfaces/<slug>/components.md` from `templates/components.md`: one row per component class on the surface (button, icon button, nav item, tab, input, select, menu, dialog, drawer, list row, card, toast, skeleton, form, empty stage, stream), the states the code declares for it (from reading step 7, cited `path:line`), and the states `references/ui-state-model.md` section 2 expects that the code does not declare. Feature surfaces and destinations with no code get a one-line `components.md` (`n/a - exercised on <slugs>` or `n/a - target not found in code`). The inventory is the narrator's checklist: every declared state becomes a claim below; every expected-but-undeclared state becomes a `guess` claim that the user would still expect it ("I expect the Save button to stay disabled until I change something").

## Depth: tiered, unbounded

- Primary path: the continuous route a first-time user takes - entry, auth if any, the main surface, then each feature reachable from the main navigation, in nav order. Narrate every surface on it in full: what renders, what each control does, what feedback appears, what persists.
- Everything else reachable (secondary routes, admin surfaces, modals from menus, footer links): at least one `exists` claim and one `flows` claim each.
- Every item in the primary navigation and every call-to-action gets its own `flows` claim, even when no code for the target exists: `expected` is what the label implies ("a Reports page with the app chrome"), `confidence: guess`, evidence notes `target not found in code`. A link with no destination is exactly the gap phase 2 exists to catch. Such a destination gets its own surface with one `exists` claim, stays `tier: primary` when its link sits in the primary navigation, and is narrated as its own scene at the point in the walk where the user would reach it; "in full" means everything the code offers, which for a missing page is those two claims.
- No cap on surfaces or claims. A large app gets a long tour.
- Every surface narrates its states, not only its contents. Per component class in `components.md`: at least one `looks` claim for each interaction or availability state the code declares (hover, focus, pressed, disabled with its reason, busy), one `looks` claim per data state branch (skeleton, empty, error, degraded) with the copy quoted, and one `state` claim per transformation the page performs (a panel or menu opening and closing with focus behaviour, a rail collapsing, the layout at each declared breakpoint, each declared theme mode, reduced motion, persistence across reload). A surface with interactive components and no `looks` claims is an incomplete tour.

## Voice

State sentences are narrated the same way, in the user's time: "I hover a card and it lifts a hair and its border darkens." "I press Save with the name empty and the field turns red with a message under it that says what to fix." "While the answer streams, the Send button becomes Stop." "With no connections yet, the table is replaced by a note that explains what a connection is and offers Add connection." "When I narrow the window under 900px the navigation collapses to icons and a menu button appears." "In dark mode the cards sit on a darker sheet and the text stays readable."


The default persona is `howto` (`personas/howto.md`). Whatever the persona:

- First person, present tense, one action or observation per sentence. "I open the app and land on a sign-in form with an email field, a password field, and a Sign in button."
- Name the trigger before the outcome. "I press Sign in. The app takes me to the dashboard."
- One observable per sentence. "I see three summary cards" and "the first card reads Total balance" are two sentences and two claims.
- Name things by their on-screen text ("the Export CSV button"), never by identifiers; identifiers go in the evidence column.
- Quote copy exactly as the code has it, including capitalization. Never invent data values; when a seed or fixture states real values, quote them and cite the file.
- Narrate the unhappy path when the code offers one: "If I get the password wrong, an inline message tells me the combination is not right."

## The user's-side rule

The persona narrates what a user expects from what the screen offers, not what the implementation will do. This is the rule that makes the measurement work, so it has no exceptions:

- A control with no handler, an empty handler, or a TODO is narrated as the persona expects it to behave: "I click Export CSV and a file downloads." Tag `guess`. Never "I expect nothing to happen because there is no handler".
- A control present in the markup but hidden by a stylesheet, an inline style, or a condition the persona has no reason to know about is narrated as visible: "Below the form I see a Create account link." Tag `guess`, and note the hiding rule in the evidence column so phase 3 can point at it. Never "the CSS hides it, so I do not see it". If the tour can name the user-visible condition that reveals it (a toggle, a role, a plan), narrate that condition instead and tag `inferred`.
- A link or route whose target file cannot be found is still narrated as opening: "I click Reports and a reports page opens." Tag `guess`, evidence `target not found in code`.
- Doubt lives in the confidence tag and in a prose aside, never in `expected`. Hedge honestly in prose ("I expect a toast here"); the claim row is still one binary-checkable observable.

## Promises

When product copy or repo docs promise something ("Export anytime", "Syncs every hour", "you can enable two-factor authentication below", README "every table can be exported as CSV"), the narrator quotes it and states what a user would expect to be able to do. That is a `promise` claim whose `expected` is the promised capability and whose verification attempts it. Copy that merely labels (button text, headings) is `shows`, not `promise`. README and docs promises also become `exp-<n>` rows in `rubric.md` (phase 0) and are checked on every applicable surface; a promise claim and an expectation row may describe the same capability, and both are recorded.

## Demo script format

`tour.md` follows `templates/tour.md`: a scene per surface with a `Start:` line and running time (4 seconds per claim sentence plus 3 seconds per `[cue]`), a `[cue]` line immediately before the sentence that narrates the action's outcome (the cue is the presenter's move; the next anchored sentence is what the viewer then sees), and every claim-bearing sentence ending with its anchor `[clm-<slug>-<n>]`. Pure narration (transitions, persona color) carries no anchor.

## Claim extraction

After the transcript is written, walk it top to bottom and write one row per anchored sentence in `surfaces/<slug>/claims.md` and one line in `claims.jsonl`:

- `id`: `clm-<slug>-<n>`, numbered in transcript order per surface.
- `kind`: one of the seven in SKILL.md `<claims>`. A sentence that fits two kinds is two claims.
- `component` and `state` (for `looks` and `state` claims about a component): the component class from `components.md` and the state point from `references/ui-state-model.md` section 1 (`hover`, `focus-visible`, `active`, `disabled`, `busy`, `loading`, `empty`, `error`, `open`, `expanded`, `selected`, `invalid`, `dark`, `narrow:<band>`, `reduced-motion`). `trigger` says how the state is reached ("hover the row", "narrow the window to 900px", "submit with the name empty").
- `functional`: true for `does`, `flows`, `state`, `promise`.
- `claim`: the sentence verbatim.
- `expected`: one observable a browser can check. Not "it works"; "a file download starts or a toast reading Export ready appears".
- `trigger`: the user action, or `none` for on-load claims.
- `preconditions`: claim ids that must hold first (signed in, on this surface, record exists).
- `evidence`: `path:line` locations that produced the belief. At least one. Two locations, two pointers.
- `confidence`: `sure` | `inferred` | `guess` per SKILL.md.
- `destructive`: true when the trigger deletes, cancels, sends, or pays.
- `tier`: `primary` for claims on the continuous demo path (including every primary-navigation item and its destination), `secondary` for side branches and footer or deep links, `feature` for claims on a cross-surface feature surface (session, search, theme).

Surface slugs: kebab-case from the route or screen name (`login`, `dashboard`, `settings-profile`). Cross-surface features get a feature slug (`session`, `search`). Keep slugs stable across runs.

## Reconciliation on re-tour

When `claims.jsonl` already exists, write the new transcript first, then reconcile: a new claim whose `surface + kind + trigger + expected` matches an existing claim keeps the existing id; existing claims with no match get `status: retired`; unmatched new claims take the next `n` for their surface. Never renumber.
