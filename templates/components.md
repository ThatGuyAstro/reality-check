# Components: <slug>

Written in phase 1 from the code only. One row per component class on this surface. "Declared" lists the states the code styles or branches on, with `path:line`. "Expected, undeclared" lists states `references/ui-state-model.md` section 2 expects for the class that the code never mentions; each becomes a `guess` claim.

| component | instances (selector or label) | declared states (path:line) | expected, undeclared | claims |
|---|---|---|---|---|
| button.primary | "Save", "New item" | hover css/app.css:41; focus-visible app.css:60; disabled app.css:70 (no reason) | busy | clm-<slug>-12, clm-<slug>-13 |
| list row | .row | hover app.css:120 (reveals .rowAction) | focus-visible, selected, empty, error, loading | clm-<slug>-20 |
| dialog | "New item" | open/closed Dialog.tsx:30 | focus trap, Escape, focus return | clm-<slug>-30 |
| page | - | breakpoints 900 app.css:400; .dark app.css:1; reduced-motion app.css:900 | - | clm-<slug>-40, clm-<slug>-41 |
