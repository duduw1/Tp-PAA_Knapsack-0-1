#!/usr/bin/env python3
"""
Randomized tests runner for knapsack implementations in `src/`.
Generates instances and runs implementations: 1_brutalF (small n), 2_pd, 3_greed, 4_pd_com_itens.
Saves results to `scripts/random_results.csv` and prints a short summary.
"""
import random, time, csv, os, importlib.util

BASE = os.path.dirname(os.path.abspath(__file__))
# Project root (parent of scripts)
ROOT = os.path.dirname(BASE)
SRC = os.path.join(ROOT, 'src')
OUT = os.path.join(BASE, 'random_results.csv')

# Helper to load module by path
def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

mods = {}
# Expected files in src
candidates = {
    'impl_1': [os.path.join(SRC, '1_brutalF.py'), os.path.join(ROOT, '1_brutalF.py')],
    'impl_2': [os.path.join(SRC, '2_pd.py'), os.path.join(ROOT, '2_pd.py')],
    'impl_3': [os.path.join(SRC, '3_greed.py'), os.path.join(ROOT, '3_greed.py')],
    'impl_4': [os.path.join(SRC, '4_pd_com_itens.py'), os.path.join(ROOT, '4_pd_com_itens.py')],
}

for k, paths in candidates.items():
    loaded = False
    for p in paths:
        if os.path.exists(p):
            try:
                mods[k] = load_module(p, k)
                loaded = True
                break
            except Exception as e:
                print('Failed to load', p, e)
    if not loaded:
        print('Module not found for', k, 'checked paths:', paths)

# Test parameters
ns = [8, 12, 16, 20, 24]
reps = 5
max_weight = 20
max_value = 100

rows = []
for n in ns:
    for r in range(reps):
        items = []
        for i in range(n):
            w = random.randint(1, max_weight)
            v = random.randint(1, max_value)
            items.append({'w': w, 'v': v})
        capacity = sum(it['w'] for it in items) // 2
        val = [it['v'] for it in items]
        wt = [it['w'] for it in items]

        for impl_name, mod in mods.items():
            rec = {'impl': impl_name, 'n': n, 'capacity': capacity, 'status': 'ok', 'time': None, 'result': None, 'ops': 0, 'error': ''}
            try:
                t0 = time.perf_counter()
                # impl_4 has knapsack_with_items; others return int
                if impl_name == 'impl_4' and hasattr(mod, 'knapsack_with_items'):
                    res = mod.knapsack_with_items(capacity, val, wt)[0]
                else:
                    res = mod.knapsack(capacity, val, wt)
                t1 = time.perf_counter()
                rec['time'] = t1 - t0
                rec['result'] = int(res)
                # Capture operations count if available
                if hasattr(mod, 'OPS'):
                    rec['ops'] = mod.OPS
            except RecursionError as re:
                rec['status'] = 'recursion_error'
                rec['error'] = str(re)
            except Exception as e:
                rec['status'] = 'error'
                rec['error'] = str(e)
            rows.append(rec)
        # end for mods
    # end reps
# end ns

# Save CSV
keys = ['impl','n','capacity','status','time','result','ops','error']
with open(OUT, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=keys)
    w.writeheader()
    for row in rows:
        w.writerow(row)

print('Wrote', OUT)
# Quick summary: for each n, compare impl_3 vs impl_4 results (gap)
import math
from collections import defaultdict
by_n = defaultdict(list)
for row in rows:
    by_n[row['n']].append(row)

print('\nSummary (avg times, avg gap greedy vs exact):')
for n, recs in sorted(by_n.items()):
    times = defaultdict(list)
    ops_by_impl = defaultdict(list)
    res_by_impl = defaultdict(list)
    for r in recs:
        times[r['impl']].append(r['time'] if r['time'] is not None else float('nan'))
        res_by_impl[r['impl']].append(r['result'])
        ops_by_impl[r['impl']].append(r['ops'])
        
    avg_times = {impl: sum([t for t in times[impl]])/len(times[impl]) for impl in times}
    avg_ops = {impl: sum([op for op in ops_by_impl[impl]])/len(ops_by_impl[impl]) for impl in ops_by_impl}
    
    # compute gap: average over repetitions of (opt - approx)
    gaps = []
    for i in range(reps):
        try:
            vopt = res_by_impl['impl_4'][i]
            vapprox = res_by_impl['impl_3'][i]
            gaps.append(vopt - vapprox)
        except Exception:
            pass
    avg_gap = sum(gaps)/len(gaps) if gaps else None
    
    print(f'n={n}:')
    for impl in sorted(avg_times):
        print(f"  {impl}: time={avg_times[impl]:.4f}s, ops={avg_ops[impl]:.1f}")
    if avg_gap is not None:
        print(f"  avg_gap={avg_gap:.2f}")

print('\nDone')