# Environment

| Field | Value | Provenance |
|---|---|---|
| Run id | run-<YYYYMMDD-HHMM> | - |
| Dev command | `<command>` | evidenced (<path:line>) \| inferred |
| Base URL | <url> | evidenced (<path>) \| inferred \| given (invocation) |
| Entry surface | <route or file> | evidenced (<path>) |
| Auth | <none \| form login at <route> \| external provider> | evidenced (<path>) \| inferred |
| Credentials | <user> / <where the password is documented, never a real secret> | evidenced (<path>) \| inferred \| given |
| Seed data | <what exists on first run> | evidenced (<path>) \| inferred |
| Notes | <anything the verifier must know before starting> | - |

## Startup log (filled in by phase 2; in phase 0 when a URL was given, write "URL given, no dev command run")
```
<captured stdout of the dev command, first 40 lines; or "URL given and reachable, no dev command run"; or the reason the app did not start>
```
