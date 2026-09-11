#!/usr/bin/env python3
"""Format-agnostic outcome grader for reality-check v2 runs of the planted fixtures.
Usage: python3 grade.py <docs/reality-check dir> --fixture ledgerlite|acme
Reads artifacts on disk; never trusts a run report."""
import json, sys, os, glob, re
args=[a for a in sys.argv[1:] if not a.startswith('--')]
fx=sys.argv[sys.argv.index('--fixture')+1] if '--fixture' in sys.argv else None
D=args[0] if args else '.'
def jl(n):
    p=os.path.join(D,n); return [json.loads(l) for l in open(p) if l.strip()] if os.path.exists(p) else []
claims,verdicts,obs,findings,tickets=jl('claims.jsonl'),jl('verdicts.jsonl'),jl('observations.jsonl'),jl('findings.jsonl'),jl('tickets/tickets.jsonl')
cl={c['id']:c for c in claims}; latest={}
for v in verdicts: latest[v['claim']]=v
def blob(x): return json.dumps(x).lower()
def claims_where(pred): return [c for c in claims if pred(blob(c))]
def latest_v(cs): return [latest.get(c['id'],{}).get('verdict','') for c in cs]
def any_contra(cs): return any(v.startswith('contradicted') for v in latest_v(cs))
def any_conf(cs): return 'confirmed' in latest_v(cs)
def tk(pred): return [t for t in tickets if pred(blob(t)+' '+open(os.path.join(D,t['file'])).read().lower() if os.path.exists(os.path.join(D,t['file'])) else blob(t))]
def ob(pred): return [o for o in obs if pred(blob(o))]
def fd(pred): return [f for f in findings if pred(blob(f))]
checks=[]
def check(name,ok,detail): checks.append((name,bool(ok),detail))
# structure
for n in ['manifest.json','tour.md','tour.verified.md','results.md','claims.jsonl','verdicts.jsonl','observations.jsonl','findings.jsonl','tickets/index.md','tickets/tickets.jsonl','rubric.md','environment.md']:
    if not os.path.exists(os.path.join(D,n)): check('required file '+n,False,'missing')
check('every verdict row has claim/run_id/verdict/url/screenshot/observed', all(all(k in v for k in ('claim','run_id','verdict','url','screenshot','observed')) for v in verdicts), f'{len(verdicts)} rows')
missing=[v['screenshot'] for v in verdicts if not os.path.exists(os.path.join(D,v['screenshot'])) and not os.path.exists(v['screenshot'])]
check('every cited verdict screenshot exists', verdicts and not missing, f'missing {missing[:5]}')
check('every contradicted row has a gap', all(v.get('gap') for v in verdicts if v['verdict'].startswith('contradicted')), '')
tfiles=glob.glob(os.path.join(D,'tickets','TKT-*.md'))
bad=[os.path.basename(f) for f in tfiles if 'Agent brief' not in open(f).read() or not re.search(r'## Acceptance\s*```', open(f).read())]
check('every ticket has a fenced Acceptance block and an Agent brief', tfiles and not bad, f'{len(tfiles)} tickets; bad {bad}')
def flagged(name, cpred, tpred):
    cs=claims_where(cpred); t=tk(tpred); o=ob(tpred); f=fd(tpred)
    check(f'{name}: flagged (contradicted claim, obs, or finding)', any_contra(cs) or o or f, f'claims {[(c["id"],latest.get(c["id"],{}).get("verdict")) for c in cs]}; obs {[x["id"] for x in o]}; findings {[x["id"] for x in f]}')
    check(f'{name}: ticketed', bool(t), f'tickets {[x["id"] for x in t]}')
    return t
