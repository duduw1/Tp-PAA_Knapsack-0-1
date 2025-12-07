import math, csv
import numpy as np
xs=[]
ys=[]
with open('results.csv', 'r', encoding='utf-8') as f:
    r=csv.DictReader(f)
    for row in r:
        if row['impl']=='impl_1' and row['status'] in ('ok','timeout'):
            try:
                n=int(row['n_items'])
                t=float(row['time'])
            except:
                continue
            if n>=10:
                xs.append(n)
                ys.append(t)
xs=np.array(xs)
ys=np.array(ys)
mask=ys>0
xs=xs[mask]; ys=ys[mask]
lny=np.log(ys)
A=np.vstack([xs, np.ones_like(xs)]).T
slope, intercept = np.linalg.lstsq(A, lny, rcond=None)[0]
lnb=slope
lna=intercept
a=math.exp(lna)
b=math.exp(lnb)
print('data points (n,t):')
for x,y in zip(xs,ys): print(x,y)
print('\nFitted model: t = a * b^n')
print('a =',a)
print('b =',b)
nmax = max(xs)
est_nmax = a*(b**nmax)
n10 = 10*nmax
est_10x = a*(b**(n10))
print(f'largest n in fit: {nmax}')
print('estimate at nmax:', est_nmax)
print(f'estimate at 10x nmax (n={n10}):', est_10x)
years = est_10x/(3600*24*365)
print('est_10x in seconds:', est_10x)
print('est_10x in years:', years)
