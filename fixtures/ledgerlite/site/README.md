# Ledgerlite (fixture)

A tiny static bookkeeping dashboard used to exercise product-experience tooling.

## Run

```bash
cd site && python3 -m http.server 4173
```

Then open http://localhost:4173/.

## Test account

- Email: `demo@planted.test`
- Password: `planted-pass`

Sessions are stored in `localStorage` under `ledgerlite.session`. Display name and theme are stored under `ledgerlite.profile`.

## Product promises

- Every table can be exported as CSV.
- The interface targets WCAG AA contrast.

## Pages

- `index.html` - sign in
- `dashboard.html` - balances, recent transactions, sync and export
- `settings.html` - profile, theme, security