if fx=='ledgerlite':
    flagged('D1 Export CSV', lambda s:'export' in s, lambda s:'export' in s and 'csv' in s)
    flagged('D2 Reports 404', lambda s:'reports' in s, lambda s:'reports' in s)
    flagged('D3 hidden Create account link', lambda s:'create account' in s or 'register' in s, lambda s:'create account' in s or 'register' in s)
    con=fd(lambda s:('synced' in s or 'b5b5b5' in s) and 'contrast' in s)
    check('D4 caption contrast finding with numeric ratio', any(re.search(r'\d\.\d',f.get('observed','')) for f in con), f'{[(f["id"],f.get("observed","")[:60]) for f in con]}')
    check('D4 ticketed', bool(tk(lambda s:'synced' in s or 'b5b5b5' in s)), '')
    hit=fd(lambda s:'refresh' in s or 'icon-btn' in s)
    check('D5 20px icon button finding names .icon-btn', any('icon-btn' in blob(f) for f in hit), f'{[(f["id"],f.get("observed","")[:50]) for f in hit]}')
    check('D5 ticketed', bool(tk(lambda s:'icon-btn' in s or 'refresh' in s)), '')
    flagged('D6 two-factor promise', lambda s:'two-factor' in s or '2fa' in s, lambda s:'two-factor' in s or '2fa' in s)
    for name,pred in [('login lands on dashboard',lambda s:'dashboard' in s and ('sign in' in s or 'press' in s or 'log in' in s or 'takes me' in s or 'land' in s)),('wrong password error',lambda s:'incorrect' in s),('three cards',lambda s:'card' in s),('save shows Saved',lambda s:'saved' in s),('theme persists',lambda s:'dark' in s or 'theme' in s),('log out returns',lambda s:'log out' in s or 'logout' in s or 'sign out' in s)]:
        cs=claims_where(pred); check('working path confirmed: '+name, any_conf(cs), f'{[(c["id"],latest.get(c["id"],{}).get("verdict")) for c in cs]}')
    fp=[t['id'] for t in tickets if any(latest.get(s,{}).get('verdict')=='confirmed' for s in t.get('sources',[]))]
    check('no ticket sourced from a confirmed claim (working paths untouched)', not fp, f'{fp}')
    btn=[f['id'] for f in findings if f.get('category')=='hit-areas' and '.btn' in blob(f) and '39' in blob(f) and f.get('status')!='retired']
    check('no hit-area finding on the 39px .btn controls (project norm)', not btn, f'{btn}')
elif fx=='acme':
    flagged('P1 register link 404', lambda s:'create an account' in s or 'register' in s, lambda s:'register' in s or 'create an account' in s)
    flagged('P2 Export CSV no-op', lambda s:'export' in s, lambda s:'export' in s)
    flagged('P3 hidden Reports nav', lambda s:'reports' in s, lambda s:'reports' in s)
    cs=claims_where(lambda s:'save' in s and ('toast' in s or 'saved' in s)); check('P4 Save confirmed', any_conf(cs), f'{[(c["id"],latest.get(c["id"],{}).get("verdict")) for c in cs]}')
    fp=[t['id'] for t in tickets if any(latest.get(s,{}).get('verdict')=='confirmed' for s in t.get('sources',[]))]
    check('no ticket sourced from a confirmed claim (Save, Settings link, Sign out untouched)', not fp, f'{fp}')
    flaky=[t['id'] for t in tickets if 'pointer-click-flaky' in blob(t) and t['severity'] in ('critical','high')]
    check('no critical/high ticket from a pointer-click flake', not flaky, f'{flaky}')
    con=fd(lambda s:'hint' in s and 'contrast' in s)
    check('P5 hint contrast finding with numeric ratio', any(re.search(r'\d\.\d',f.get('observed','')) for f in con), f'{[(f["id"],f.get("observed","")[:60]) for f in con]}')
    check('P5 fix names css/app.css .hint', any('app.css' in blob(f) and '.hint' in blob(f) for f in con), '')
    check('P5 ticketed', bool(tk(lambda s:'hint' in s and 'contrast' in s)), '')
    for name,pred in [('login lands on dashboard',lambda s:'dashboard' in s and ('sign in' in s or 'press' in s)),('wrong credentials error',lambda s:'not right' in s or 'wrong' in s),('greeting',lambda s:'welcome back' in s),('stat cards',lambda s:'27' in s or 'open tasks' in s),('sign out returns',lambda s:'sign out' in s)]:
        cs=claims_where(pred); check('working path confirmed: '+name, any_conf(cs), f'{[(c["id"],latest.get(c["id"],{}).get("verdict")) for c in cs]}')
    btn=[f['id'] for f in findings if f.get('category')=='hit-areas' and ('37' in blob(f) or '39' in blob(f)) and '24' not in f.get('observed','') and f.get('status')!='retired']
    check('no hit-area finding on the 37-39px buttons (above floor, at norm)', not btn, f'{btn}')
else:
    check('--fixture given', False, 'ledgerlite|acme')
from collections import Counter
print(f'reality-check v2 grade for {D} ({fx})\nclaims={len(claims)} verdicts={len(verdicts)} observations={len(obs)} findings={len(findings)} tickets={len(tickets)}')
print('verdicts:', Counter(v['verdict'].split('(')[0] for v in latest.values()))
for n,ok,d in checks: print(('PASS ' if ok else 'FAIL ')+n+('  -- '+d if d else ''))
print(f'\n{sum(1 for _,ok,_ in checks if ok)}/{len(checks)} checks pass')
sys.exit(0 if all(ok for _,ok,_ in checks) else 1)
