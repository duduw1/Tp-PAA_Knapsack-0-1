#!/usr/bin/env python3
import csv, math, os

csv_path = 'results.csv'
out_tex = 'knapsack_report.tex'

if not os.path.exists(csv_path):
    print('results.csv not found in current directory')
    raise SystemExit(1)

# Read impl_1 timings and group by n_items (take max per n to reflect worst-case/timeouts)
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
        # keep the maximum observed time for that n
        if n not in data or t > data[n]:
            data[n] = t

if not data:
    print('No impl_1 data found in results.csv')
    raise SystemExit(1)

# Sort by n
items = sorted(data.items())

# Use points with n>=10 for fitting to avoid noise from tiny times
fit_points = [(n,t) for n,t in items if n >= 10 and t>0]
if not fit_points:
    fit_points = [(n,t) for n,t in items if t>0]

ns = [n for n,t in fit_points]
ts = [t for n,t in fit_points]

# Linear regression on ln(t) = A + B*n
ln_ts = [math.log(t) for t in ts]
N = len(ns)
mean_n = sum(ns)/N
mean_ln = sum(ln_ts)/N
num = sum((ns[i]-mean_n)*(ln_ts[i]-mean_ln) for i in range(N))
den = sum((ns[i]-mean_n)**2 for i in range(N))
if den == 0:
    B = 0.0
else:
    B = num/den
A = mean_ln - B*mean_n
a = math.exp(A)
b = math.exp(B)

# Largest measured n
n_max = max(data.keys())
# Estimate for 10x input in terms of n (n' = 10 * n_max)
n_10x = 10 * n_max
est_10x = a * (b**(n_10x))

def human_time(seconds):
    if seconds < 1:
        return f"{seconds:.6f} s"
    minutes = seconds/60
    if minutes < 60:
        return f"{minutes:.3f} min ({seconds:.3f} s)"
    hours = minutes/60
    if hours < 24:
        return f"{hours:.3f} h ({seconds:.0f} s)"
    days = hours/24
    if days < 365:
        return f"{days:.3f} days ({seconds:.0f} s)"
    years = days/365
    return f"{years:.3e} years ({seconds:.3e} s)"

# Build LaTeX content for Section 2
lines = []
lines.append('% Auto-generated Section 2 for knapsack_report.tex')
lines.append('\\section{Seção 2 — Medições do algoritmo ingênuo (1.py) e extrapolações}')
lines.append('A seguir estão os tempos medidos para a implementação ingênua (\\texttt{1.py}). O maior input testado foi $n=%d$.'% (n_max))
lines.append('\\begin{table}[h]\\centering')
lines.append('\\begin{tabular}{@{}rrr@{}}')
lines.append('\\toprule')
lines.append('$n$ & tempo (s) & tempo (legível)\\')
lines.append('\\midrule')
for n,t in items:
    lines.append(f'{n} & {t:.6e} & {human_time(t)}\\')
lines.append('\\bottomrule')
lines.append('\\end{tabular}')
lines.append('\\caption{Tempos medidos para \\texttt{1.py} (por $n$).}\\end{table}')

lines.append('\\bigskip')
lines.append('Usamos um ajuste exponencial do tipo $T(n) \\approx a \\cdot b^{n}$ para modelar o crescimento observado. Uma regressão linear em $\\ln T$ vs $n$ fornece:')
lines.append('\\[ a = %.4e,\\qquad b = %.6f. \\\\]' % (a,b))
lines.append('Com esse modelo, para uma entrada 10\\times maior (\\(n = %d\\)) estimamos:' % (n_10x))
lines.append('\\begin{itemize}')
lines.append('  \\item Estimativa (segundos): %.3e \\\\' % (est_10x))
lines.append('  \\item Estimativa (legível): %s \\\\' % (human_time(est_10x)))
lines.append('\\end{itemize}')


# Write full minimal LaTeX document (user will add rest later)
doc = (
    "\\documentclass[11pt,a4paper]{article}\\n"
    "\\usepackage[utf8]{inputenc}\\n"
    "\\usepackage[brazil]{babel}\\n"
    "\\usepackage{booktabs}\\n"
    "\\usepackage{siunitx}\\n"
    "\\begin{document}\\n"
    "\\section*{Relat\\'orio - Se\\c{c}\\~ao 2}\\n"
)
doc += "\n".join(lines)
doc += "\n\\end{document}\\n"

with open(out_tex, 'w', encoding='utf-8') as f:
    f.write(doc)

print('Wrote', out_tex)
print('Used points:', fit_points)
print('Fitted a=', a, 'b=', b)
print('Estimated time for n=%d: %s' % (n_10x, human_time(est_10x)))