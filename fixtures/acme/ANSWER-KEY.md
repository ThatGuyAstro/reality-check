# Planted answer key - fixtures/planted-app

Never copy this file into a run's fixture directory. The served root is `site/`.

| # | Plant | Where | Expected outcome from a correct run |
|---|---|---|---|
| P1 | "Create an account" links to `register.html`, which does not exist | `site/index.html` footer link | claim that registration exists/opens -> CONTRADICTED (404) |
| P2 | "Export CSV" button has no click handler (`js/app.js` only `void`s it) | `site/dashboard.html` toolbar | claim that export produces a download/anything -> CONTRADICTED (no-op) |
| P3 | "Reports" nav link present in markup but `display:none` | `site/dashboard.html`, `site/settings.html` sidebar | claim that Reports appears in nav -> CONTRADICTED (not visible) |
| P4 | Settings "Save" works: updates name and shows toast (control) | `site/settings.html`, `js/app.js` | claim -> CONFIRMED, not filed as a bug |
| P5 | Helper text "Use your work email address" is `#c9c9c9` on white (~1.7:1) | `site/css/app.css` `.hint` | critique finding with severity, contrast measurement, fix as `css/app.css` `.hint { color: ... }` |
| P6 | README promises "Every project table can be exported as CSV with one click"; export is a no-op (P2) | `site/README.md` line 3 | expectation row E-01 (promise) verified on dashboard -> CONTRADICTED; ticketed, quoting the README |

Also true and confirmable: login with demo@example.com / demo1234 lands on dashboard; wrong credentials show inline error; greeting says "Welcome back, Demo User."; three stat cards (3 / 27 / 4); sign out returns to sign-in.
