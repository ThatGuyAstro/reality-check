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
states=jl('states.jsonl')
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
import hashlib
def st(pred): return [x for x in states if pred(blob(x))]
def st_bad(pred): return [x for x in st(pred) if x.get('verdict') in ('missing','broken')]
def st_ok(pred): return [x for x in st(pred) if x.get('verdict')=='present']
def any_hit(name, pred):
    return st_bad(pred) or ob(pred) or fd(pred)
# ---- state-pass structure (every fixture) ----
surfs=[d for d in glob.glob(os.path.join(D,'surfaces','*')) if os.path.isdir(d)]
check('states.jsonl has rows', len(states)>0, f'{len(states)} rows')
def page_surface(d):
    c=os.path.join(d,'critique.md'); v=os.path.join(d,'verification.md')
    t=(open(c).read() if os.path.exists(c) else '')+(open(v).read() if os.path.exists(v) else '')
    return 'sweep: n/a' not in t and 'states: n/a' not in t
nocomp=[os.path.basename(d) for d in surfs if page_surface(d) and not os.path.exists(os.path.join(d,'components.md'))]
check('every surface has components.md', surfs and not nocomp, f'missing: {nocomp}')
crit_missing=[]
for d in surfs:
    c=os.path.join(d,'critique.md')
    if os.path.exists(c):
        t=open(c).read()
        if 'sweep: n/a' in t: continue   # feature surfaces and unrendered destinations carry no sweep
        for sec in ('## Design read','## State matrix','## Transformations'):
            if sec not in t: crit_missing.append((os.path.basename(d),sec))
check('every critique has Design read, State matrix, Transformations', not crit_missing, f'{crit_missing[:6]}')
def md5(p): return hashlib.md5(open(p,'rb').read()).hexdigest()
reused=[]
for f in findings:
    sp=os.path.join(D,f.get('screenshot',''))
    if not os.path.exists(sp): reused.append((f['id'],'missing')); continue
    surf=f['surface']; ov=[os.path.join(D,'surfaces',surf,'screenshots',n) for n in os.listdir(os.path.join(D,'surfaces',surf,'screenshots')) if n.endswith('--overview.png') or n.endswith('--full.png')]
    if any(os.path.exists(o) and md5(o)==md5(sp) for o in ov): reused.append((f['id'],'page capture'))
