#!/usr/bin/env python3
import csv, os
import math

OUTDIR = 'figs'
os.makedirs(OUTDIR, exist_ok=True)
csv_path = 'results.csv'
png_out = os.path.join(OUTDIR, 'impl1_times.png')

def read_impl1(csv_path):
    data = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        r = csv.DictReader(f)
        for row in r:
            if row.get('impl') != 'impl_1':
                continue
            try:
                n = int(row.get('n_items', 0))
                t = float(row.get('time', 0.0))
            except:
                continue
            # keep maximum observed time for the n (reflecting timeouts)
            if n not in data or t > data[n]:
                data[n] = t
    return dict(sorted(data.items()))

data = read_impl1(csv_path)
if not data:
    print('No impl_1 data found in', csv_path)
    raise SystemExit(1)

ns = list(data.keys())
ts = [data[n] for n in ns]

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
except Exception as e:
    print('matplotlib not available or failed to import:', e)
    print('Please install matplotlib (pip install matplotlib) and re-run this script.')
    raise

plt.figure(figsize=(7,4))
plt.plot(ns, ts, marker='o', linestyle='-', label='impl_1 (naive)')
plt.yscale('log')
plt.xlabel('n (number of items)')
plt.ylabel('tempo (s) [escala log]')
plt.title('Tempos medidos — implementação ingênua (impl_1)')
plt.grid(True, which='both', ls='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig(png_out, dpi=200)
print('Wrote', png_out)
