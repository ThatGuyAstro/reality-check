```
        ┌──────────────────────────────────────────────────┐
        │                                                    │
        │   REALITY CHECK                                   │
        │   "the code says it works. does it, though?"      │
        │                                                    │
        └──────────────────────────────────────────────────┘
```

**reality-check** is an agent skill that closes the gap between *what your app's
code implies a user will experience* and *what actually happens when someone opens
a browser and tries it.*

You point it at a running (or startable) web app. It reads the code and writes down,
in plain first-person prose, everything a first-time user would expect to see and do
— like a narrator recording a demo video from the source alone. Then it opens a real
browser, walks that exact script, and marks every single sentence **confirmed** or
**contradicted**, with a screenshot as proof. Anything it finds along the way that the
code never mentioned — a dead button, a link to nowhere, text nobody can read — gets
written down too. Every gap that survives becomes a ticket an agent (or a person) can
pick up and fix, with the repro steps and the fix already sketched out.

It's built as a portable **agent skill**: a folder of instructions any capable coding
agent can read and follow. It works with **Claude Code**, **Cursor CLI**, and
**Codex CLI** out of the box, and it's plain enough Markdown + JSON to run in anything
else that can read a file and drive a browser.

---

## Table of contents

- [Why this exists](#why-this-exists)
- [How it thinks](#how-it-thinks)
- [Quick start](#quick-start)
- [Install](#install)
- [A worked example](#a-worked-example)
- [What you get back](#what-you-get-back)
- [The claim vocabulary](#the-claim-vocabulary)
- [Modes](#modes)
- [Personas](#personas)
- [Design rules, in one breath each](#design-rules-in-one-breath-each)
- [Re-checking after a fix](#re-checking-after-a-fix)
- [Try it on the bundled fixtures](#try-it-on-the-bundled-fixtures)
- [Origin story](#origin-story)
- [Evaluation](#evaluation)
- [FAQ](#faq)
- [Contributing](#contributing)
- [License](#license)

---

## Why this exists

Every coding agent — and most engineers, if we're honest — has done this:

> *Read the handler. Read the route. Yeah, that button downloads a CSV. Looks solid. Ship it.*

And the button does nothing, because the click handler was stubbed out three commits
ago and nobody re-tested it. Or the "Create account" link is real, wired correctly,
and hidden behind a CSS rule nobody remembers writing. Code review catches *some* of
this. Nothing catches *all* of it, because the failure mode is specifically the gap
between **what confident code-reading implies** and **what a browser actually shows**
— and if you only ever read the code, or only ever click around without a script,
you can't see that gap. You need both, done separately, then compared.

That's the whole trick:

```
   ┌────────────────────────┐          ┌────────────────────────┐
   │   WHAT THE CODE SAYS    │          │  WHAT THE BROWSER SHOWS │
   │                         │          │                         │
   │  <button id=export>     │          │  [ click ]              │
   │    Export CSV           │   VS.    │  ...nothing happens.    │
   │  </button>               │          │  no request. no file.   │
   │  onClick={exportCsv}     │          │  no error either.       │
   └────────────────────────┘          └────────────────────────┘
                        \                    /
                         \                  /
                          v                v
                    ┌─────────────────────────┐
                    │   THE GAP = a ticket     │
                    │   TKT-002, filed,        │
                    │   with a repro and a fix │
                    └─────────────────────────┘
```

## How it thinks

Three phases, run strictly in order, on purpose never mixed:

```
  ┌───────────────┐       ┌────────────────┐       ┌────────────────┐
  │   1. TOUR      │  ──▶  │   2. VERIFY     │  ──▶  │   3. TICKETS    │
  │                │       │                 │       │                 │
  │ read the code  │       │ open a real     │       │ every gap and   │
  │ only. write a  │       │ browser only.   │       │ every unnarrated│
  │ first-person   │       │ walk the tour,  │       │ observation     │
  │ demo script.   │       │ mark every line │       │ becomes a       │
  │                │       │ confirmed or    │       │ dispatchable    │
  │ no browser.    │       │ contradicted.   │       │ ticket with a   │
  │ no server.     │       │ screenshot each.│       │ repro + fix.    │
  │ no curl.       │       │ never peek code.│       │                 │
  └───────────────┘       └────────────────┘       └────────────────┘
```

The separation **is** the measurement. If the browser leaks into phase 1, you get a
tour that's already correct — and correctness isn't what you're testing for. If the
code leaks into phase 2, a verdict can get talked into "confirmed" by a comment that
says the button *should* work. Keep them apart and the gap between them becomes a
number you can trust.

A few rules make that gap honest instead of generous:

- **The narrator writes from the user's side, not the implementation's.** A button
  with a stubbed-out handler is still narrated as "I click it and a file downloads" —
  tagged `guess`, because that's what the label promises a user. A link a stylesheet
  hides is narrated as visible. That's *how* a dead button and a hidden link turn
  into measured gaps instead of confirmed facts nobody double-checks.
- **Verdicts are black and white.** `confirmed`, `contradicted`, or
  `blocked(reason)`. No "mostly works," no partial credit. A half-true claim gets
  split into two claims next time, not fudged into one soft verdict.
- **Every verdict carries evidence.** A screenshot, a quoted observation, a URL.
  No exceptions. If you can't show it, it isn't confirmed.
- **The gap runs both directions.** What the code implied and the browser refuted,
  *and* what the browser revealed that the code never even hinted at (an unnarrated
  observation — the things a human notices that no line of the tour predicted).
- **Every state is a surface.** A button is not one picture; it is rest, hover,
  focus, pressed, disabled, and busy, in light and dark, at every breakpoint. A
  list is loading, empty, full, overflowing, or failed. The tour claims the states
  the code declares; the verify pass puts every component into every state and
  photographs it; the critique judges whether the set is complete and whether each
  state does its job. Contrast ratios and target sizes are floors, measured and
  reported once as systemic clusters, never the whole review.
- **Design findings are graded against the app's own norms, with hard floors that
  never move.** A 39px button in a codebase where every button is 39px is fine — that's
  the project's own standard. A 20px icon button is not, because 24×24 is a WCAG
  floor and floors don't negotiate.

## Quick start

If you already have [Claude Code](https://claude.com/claude-code), [Cursor
CLI](https://cursor.com/cli), or [Codex CLI](https://github.com/openai/codex)
installed, this is genuinely three commands:

```bash
git clone https://github.com/ThatGuyAstro/reality-check.git
cd reality-check
./install.sh
```

Then, in your own project, with your dev server running (or not — it'll try to
start it for you):

```
reality-check http://localhost:3000
```

...and go make coffee. It reads your app, opens a browser, walks it end to end, and
leaves a full report plus a stack of ready-to-fix tickets in `docs/reality-check/`.

## Install

`install.sh` requires no arguments and no sudo. It symlinks this repo into every
skills directory it finds on your machine, so updating is just `git pull`:

```bash
./install.sh
```

That gives you:

| Where | What lands there |
|---|---|
| `~/.claude/skills/reality-check` | the skill, plus `/reality-check` slash-command shims in `~/.claude/commands/reality-check/` |
| `~/.codex/skills/reality-check` | the skill, for Codex CLI's skill loader |
| `~/.cursor/skills/reality-check` | the skill, for Cursor CLI's skill loader |
| `~/.agents/skills/reality-check` | the cross-runtime skills hub some tools share |

If you were already running an earlier version of this skill under the name
`reality-check`, the installer keeps your previous one reachable at
`reality-check-v1` instead of silently replacing it.

**Claude Code:** once installed, just say what you want in plain English —
"reality-check this app," "does the signup flow actually work," "tour
localhost:3000" — or invoke a mode directly with `/reality-check`,
`/reality-check:verify`, `/reality-check:recheck`, and so on (see
[Modes](#modes)).

**Cursor CLI and Codex CLI:** neither has slash commands for skills yet, so just
type the skill name and your request in chat:

```
reality-check http://localhost:5173
reality-check :recheck TKT-004
```

**Anything else that can read files and drive a browser:** this skill has no
Claude-Code-only dependencies. `SKILL.md` is the entire instruction set; everything
under `references/`, `templates/`, and `personas/` is plain Markdown and JSON. Point
any sufficiently capable agent at `SKILL.md` and tell it to follow the rules.

**One real dependency:** the [`agent-browser`](https://www.npmjs.com/package/agent-browser)
CLI, which is how the verify phase actually drives a browser.

```bash
npm i -g agent-browser
agent-browser install
```

## A worked example

Say your app has a sign-in page, and the sign-in code looks roughly like this:

```html
<a class="register-link" href="register.html">Create account</a>
```
```css
.register-link { display: none; }
```

**Phase 1 (Tour)** reads that and — because a user reading the label "Create
account" has no idea the CSS hides it — writes:

> *"Below the form there is a link that says Create account."* `[clm-login-4]`
> — confidence: `guess`

**Phase 2 (Verify)** opens a real browser, checks the sign-in page, and finds the
link is in the DOM but `is visible` returns `false`. That's a straight contradiction:

```
clm-login-4   exists   guess   contradicted / model-belief
  observed: "present in DOM, is visible: false (css/app.css:45 .register-link
             { display: none; })"
  screenshot: surfaces/login/screenshots/clm-login-4.png
```

**Phase 3 (Tickets)** turns that into something dispatchable:

```
┌─────────────────────────────────────────────────────────────────────┐
│ TKT-003 · high · functional · model-belief                          │
│                                                                       │
│ Create account link is hidden by CSS and unreachable                │
│                                                                       │
│ Believed:  "Below the form there is a link that says Create          │
│             account." (guess)                                        │
│ Observed:  present in the DOM, is visible: false                     │
│ Source:    css/app.css:45, index.html:21                             │
│ Fix:       remove the `.register-link { display: none; }` rule       │
│                                                                       │
│ Agent brief:                                                         │
│   Open: css/app.css, index.html                                      │
│   Must pass: is visible ".register-link" -> true                     │
│   Then run: reality-check :recheck TKT-003                           │
└─────────────────────────────────────────────────────────────────────┘
```

Fix the CSS, run `reality-check :recheck TKT-003`, and the ticket flips itself to
`fixed` — with the new screenshot as proof.

## What it actually exercises

Most "UI testing" checks that things exist. This checks that they *behave*, in every
state a person can put them in:

```
  COMPONENT STATES                     PAGE DYNAMICS
  ──────────────────                   ──────────────────
  rest · hover · focus-visible         every declared breakpoint (+/- 1px)
  active · disabled (+ reason)         light · dark · reduced motion
  busy · loading · empty · error       dialogs: focus in, trap, Escape, return
  open · expanded · selected           menus: outside click, Escape
  invalid · dirty · submitting         forms: empty submit, bad input, double submit
  succeeded · failed                   sticky chrome vs anchors and inner scroll
  overflow (long strings, long lists)  soft vs hard navigation, back, deep link
  offline · synthesized via mocks      keyboard-only path, toasts and timers
```

Each state gets a row in `states.jsonl` (present / missing / broken), an element
screenshot taken while the state holds, and a computed-style diff against rest. The
critique then reads the page the way a designer would: hierarchy, grouping,
repetition, signifiers, copy honesty, consistency across surfaces, using named
heuristics (Nielsen, Gestalt, Norman, Fitts) with a measurement behind each
sentence. The vocabulary lives in
[`references/ui-state-model.md`](references/ui-state-model.md).

## What you get back

Everything lands in `docs/reality-check/` inside the project you ran it against —
never inside this skill's own folder:

```
docs/reality-check/
├── environment.md          how the app runs: dev command, URL, seed accounts
├── rubric.md                the project's own design norms + floors + doc promises
├── tour.md                  the narrated demo script, scene by scene
├── tour.verified.md         the same script, every line marked [confirmed]/[contradicted]
├── results.md                the headline numbers, printed and saved
├── claims.jsonl              one row per narrated claim
├── verdicts.jsonl             one row per verdict, append-only across re-runs
├── states.jsonl               one row per component state and page dynamic exercised
├── observations.jsonl        things a human would notice that the tour never predicted
├── findings.jsonl             measured design/UX findings
├── surfaces/
│   └── <page-slug>/
│       ├── components.md     this page's state inventory (what the code declares per component)
│       ├── claims.md         this page's claim ledger
│       ├── verification.md   this page's verdicts, state rows, evidence
│       ├── critique.md       design read, state matrix, transformations, findings
│       └── screenshots/      proof for every verdict, state, and finding
└── tickets/
    ├── index.md               every ticket, by severity, in the order a user hits them
    ├── tickets.jsonl
    └── TKT-001-login.md       one dispatchable file per ticket
```

Nothing here is a black box. Every number in the summary traces back to a row in a
`.jsonl` file, and every row points at a screenshot you can open and check yourself.

## The claim vocabulary

Every sentence in the tour is exactly one claim, of exactly one kind:

| Kind | Says | Verified by |
|---|---|---|
| `exists` | something is present and visible | snapshot + visibility check |
| `shows` | specific text or data is displayed | reading the text, quoted |
| `looks` | a visual property holds (layout, style, state) | a screenshot + a measurement |
| `does` | a control produces an effect | performing it, then checking for one |
| `flows` | an action moves you from page A to page B | performing it, checking the destination |
| `state` | something persists across reload or navigation | performing it, then reloading and re-checking |
| `promise` | copy or docs promise a capability | quoting the promise, then attempting it |

Every claim also carries a **confidence tag**, set once during the tour and never
touched again during verification:

- **`sure`** — one clear line of code says so.
- **`inferred`** — pieced together from a few places.
- **`guess`** — the narrator filled a real gap (no handler, hidden by CSS, target
  file missing).

The headline number the whole thing is built around: **what fraction of confident
claims turned out wrong, versus what fraction of guesses did.** If your `sure`
claims are holding at 100% and your `guess` claims are cratering, you've just
measured exactly where your code is misleading a reader — which is the whole point.

## Modes

| Mode | What it does |
|---|---|
| `reality-check <url>` | full pipeline: tour → verify → tickets → results |
| `:tour` | phase 1 only — code reading, no browser at all |
| `:verify <url>` | phase 2 only, against an existing tour |
| `:tickets` | phase 3 only, against existing verification |
| `:recheck <TKT-id \| claim-id \| --all>` | re-verify and flip ticket status; `--all` reports regressions and fixes separately |
| `:surface <slug>` | scope any phase to a single page/surface |
| `:persona <name>` | narrate as a different kind of user (see below) |
| `:viewport <WxH>` | run at a specific viewport, default `1920x1080` |
| `:mobile` | also run a `390x844` mobile pass |
| `:mutate` | allow destructive actions (delete, cancel, pay) — off by default |
| `:auth <user> <pass>` | explicit login credentials for the verify pass |

Modes compose: `reality-check :verify :mobile :mutate` is a completely valid
sentence. There's also environment-variable support for CI-style runs:
`REALITY_CHECK_URL`, `REALITY_CHECK_USER`, `REALITY_CHECK_PASS`.

## Personas

The narrator has a voice, and the voice changes what it notices. Eight are bundled;
`howto` is the default:

| Persona | Notices most |
|---|---|
| `howto` | what a brand-new user sees and clicks, in order |
| `skeptical-evaluator` | edge cases, empty states, permission gates, promises |
| `onboarding-newcomer` | first-run friction, unclear labels |
| `power-user` | shortcuts, bulk actions, keyboard paths |
| `sales-demo` | the happy path, the wow moments |
| `investor-demo` | polish, trust signals, credibility |
| `support-walkthrough` | error states, recovery paths |
| `accessibility-auditor` | contrast, focus order, screen-reader labels |

Drop your own into `docs/reality-check/personas/<name>.md` in the target project
and call it with `:persona <name>`.

## Design rules, in one breath each

- **Codebase-agnostic** — framework, router, and auth model are discovered, never
  assumed.
- **Standardized output** — every project gets the identical `docs/reality-check/`
  tree, so downstream tooling (and your own muscle memory) can rely on the shape.
- **Evidence or it didn't happen** — no verdict without a screenshot, no finding
  without a measurement and a file.
- **Floors never adapt, norms always do** — WCAG contrast, hit-area size, and
  visible focus are non-negotiable; everything else is graded against what the
  project itself already does consistently.
- **A dead thing the code correctly predicted is still a bug** — a button
  narrated (accurately!) as "does nothing" still becomes a ticket. Being right
  about a bug doesn't make it not a bug.
- **Tool flakiness is not a product bug** — if a programmatic click proves a
  handler works but the pointer-click path is flaky, that's a low-severity note,
  not a blocker ticket.

## Re-checking after a fix

Once tickets exist, fixing one and re-running is a single command:

```
reality-check :recheck TKT-003
```

This re-verifies just that ticket's sources, appends a new verdict row (the old
one is never deleted — `verdicts.jsonl` is append-only across every run), and
flips the ticket to `fixed` if everything now checks out. Run it with `--all`
after a bigger change and it'll tell you two separate things: what got fixed, and
— just as importantly — what used to work and just broke.

## Try it on the bundled fixtures

This repo ships three tiny, self-contained demo apps with intentionally planted bugs,
used to prove the skill actually catches what it claims to catch. Two plant
functional gaps (dead buttons, hidden links, missing pages); the third, Orbit, plants
sixteen state, transformation, and design defects that no static audit finds: an
untrapped dialog, a menu that never closes, hover-only actions, a skeleton that never
resolves, a form that names no field, dark-mode white islands, a breakpoint that
overlaps and overflows, a link dressed as a button, raw identifiers in copy, and a
global `outline: none`.

```bash
cd fixtures/ledgerlite/site && python3 -m http.server 4173 &
reality-check http://localhost:4173
```

Each fixture's `ANSWER-KEY.md` lists every planted defect (never read these before
running — that defeats the point). Grade a finished run against the key with:

```bash
python3 grade.py docs/reality-check --fixture ledgerlite   # or: acme, orbit
```

## Origin story

This skill wasn't designed top-down. It's the merged result of a small experiment:
two separate AI agent sessions were independently given the same brief — build a
skill that measures the gap between what code implies and what a browser shows —
with no visibility into each other's work. Both built genuinely good, genuinely
different tools.

Rather than pick a favorite by reading the code, both were run cold against **each
other's** test fixtures, graded purely by checking the artifacts they produced on
disk (never by trusting their own self-reported summary). The comparison surfaced
real, specific misses in both: one skill quietly dropped a hidden button that its
own rules should have caught; the other filed several false "broken" tickets
against features that worked fine, tripped up by a flaky click and an
overly-generic size threshold.

This repo is the result of taking the better half of each design, closing every
specific miss the head-to-head test found, and then re-running the whole
comparison against the merged version until it beat both parents on both
fixtures with zero false positives. The full before/after evidence is in
[`docs/tests/`](docs/tests/).

## Evaluation

Every rule change in this skill's history traces to a real, cited failure from an
actual run — not a hypothetical. The short version, from
[`docs/tests/2026-09-11-merge-green.md`](docs/tests/2026-09-11-merge-green.md):

- Across five full cold runs (three on one fixture, two on the other) plus one
  re-check run, **every planted defect was caught and ticketed, every time.**
- **Zero tickets were ever filed against a feature that actually worked.**
- A flaky pointer-click occurred live during testing (three real cases) and was
  correctly absorbed as a low-severity note instead of a false blocker ticket in
  every case.
- Along the way, it also caught two *real, unplanted* bugs in the fixture apps
  that nobody had put there on purpose — a login handler that silently discards a
  saved display name, and a dark-mode contrast regression.

## FAQ

**Does this replace tests?** No. Unit and integration tests check that code does
what the *developer* intended. This checks whether the app does what a *user*
reading the interface would reasonably expect — a different, and often bigger,
gap. Both matter.

**Will it click "Delete Account"?** Not unless you pass `:mutate`. Destructive
actions are blocked by default and reported as such.

**Does it need my app's source, or just a URL?** Both. The tour phase reads your
source code; the verify phase needs a running (or startable) app to open in a
browser. If it can find your dev command in `package.json` or the equivalent, it
will start the app itself.

**What if my app needs a login?** Point it at seed credentials in your README,
`.env`, or test fixtures, or pass `:auth <user> <pass>` directly.

**Is this specific to any framework?** No — Next.js, plain HTML, Rails, Django,
Vite, whatever. The tour phase discovers your dev command, routing, and auth model
from the code itself rather than assuming a stack.

**Can I trust the tickets it writes?** Every verdict cites a screenshot and a
quoted browser observation, and every finding cites a measured value and a file.
Nothing is asserted from reading code alone — that's the entire premise of the
tool.

## Contributing

Issues and pull requests are welcome — especially real-world runs against
frameworks or auth patterns this hasn't been tested on yet. If you're proposing a
change to the skill's *rules* (not just a typo fix), the most useful PR includes:

1. What real run exposed the gap (a claim that should have been caught and wasn't,
   or a false positive that shouldn't have fired).
2. The specific rule change.
3. A re-run of `grade.py` against both bundled fixtures showing the fix holds and
   nothing regressed.

That's the same bar this skill was held to during its own development — every rule
here earned its place by fixing something a real cold run got wrong.

## License

MIT — see [`LICENSE`](LICENSE).