check('finding screenshots exist; at most 1 in 5 reuse a page capture', findings and not [r for r in reused if r[1]=='missing'] and len(reused)<=max(1,len(findings)//5), f'{reused[:6]}')
state_shots=[x for x in states if x.get('screenshot') and os.path.exists(os.path.join(D,x['screenshot']))]
check('state rows cite screenshots that exist', states and len(state_shots)>=0.8*len(states), f'{len(state_shots)}/{len(states)}')
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
elif fx=='orbit':
    # planted state / transformation / design defects; each must surface as a missing/broken state row, an observation, or a finding, and be ticketed
    plants=[
     ('P1 hover-only card actions (no keyboard path)', lambda s:('archive' in s or 'actions' in s) and ('hover' in s or 'focus' in s or 'keyboard' in s)),
     ('P2 New task dialog focus/trap/escape', lambda s:('dialog' in s or 'new task' in s) and ('focus' in s or 'escape' in s or 'trap' in s)),
     ('P3 filter menu never closes (outside click / Escape)', lambda s:('filter' in s or 'menu' in s) and ('escape' in s or 'outside' in s or 'close' in s)),
     ('P4 Calendar bare empty state', lambda s:'calendar' in s or ('no results' in s and 'empty' in s)),
     ('P5 comments skeleton never resolves', lambda s:('comment' in s or 'skeleton' in s) and ('resolve' in s or 'never' in s or 'stuck' in s or 'loading' in s)),
     ('P6 profile form: error names nothing / no success feedback', lambda s:('something went wrong' in s or 'display name' in s or 'profile' in s) and ('field' in s or 'success' in s or 'feedback' in s or 'invalid' in s or 'save' in s)),
     ('P7 Export disabled with no reason', lambda s:'export' in s and ('reason' in s or 'disabled' in s)),
     ('P8 dark mode: white card islands / menu text invisible', lambda s:'dark' in s and ('card' in s or 'menu' in s or 'white' in s or 'island' in s)),
     ('P9 900px overflow / sidebar overlap', lambda s:('900' in s or 'narrow' in s or 'overflow' in s or 'overlap' in s) and ('sidebar' in s or 'scrollwidth' in s or 'overflow' in s or 'column' in s)),
     ('P10 signifiers: link as primary button / button as link / two primaries / destructive no confirm', lambda s:('delete all done' in s or 'view archive' in s) or ('primary' in s and ('two' in s or 'compet' in s or 'more than one' in s)) or ('confirm' in s and 'delete' in s)),
     ('P11 raw identifiers in copy (usr_, IN_PROGRESS)', lambda s:'usr_' in s or 'in_progress' in s or 'identifier' in s or 'enum' in s),
     ('P12 repetition: Sample data / Learn more on every card', lambda s:'sample data' in s or 'learn more' in s or 'every card' in s),
     ('P13 motion: hover scale / slow transition / pulse ignores reduced motion', lambda s:('scale' in s or 'pulse' in s or 'reduced' in s or '600' in s or '.6s' in s) and ('hover' in s or 'motion' in s or 'dot' in s or 'animation' in s)),
     ('P14 sticky toolbar covers anchor target', lambda s:('sticky' in s or 'toolbar' in s) and ('anchor' in s or 'cover' in s or 'overlap' in s or 'hidden behind' in s or 'archived' in s)),
     ('P15 toast dismisses in 700ms', lambda s:'toast' in s and ('700' in s or 'fast' in s or 'dismiss' in s or 'read' in s)),
     ('P16 no focus ring on buttons (systemic)', lambda s:('focus' in s and ('ring' in s or 'outline' in s or 'visible' in s)) and 'button' in s),
    ]
    for name,pred in plants:
        hits=any_hit(name,pred); t=tk(pred)
        check(f'{name}: surfaced', bool(hits), f'states {[x["id"] for x in st_bad(pred)][:3]} obs {[x["id"] for x in ob(pred)][:3]} findings {[x["id"] for x in fd(pred)][:3]}')
        check(f'{name}: ticketed', bool(t), f'{[x["id"] for x in t][:4]}')
    # systemic clustering: focus ring should be one cluster, not per button
    focus_f=fd(lambda s:'focus' in s and ('ring' in s or 'outline' in s) and 'button' in s)
    check('P16 reported as one systemic finding (<=2 rows)', 0<len(focus_f)<=2, f'{[x["id"] for x in focus_f]}')
    # working paths: confirmed claims, present states, no tickets against them
    for name,pred in [('tabs switch with aria-selected / arrow keys', lambda s:'tab' in s and ('arrow' in s or 'selected' in s)),('search filters cards', lambda s:'search' in s),('sidebar collapse persists', lambda s:'collapse' in s or 'sidebar' in s),('done column helpful empty state', lambda s:'done' in s and 'empty' in s),('activity rows render', lambda s:'activity' in s and ('row' in s or 'three' in s or 'render' in s))]:
        cs=claims_where(pred); ok_states=st_ok(pred)
        check('working path present/confirmed: '+name, any_conf(cs) or bool(ok_states), f'claims {[(c["id"],latest.get(c["id"],{}).get("verdict")) for c in cs][:3]} states {[x["id"] for x in ok_states][:2]}')
    fp=[t['id'] for t in tickets if any(latest.get(s,{}).get('verdict')=='confirmed' for s in t.get('sources',[]))]
    check('no ticket sourced from a confirmed claim', not fp, f'{fp}')
    fp2=[t['id'] for t in tickets if ('done column' in blob(t) and 'empty' in blob(t) and 'helpful' not in blob(t) and 'bare' in blob(t)) or ('arrow' in blob(t) and 'tab' in blob(t))]
    check('no ticket against the Done empty state or the tabs', not fp2, f'{fp2}')
    # transformation coverage
    check('breakpoint 900 measured (state row narrow:900)', bool(st(lambda s:'narrow:900' in s or '"state": "narrow:9' in s)), '')
    check('dark mode measured (state row dark)', bool(st(lambda s:'"state": "dark"' in s)), '')
    check('reduced motion measured', bool(st(lambda s:'reduced-motion' in s)), '')
else:
    check('--fixture given', False, 'ledgerlite|acme|orbit')
from collections import Counter
print(f'reality-check v2 grade for {D} ({fx})\nclaims={len(claims)} verdicts={len(verdicts)} observations={len(obs)} findings={len(findings)} tickets={len(tickets)}')
print('verdicts:', Counter(v['verdict'].split('(')[0] for v in latest.values()))
for n,ok,d in checks: print(('PASS ' if ok else 'FAIL ')+n+('  -- '+d if d else ''))
print(f'\n{sum(1 for _,ok,_ in checks if ok)}/{len(checks)} checks pass')
sys.exit(0 if all(ok for _,ok,_ in checks) else 1)
